"""Geoscan UAV Flight Planner — FastAPI backend"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from export import missions_to_geojson, missions_to_kml
from optimizer import allocate_missions, allocate_multi_zone
from uav_specs import UAV_FLEET, UAVSpec, PAYLOAD_SPECS

app = FastAPI(title="Geoscan UAV Planner", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


# ─── Models ──────────────────────────────────────────────────────────────────

class LandingSite(BaseModel):
    """Взлётно-посадочный пункт (ВПП) — предопределённая площадка."""
    id: str
    latlon: list[float] = Field(..., min_length=2, max_length=2)
    name: Optional[str] = None


class UAVInstance(BaseModel):
    uav_type_id: str
    # Either a pre-defined site id OR explicit lat/lon (legacy / manual placement)
    site_id: Optional[str] = Field(None, description="ID ВПП из landing_sites")
    start_latlon: Optional[list[float]] = Field(None, min_length=2, max_length=2)
    land_latlon: Optional[list[float]] = None


class PlanRequest(BaseModel):
    area_polygon: Optional[list[list[float]]] = Field(None, description="[[lat,lon], ...] ≥3 points")
    area_polygons: Optional[list[list[list[float]]]] = Field(
        None, description="Несколько зон съёмки [[[lat,lon],...], ...]. Если задано, area_polygon игнорируется."
    )
    no_fly_zones: list[list[list[float]]] = Field(default_factory=list)
    airspace_boundary: Optional[list[list[float]]] = Field(
        None, description="Границы разрешённого воздушного пространства [[lat,lon],...]"
    )
    landing_sites: list[LandingSite] = Field(
        default_factory=list, description="Взлётно-посадочные пункты"
    )
    reserve_landing_areas: list[list[float]] = Field(
        default_factory=list, description="Резервные площадки посадки [[lat,lon],...]"
    )
    uavs: list[UAVInstance] = Field(..., min_length=1)
    payload_type: str = Field("rgb")
    altitude_m: float = Field(150.0, gt=0, le=4000)
    overlap_side: float = Field(0.3, ge=0, le=0.9)
    overlap_front: float = Field(0.7, ge=0, le=0.95)
    wind_speed_ms: float = Field(0.0, ge=0)
    wind_dir_deg: float = Field(0.0, ge=0, lt=360)
    optimization: str = Field("both", description="min_time | min_wear | both")
    startup_cost_min: float = Field(
        30.0, ge=0,
        description="Стоимость запуска одного БПЛА в минутах налёта (штраф на разворачивание)"
    )


class PlanResponse(BaseModel):
    missions: list[dict[str, Any]]
    geojson: dict[str, Any]
    summary: dict[str, Any]
    # Both optimization results when optimization="both"
    missions_min_time: Optional[list[dict[str, Any]]] = None
    missions_min_flight: Optional[list[dict[str, Any]]] = None
    geojson_min_time: Optional[dict[str, Any]] = None
    geojson_min_flight: Optional[dict[str, Any]] = None
    comparison: Optional[dict[str, Any]] = None


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _validate_and_build_uav_list(req: PlanRequest) -> list[dict]:
    # Build site lookup
    sites = {s.id: s.latlon for s in req.landing_sites}

    uav_list = []
    for inst in req.uavs:
        spec = UAV_FLEET.get(inst.uav_type_id)
        if not spec:
            raise HTTPException(400, f"Неизвестный тип БВС: {inst.uav_type_id}")

        # Payload compatibility check
        if req.payload_type not in spec.supported_payloads:
            raise HTTPException(
                400,
                f"{spec.name} не поддерживает съёмку типа «{req.payload_type}». "
                f"Доступно: {', '.join(spec.supported_payloads)}",
            )

        if req.wind_speed_ms > spec.max_wind_ms:
            raise HTTPException(
                400, f"{spec.name}: ветер {req.wind_speed_ms} м/с > макс. {spec.max_wind_ms} м/с"
            )
        if req.altitude_m > spec.max_altitude_agl_m:
            raise HTTPException(
                400, f"{spec.name}: высота {req.altitude_m} м > макс. {spec.max_altitude_agl_m} м"
            )

        # Resolve start_latlon: site_id takes priority over manual latlon
        if inst.site_id:
            if inst.site_id not in sites:
                raise HTTPException(400, f"Неизвестная ВПП: {inst.site_id}")
            start = sites[inst.site_id]
        elif inst.start_latlon:
            start = inst.start_latlon
        else:
            raise HTTPException(400, f"БВС {inst.uav_type_id}: не задан ни site_id, ни start_latlon")

        land = inst.land_latlon or start

        uav_list.append({
            "id": inst.uav_type_id,
            "spec": spec,
            "start_latlon": start,
            "land_latlon": land,
        })
    return uav_list


def _run_missions(req: PlanRequest, uav_list: list[dict], optimization: str) -> list[dict]:
    active_zones = getattr(req, "_active_zones", None)
    if active_zones is None:
        active_zones = req.area_polygons or ([req.area_polygon] if req.area_polygon else [])

    common = dict(
        no_fly_zones=req.no_fly_zones,
        airspace_boundary=req.airspace_boundary,
        reserve_landing_areas=req.reserve_landing_areas,
        uavs=uav_list,
        payload_type=req.payload_type,
        altitude_m=req.altitude_m,
        overlap_side=req.overlap_side,
        overlap_front=req.overlap_front,
        wind_speed_ms=req.wind_speed_ms,
        wind_dir_deg=req.wind_dir_deg,
        optimization=optimization,
    )

    if not active_zones:
        raise HTTPException(400, "area_polygon или area_polygons: минимум 1 зона с 3+ точками")
    if len(active_zones) > 1:
        missions = allocate_multi_zone(
            area_polygons=active_zones,
            startup_cost_min=req.startup_cost_min,
            **common,
        )
    else:
        missions = allocate_missions(area_polygon=active_zones[0], **common)

    for m in missions:
        m.pop("sub_polygon", None)
    return missions


def _make_summary(missions: list[dict], optimization: str) -> dict:
    total_area = sum(m.get("metrics", {}).get("area_km2", 0) for m in missions)
    total_photos = sum(m.get("metrics", {}).get("photo_count", 0) for m in missions)
    return {
        "total_uavs": len(missions),
        "optimization": optimization,
        "max_mission_time_min": max((m["stats"]["time_s"] / 60 for m in missions), default=0),
        "total_distance_km": sum(m["stats"]["distance_m"] for m in missions) / 1000,
        "total_area_km2": round(total_area, 3),
        "total_photos": total_photos,
        "missions": [
            {
                "uav": m["uav_name"],
                "uav_id": m["uav_id"],
                "uav_type": m.get("uav_type", ""),
                "takeoff_type": m.get("takeoff_type", ""),
                "landing_type": m.get("landing_type", ""),
                "distance_km": round(m["stats"]["distance_m"] / 1000, 2),
                "time_min": round(m["stats"]["time_s"] / 60, 1),
                "waypoint_count": len(m["waypoints"]),
                "warning": m["stats"].get("warning"),
                # Coverage metrics
                "area_km2": m.get("metrics", {}).get("area_km2", 0),
                "gsd_cm": m.get("metrics", {}).get("gsd_cm", 0),
                "strip_count": m.get("metrics", {}).get("strip_count", 0),
                "photo_count": m.get("metrics", {}).get("photo_count", 0),
                "swath_m": m.get("metrics", {}).get("swath_m", 0),
                "photo_interval_m": m.get("metrics", {}).get("photo_interval_m", 0),
                "altitude_m": m.get("altitude_m", 0),
                "cost_rub_est": round(m["stats"]["time_s"] / 3600 * {
                    "geoscan_201": 18000, "geoscan_401": 25000,
                    "geoscan_801": 12000, "geoscan_gemini": 8000,
                }.get(m["uav_id"], 15000)),
                "start_latlon": m.get("start_latlon"),
                "land_latlon": m.get("land_latlon"),
                "assigned_zones": m.get("assigned_zones"),
                "n_zones": m.get("n_zones", 1),
                "cruise_count": sum(1 for w in m["waypoints"] if w["action"] == "cruise"),
                "survey_pct": m["stats"].get("survey_pct", 0),
                "wind_power_factor": m["stats"].get("wind_power_factor", 1.0),
                "strip_angle_deg": m.get("strip_angle_deg"),
            }
            for m in missions
        ],
    }


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.get("/api/payloads")
def get_payloads():
    return PAYLOAD_SPECS


@app.get("/api/uavs")
def get_uavs():
    return [
        {
            "id": v.id, "name": v.name, "type": v.type,
            "max_flight_time_min": v.max_flight_time_min,
            "cruise_speed_ms": v.cruise_speed_ms,
            "max_wind_ms": v.max_wind_ms,
            "max_altitude_agl_m": v.max_altitude_agl_m,
            "supported_payloads": v.supported_payloads,
            "takeoff_type": v.takeoff_type,
            "landing_type": v.landing_type,
            "focal_mm": v.default_focal_mm,
            "sensor_w_mm": v.default_sensor_w_mm,
            "sensor_h_mm": v.default_sensor_h_mm,
            "max_range_km": v.max_range_km,
        }
        for v in UAV_FLEET.values()
    ]


@app.post("/api/plan", response_model=PlanResponse)
def plan_missions(req: PlanRequest):
    # Resolve active zones list
    if req.area_polygons and len(req.area_polygons) >= 1:
        active_zones = req.area_polygons
    elif req.area_polygon and len(req.area_polygon) >= 3:
        active_zones = [req.area_polygon]
    else:
        raise HTTPException(400, "area_polygon или area_polygons: минимум 1 зона с 3+ точками")
    req._active_zones = active_zones  # type: ignore[attr-defined]

    uav_list = _validate_and_build_uav_list(req)

    if req.optimization == "both":
        missions_mt = _run_missions(req, uav_list, "min_time")
        missions_mw = _run_missions(req, uav_list, "min_wear")

        gj_mt = missions_to_geojson(missions_mt)
        gj_mw = missions_to_geojson(missions_mw)

        summary_mt = _make_summary(missions_mt, "min_time")
        summary_mw = _make_summary(missions_mw, "min_wear")

        def _total_hours(missions):
            return sum(m["stats"]["time_s"] for m in missions) / 3600

        def _effective_cost_min(missions, startup_min):
            flight_min = sum(m["stats"]["time_s"] for m in missions) / 60
            return round(flight_min + len(missions) * startup_min, 1)

        comparison = {
            "min_time": {
                "max_mission_time_min": round(summary_mt["max_mission_time_min"], 1),
                "total_distance_km": round(summary_mt["total_distance_km"], 2),
                "total_flight_hours": round(_total_hours(missions_mt), 2),
                "effective_cost_min": _effective_cost_min(missions_mt, req.startup_cost_min),
                "n_uavs": len(missions_mt),
            },
            "min_wear": {
                "max_mission_time_min": round(summary_mw["max_mission_time_min"], 1),
                "total_distance_km": round(summary_mw["total_distance_km"], 2),
                "total_flight_hours": round(_total_hours(missions_mw), 2),
                "effective_cost_min": _effective_cost_min(missions_mw, req.startup_cost_min),
                "n_uavs": len(missions_mw),
            },
            "startup_cost_min": req.startup_cost_min,
        }

        return PlanResponse(
            missions=missions_mt,
            geojson=gj_mt,
            summary=summary_mt,
            missions_min_time=missions_mt,
            missions_min_flight=missions_mw,
            geojson_min_time=gj_mt,
            geojson_min_flight=gj_mw,
            comparison=comparison,
        )
    else:
        missions = _run_missions(req, uav_list, req.optimization)
        geojson = missions_to_geojson(missions)
        summary = _make_summary(missions, req.optimization)
        return PlanResponse(missions=missions, geojson=geojson, summary=summary)


@app.post("/api/export/kml")
def export_kml(req: PlanRequest):
    uav_list = _validate_and_build_uav_list(req)
    opt = req.optimization if req.optimization not in ("both", "min_flight") else "min_time"
    missions = _run_missions(req, uav_list, opt)
    kml_str = missions_to_kml(missions)
    return Response(
        content=kml_str,
        media_type="application/vnd.google-earth.kml+xml",
        headers={"Content-Disposition": 'attachment; filename="flight_plan.kml"'},
    )


@app.post("/api/export/geojson")
def export_geojson(req: PlanRequest):
    uav_list = _validate_and_build_uav_list(req)
    opt = req.optimization if req.optimization not in ("both", "min_flight") else "min_time"
    missions = _run_missions(req, uav_list, opt)
    geojson = missions_to_geojson(missions)
    return Response(
        content=json.dumps(geojson, ensure_ascii=False, indent=2),
        media_type="application/geo+json",
        headers={"Content-Disposition": 'attachment; filename="flight_plan.geojson"'},
    )


# Serve frontend
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {"message": "Frontend not found."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
