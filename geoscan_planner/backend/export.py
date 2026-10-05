"""Export missions to KML and GeoJSON."""
import json
from typing import Any

import simplekml

_UAV_COLORS_KML = ["ff0000ff", "ff00ff00", "ffff0000", "ff00ffff", "ffff00ff"]
_UAV_COLORS_HEX = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#a855f7"]


def missions_to_geojson(missions: list[dict[str, Any]]) -> dict:
    features = []

    for idx, mission in enumerate(missions):
        # Route line — all nav waypoints
        route_wps = [wp for wp in mission["waypoints"]
                     if wp["action"] not in ("photo",)]
        coords = [[wp["lon"], wp["lat"], wp["alt_m"]] for wp in route_wps]
        features.append({
            "type": "Feature",
            "properties": {
                "uav_id": mission["uav_id"],
                "uav_name": mission["uav_name"],
                "distance_m": round(mission["stats"]["distance_m"], 1),
                "time_s": round(mission["stats"]["time_s"], 1),
                "warning": mission["stats"].get("warning"),
                "color_index": idx,
                "feature_type": "route",
            },
            "geometry": {"type": "LineString", "coordinates": coords},
        })

        # Photo trigger line (separate thin dashed line)
        photo_wps = [wp for wp in mission["waypoints"] if wp["action"] == "photo"]
        if photo_wps:
            ph_coords = [[wp["lon"], wp["lat"], wp["alt_m"]] for wp in photo_wps]
            features.append({
                "type": "Feature",
                "properties": {
                    "uav_id": mission["uav_id"],
                    "color_index": idx,
                    "feature_type": "photo_line",
                },
                "geometry": {"type": "MultiPoint", "coordinates": ph_coords},
            })

        # Sub-polygon
        if mission.get("sub_polygon"):
            poly_coords = [[p[1], p[0]] for p in mission["sub_polygon"]]
            if poly_coords[0] != poly_coords[-1]:
                poly_coords.append(poly_coords[0])
            features.append({
                "type": "Feature",
                "properties": {"feature_type": "sub_polygon", "uav_id": mission["uav_id"]},
                "geometry": {"type": "Polygon", "coordinates": [poly_coords]},
            })

        # Takeoff / land / RTL / cruise-detour markers
        for wp in mission["waypoints"]:
            if wp["action"] in ("takeoff", "land", "rtl", "cruise"):
                features.append({
                    "type": "Feature",
                    "properties": {
                        "uav_id": mission["uav_id"],
                        "action": wp["action"],
                        "phase": wp.get("phase", ""),
                        "color_index": idx,
                        "feature_type": "cruise_detour" if wp["action"] == "cruise" else None,
                    },
                    "geometry": {"type": "Point", "coordinates": [wp["lon"], wp["lat"], wp["alt_m"]]},
                })

        # Detour segment: orange line through cruise waypoints (one extra wp on each side)
        wps = mission["waypoints"]
        cruise_indices = [i for i, w in enumerate(wps) if w["action"] == "cruise"]
        if cruise_indices:
            groups: list[list[int]] = []
            group = [cruise_indices[0]]
            for ci in cruise_indices[1:]:
                if ci == group[-1] + 1:
                    group.append(ci)
                else:
                    groups.append(group)
                    group = [ci]
            groups.append(group)
            for g in groups:
                s = max(0, g[0] - 1)
                e = min(len(wps) - 1, g[-1] + 1)
                detour_coords = [[wps[i]["lon"], wps[i]["lat"], wps[i]["alt_m"]] for i in range(s, e + 1)]
                features.append({
                    "type": "Feature",
                    "properties": {
                        "uav_id": mission["uav_id"],
                        "feature_type": "detour_segment",
                        "color_index": idx,
                    },
                    "geometry": {"type": "LineString", "coordinates": detour_coords},
                })

        # Reserve landing areas
        for rl in mission.get("reserve_landing_areas", []):
            features.append({
                "type": "Feature",
                "properties": {"feature_type": "reserve_landing", "uav_id": mission["uav_id"]},
                "geometry": {"type": "Point", "coordinates": [rl[1], rl[0]]},
            })

    return {"type": "FeatureCollection", "features": features}


def missions_to_kml(missions: list[dict[str, Any]]) -> str:
    kml = simplekml.Kml(name="Geoscan Flight Plan")

    for idx, mission in enumerate(missions):
        folder = kml.newfolder(name=mission["uav_name"])
        color = _UAV_COLORS_KML[idx % len(_UAV_COLORS_KML)]

        # Full route (nav waypoints)
        route_wps = [wp for wp in mission["waypoints"] if wp["action"] != "photo"]
        coords = [(wp["lon"], wp["lat"], wp["alt_m"]) for wp in route_wps]
        ls = folder.newlinestring(name=f"{mission['uav_name']} маршрут", coords=coords)
        ls.altitudemode = simplekml.AltitudeMode.relativetoground
        ls.extrude = 1
        ls.style.linestyle.color = color
        ls.style.linestyle.width = 2

        # Waypoint placemarks
        for wp in route_wps:
            pm = folder.newpoint(
                name=f"{wp['action']} [{wp.get('phase','')}]",
                coords=[(wp["lon"], wp["lat"], wp["alt_m"])],
            )
            pm.altitudemode = simplekml.AltitudeMode.relativetoground
            pm.description = f"Фаза: {wp.get('phase','')}\nВысота: {wp['alt_m']} м"

        # Reserve landing areas
        rl_folder = folder.newfolder(name="Резервные площадки")
        for j, rl in enumerate(mission.get("reserve_landing_areas", []), 1):
            pm = rl_folder.newpoint(name=f"Резерв {j}", coords=[(rl[1], rl[0], 0)])
            pm.altitudemode = simplekml.AltitudeMode.relativetoground
            pm.style.iconstyle.color = "ff00ffff"

        folder.description = (
            f"Расстояние: {mission['stats']['distance_m']:.0f} м | "
            f"Время: {mission['stats']['time_s']/60:.1f} мин"
        )

    return kml.kml()
