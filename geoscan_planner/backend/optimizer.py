"""
Multi-UAV task allocation.

min_time  : Minimize max(mission_time). Proportional area split by UAV capacity
            (speed × endurance). Faster/longer UAV gets larger sector.

min_wear  : Minimize sum(flight_time) + n_deployed × startup_cost.
            Equal-area sectors, then assign nearest to each UAV start point.

allocate_multi_zone: Assign N disjoint survey zones to M UAVs (LPT heuristic).
"""
import math
from itertools import permutations
from typing import Any, Optional

from shapely.affinity import rotate as affine_rotate
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union

from coverage import compute_coverage_strips, estimate_stats, swath_width, photo_interval, EARTH_R, _add_nfz_detours
from uav_specs import UAVSpec


# ─── Geometry helpers ─────────────────────────────────────────────────────────

def _poly_to_xy(polygon_latlon: list[list[float]]) -> tuple[Polygon, float, float]:
    olat, olon = polygon_latlon[0]
    def to_xy(pt):
        x = math.radians(pt[1] - olon) * EARTH_R * math.cos(math.radians(olat))
        y = math.radians(pt[0] - olat) * EARTH_R
        return x, y
    return Polygon([to_xy(p) for p in polygon_latlon]), olat, olon


def _xy_to_ll(x: float, y: float, olat: float, olon: float) -> list[float]:
    return [
        olat + math.degrees(y / EARTH_R),
        olon + math.degrees(x / (EARTH_R * math.cos(math.radians(olat)))),
    ]


def _area_sq_km(polygon_latlon: list[list[float]]) -> float:
    if len(polygon_latlon) < 3:
        return 0.0
    poly, _, _ = _poly_to_xy(polygon_latlon)
    return poly.area / 1e6


def _dist_m(a: list[float], b: list[float]) -> float:
    dlat = math.radians(b[0] - a[0])
    dlon = math.radians(b[1] - a[1])
    mlat = math.radians((a[0] + b[0]) / 2)
    return math.sqrt((dlat * EARTH_R) ** 2 + (dlon * EARTH_R * math.cos(mlat)) ** 2)


# ─── Area splitting ───────────────────────────────────────────────────────────

def _split_proportional(
    area_polygon: list[list[float]],
    fractions: list[float],
) -> list[list[list[float]]]:
    """Split polygon into len(fractions) sub-polygons along Y axis with given proportions."""
    n = len(fractions)
    if n <= 1:
        return [area_polygon]

    poly, olat, olon = _poly_to_xy(area_polygon)
    minx, miny, maxx, maxy = poly.bounds
    height = maxy - miny

    def to_ll(x, y): return _xy_to_ll(x, y, olat, olon)

    cum = 0.0
    slices = []
    for i, frac in enumerate(fractions):
        y0 = miny + cum * height
        cum += frac
        y1 = miny + cum * height + (1 if i < n - 1 else 0)
        slab = Polygon([(minx - 1, y0), (maxx + 1, y0), (maxx + 1, y1), (minx - 1, y1)])
        sub = poly.intersection(slab)
        if sub.is_empty or sub.area < 1:
            continue
        if sub.geom_type == "Polygon":
            slices.append([to_ll(x, y) for x, y in sub.exterior.coords])
        elif sub.geom_type == "MultiPolygon":
            largest = max(sub.geoms, key=lambda g: g.area)
            slices.append([to_ll(x, y) for x, y in largest.exterior.coords])

    while len(slices) < n:
        slices.append(slices[-1])
    return slices[:n]


def _assign_nearest(
    sub_polys: list[list[list[float]]],
    start_points: list[list[float]],
) -> list[int]:
    """Assign sub_polys to UAVs to minimize total transit distance. Greedy O(n²)."""
    n = len(sub_polys)
    if n > 8:
        # Greedy nearest
        assigned = [-1] * n
        used_uav = set()
        for poly_idx in range(n):
            centroid = _poly_centroid(sub_polys[poly_idx])
            best_uav = min(
                (u for u in range(n) if u not in used_uav),
                key=lambda u: _dist_m(start_points[u], centroid),
            )
            assigned[poly_idx] = best_uav
            used_uav.add(best_uav)
        return assigned

    # Exact: try all permutations for small n
    best_cost = float('inf')
    best_perm = list(range(n))
    centroids = [_poly_centroid(p) for p in sub_polys]
    for perm in permutations(range(n)):
        cost = sum(_dist_m(start_points[perm[i]], centroids[i]) for i in range(n))
        if cost < best_cost:
            best_cost = cost
            best_perm = list(perm)
    # best_perm[i] = UAV index for sub_poly[i]
    # We want: for each UAV, which sub_poly?
    result = [0] * n
    for poly_idx, uav_idx in enumerate(best_perm):
        result[poly_idx] = uav_idx
    return result


def _poly_centroid(poly_latlon: list[list[float]]) -> list[float]:
    lats = [p[0] for p in poly_latlon]
    lons = [p[1] for p in poly_latlon]
    return [sum(lats) / len(lats), sum(lons) / len(lons)]


def _optimal_strip_angle(zone_polygon: list[list[float]], wind_deg: float, wind_ms: float) -> float:
    """Strip angle that aligns coverage strips with the polygon's long axis (fewer turns).
    For strong wind (>= 6 m/s), overrides to wind-perpendicular to reduce crosswind drift."""
    if wind_ms >= 6.0:
        return (wind_deg + 90) % 180
    try:
        poly, _olat, _olon = _poly_to_xy(zone_polygon)
        mrr = poly.minimum_rotated_rectangle
        coords = list(mrr.exterior.coords)
        dx0, dy0 = coords[1][0] - coords[0][0], coords[1][1] - coords[0][1]
        dx1, dy1 = coords[2][0] - coords[1][0], coords[2][1] - coords[1][1]
        len0, len1 = math.hypot(dx0, dy0), math.hypot(dx1, dy1)
        if len0 >= len1:
            return math.degrees(math.atan2(dy0, dx0)) % 180
        else:
            return math.degrees(math.atan2(dy1, dx1)) % 180
    except Exception:
        return (wind_deg + 90) % 180


# ─── Flight phase tagging ─────────────────────────────────────────────────────

def _add_phases(waypoints: list[dict]) -> list[dict]:
    survey_actions = {"survey_start", "survey_end", "photo"}
    result = []
    survey_open = False

    for wp in waypoints:
        wp = dict(wp)
        action = wp["action"]
        if action == "takeoff":
            wp["phase"] = "TAKEOFF"
        elif action == "land":
            wp["phase"] = "LAND"
        elif action in survey_actions:
            if not survey_open:
                survey_open = True
                wp["phase"] = "SURVEY_START"
            else:
                wp["phase"] = "SURVEY"
        else:
            wp["phase"] = "CRUISE"
        result.append(wp)

    for i in range(len(result) - 1, -1, -1):
        if result[i]["action"] in survey_actions:
            result[i]["phase"] = "SURVEY_END"
            break

    # RTL before land
    for i in range(len(result) - 1, -1, -1):
        if result[i]["action"] == "land" and i > 0:
            result.insert(i, {
                **result[i],
                "alt_m": result[i - 1].get("alt_m", 50),
                "action": "rtl",
                "phase": "RTL",
                "strip_id": -1,
            })
            break

    return result


# ─── Per-mission metrics ──────────────────────────────────────────────────────

def _mission_metrics(
    sub_polygon: list[list[float]],
    altitude_m: float,
    focal_mm: float,
    sensor_w_mm: float,
    sensor_h_mm: float,
    overlap_side: float,
    overlap_front: float,
    waypoints: list[dict],
) -> dict:
    area_km2 = _area_sq_km(sub_polygon)
    sw = swath_width(altitude_m, focal_mm, sensor_w_mm, overlap_side)
    pi = photo_interval(altitude_m, focal_mm, sensor_h_mm, overlap_front)
    # GSD in cm/pixel (assume 24MP equivalent = 6000×4000 = 24M, sensor_h proportional)
    gsd_h = (sensor_h_mm / focal_mm) * altitude_m / 4000 * 100  # cm/px height
    gsd_w = (sensor_w_mm / focal_mm) * altitude_m / 6000 * 100
    gsd_cm = round((gsd_h + gsd_w) / 2, 1)

    nav_wps = [wp for wp in waypoints if wp["action"] == "survey_start"]
    strip_count = len(nav_wps)
    photo_wps = [wp for wp in waypoints if wp["action"] == "photo"]
    photo_count = len(photo_wps)

    trigger_s = pi  # photo_interval returns meters between shots
    # convert to seconds at cruise speed (estimated; speed comes from spec via waypoints)
    # pi is in meters, so trigger_interval_s = pi / cruise_speed
    return {
        "area_km2": round(area_km2, 3),
        "swath_m": round(sw, 1),
        "gsd_cm": gsd_cm,
        "strip_count": strip_count,
        "photo_count": photo_count,
        "photo_interval_m": round(pi, 1),
    }


# ─── Main entry ───────────────────────────────────────────────────────────────

def allocate_missions(
    area_polygon: list[list[float]],
    no_fly_zones: list[list[list[float]]],
    airspace_boundary: Optional[list[list[float]]],
    reserve_landing_areas: list[list[float]],
    uavs: list[dict],
    payload_type: str,
    altitude_m: float,
    overlap_side: float,
    overlap_front: float,
    wind_speed_ms: float,
    wind_dir_deg: float,
    optimization: str = "min_time",
) -> list[dict[str, Any]]:
    """
    Returns list of per-UAV missions.
    optimization: "min_time" | "min_flight"
    """
    n = len(uavs)
    if n == 0:
        return []

    strip_angle = _optimal_strip_angle(area_polygon, wind_dir_deg, wind_speed_ms)

    # ── Compute allocation fractions ──────────────────────────────────────────
    capacities = [u["spec"].max_flight_time_min * u["spec"].cruise_speed_ms for u in uavs]
    total_cap = sum(capacities)

    if optimization == "min_time":
        # Proportional to capacity (speed × endurance) → equalize mission completion time
        fractions = [c / total_cap for c in capacities]
        sub_polys = _split_proportional(area_polygon, fractions)
        assignment = list(range(n))
    else:
        # min_wear: minimize sum of total flight hours across all UAVs.
        # Equal area per UAV → the slowest UAV dominates total hours.
        # Instead: weight by speed only (not endurance) so faster UAVs
        # cover more area → fewer total hours = less wear.
        speeds = [u["spec"].cruise_speed_ms for u in uavs]
        total_speed = sum(speeds)
        fractions = [s / total_speed for s in speeds]
        sub_polys = _split_proportional(area_polygon, fractions)
        # Then assign nearest sub-polygon to each UAV's start point
        start_points = [u["start_latlon"] for u in uavs]
        poly_to_uav = _assign_nearest(sub_polys, start_points)
        assignment = [0] * n
        for poly_idx, uav_idx in enumerate(poly_to_uav):
            assignment[uav_idx] = poly_idx

    # ── Build missions ────────────────────────────────────────────────────────
    missions = []
    for uav_idx, u in enumerate(uavs):
        spec: UAVSpec = u["spec"]
        poly = sub_polys[assignment[uav_idx]]
        # Altitude deconfliction: each UAV gets base + index*10 m
        uav_altitude = altitude_m + uav_idx * 10 if n > 1 else altitude_m

        wps = compute_coverage_strips(
            area_polygon=poly,
            no_fly_zones=no_fly_zones,
            airspace_boundary=airspace_boundary,
            altitude_m=uav_altitude,
            focal_mm=spec.default_focal_mm,
            sensor_w_mm=spec.default_sensor_w_mm,
            sensor_h_mm=spec.default_sensor_h_mm,
            overlap_side=overlap_side,
            overlap_front=overlap_front,
            strip_angle_deg=strip_angle,
            uav_type=spec.type,
        )

        start = u.get("start_latlon") or (poly[0] if poly else [0, 0])
        land = u.get("land_latlon") or start

        full_wps = [
            {"lat": start[0], "lon": start[1], "alt_m": 0, "action": "takeoff", "strip_id": -1},
            *wps,
            {"lat": land[0], "lon": land[1], "alt_m": 0, "action": "land", "strip_id": -1},
        ]
        full_wps = _add_phases(full_wps)

        stats = estimate_stats(full_wps, speed_ms=spec.cruise_speed_ms, wind_ms=wind_speed_ms)
        effective_time_s = stats["time_s"] * stats.get("wind_power_factor", 1.0)
        if effective_time_s > spec.max_flight_time_min * 60 * 0.85:
            stats["warning"] = "exceeds_battery"

        metrics = _mission_metrics(
            sub_polygon=poly,
            altitude_m=uav_altitude,
            focal_mm=spec.default_focal_mm,
            sensor_w_mm=spec.default_sensor_w_mm,
            sensor_h_mm=spec.default_sensor_h_mm,
            overlap_side=overlap_side,
            overlap_front=overlap_front,
            waypoints=full_wps,
        )

        missions.append({
            "uav_id": spec.id,
            "uav_name": spec.name,
            "uav_type": spec.type,
            "takeoff_type": spec.takeoff_type,
            "landing_type": spec.landing_type,
            "altitude_m": uav_altitude,
            "strip_angle_deg": strip_angle,
            "waypoints": full_wps,
            "stats": stats,
            "metrics": metrics,
            "start_latlon": start,
            "land_latlon": land,
            "sub_polygon": poly,
            "reserve_landing_areas": reserve_landing_areas,
        })

    return missions


# ─── Zone-time estimator ──────────────────────────────────────────────────────

def _estimate_zone_time(
    zone_polygon: list[list[float]],
    spec,
    altitude_m: float,
    overlap_side: float,
    overlap_front: float,
    strip_angle_deg: float,
    no_fly_zones: list,
    airspace_boundary: Optional[list],
) -> float:
    """Estimate survey flight time in seconds (no actual waypoints generated)."""
    sw = swath_width(altitude_m, spec.default_focal_mm, spec.default_sensor_w_mm, overlap_side)
    if sw <= 0:
        return 0.0
    olat, olon = zone_polygon[0][0], zone_polygon[0][1]

    def to_xy(pt):
        x = math.radians(pt[1] - olon) * EARTH_R * math.cos(math.radians(olat))
        y = math.radians(pt[0] - olat) * EARTH_R
        return x, y

    try:
        poly = Polygon([to_xy(p) for p in zone_polygon])
        if airspace_boundary and len(airspace_boundary) >= 3:
            poly = poly.intersection(Polygon([to_xy(p) for p in airspace_boundary]))
        if no_fly_zones:
            nfz_u = unary_union([Polygon([to_xy(p) for p in nfz]) for nfz in no_fly_zones if len(nfz) >= 3])
            poly = poly.difference(nfz_u)
        if poly.is_empty:
            return 0.0
        rotated = affine_rotate(poly, -strip_angle_deg, origin=(0, 0))
        minx, miny, maxx, maxy = rotated.bounds
        n_strips = max(1, math.ceil((maxy - miny) / sw))
        total_dist = n_strips * (maxx - minx + sw)
        return total_dist / spec.cruise_speed_ms
    except Exception:
        return 0.0


# ─── Multi-zone allocation ────────────────────────────────────────────────────

def allocate_multi_zone(
    area_polygons: list[list[list[float]]],
    no_fly_zones: list[list[list[float]]],
    airspace_boundary: Optional[list[list[float]]],
    reserve_landing_areas: list[list[float]],
    uavs: list[dict],
    payload_type: str,
    altitude_m: float,
    overlap_side: float,
    overlap_front: float,
    wind_speed_ms: float,
    wind_dir_deg: float,
    optimization: str = "min_time",
    startup_cost_min: float = 30.0,
) -> list[dict[str, Any]]:
    """
    Assign N disjoint survey zones to M UAVs.
    A UAV may cover multiple zones sequentially.
    Returns same format as allocate_missions().
    """
    n = len(uavs)
    if n == 0 or not area_polygons:
        return []

    n_zones = len(area_polygons)

    # Pre-compute optimal strip angle per zone
    zone_angles = [_optimal_strip_angle(z, wind_dir_deg, wind_speed_ms) for z in area_polygons]

    # ── Estimate zone-time matrix ─────────────────────────────────────────────
    zone_est: list[list[float]] = []
    for z_idx, z_poly in enumerate(area_polygons):
        row = []
        for uav_idx, u in enumerate(uavs):
            spec: UAVSpec = u["spec"]
            uav_alt = altitude_m + uav_idx * 10 if n > 1 else altitude_m
            t = _estimate_zone_time(
                z_poly, spec, uav_alt, overlap_side, overlap_front,
                zone_angles[z_idx], no_fly_zones, airspace_boundary,
            )
            row.append(t)
        zone_est.append(row)

    # ── Assign zones to UAVs (LPT greedy) ────────────────────────────────────
    loads = [0.0] * n
    uav_zones: list[list[int]] = [[] for _ in range(n)]

    zone_order = sorted(range(n_zones), key=lambda z: max(zone_est[z]), reverse=True)

    for z in zone_order:
        if optimization == "min_time":
            best = min(range(n), key=lambda u: loads[u] + zone_est[z][u])
        else:
            centroid = _poly_centroid(area_polygons[z])
            starts = [u.get("start_latlon") or centroid for u in uavs]
            def cost_w(u, _z=z, _c=centroid, _starts=starts):
                transit = _dist_m(_starts[u], _c) / max(1, uavs[u]["spec"].cruise_speed_ms)
                return loads[u] + zone_est[_z][u] + transit
            best = min(range(n), key=cost_w)
        uav_zones[best].append(z)
        loads[best] += zone_est[z][best]

    # ── Build missions ────────────────────────────────────────────────────────
    missions = []
    for uav_idx, u in enumerate(uavs):
        spec: UAVSpec = u["spec"]
        uav_alt = altitude_m + uav_idx * 10 if n > 1 else altitude_m
        assigned = uav_zones[uav_idx]
        if not assigned:
            continue

        start = u.get("start_latlon") or area_polygons[assigned[0]][0]
        land = u.get("land_latlon") or start

        # Sort assigned zones by proximity (nearest-neighbor order)
        if len(assigned) > 1:
            current = start
            ordered: list[int] = []
            remaining = list(assigned)
            while remaining:
                nearest = min(remaining, key=lambda z: _dist_m(current, _poly_centroid(area_polygons[z])))
                ordered.append(nearest)
                current = _poly_centroid(area_polygons[nearest])
                remaining.remove(nearest)
            assigned = ordered

        all_wps: list[dict] = []
        total_area = 0.0

        for z in assigned:
            wps = compute_coverage_strips(
                area_polygon=area_polygons[z],
                no_fly_zones=no_fly_zones,
                airspace_boundary=airspace_boundary,
                altitude_m=uav_alt,
                focal_mm=spec.default_focal_mm,
                sensor_w_mm=spec.default_sensor_w_mm,
                sensor_h_mm=spec.default_sensor_h_mm,
                overlap_side=overlap_side,
                overlap_front=overlap_front,
                strip_angle_deg=zone_angles[z],
                uav_type=spec.type,
            )
            all_wps.extend(wps)
            total_area += _area_sq_km(area_polygons[z])

        # Add NFZ detours for inter-zone transitions (the seam between two zones)
        if no_fly_zones and len(assigned) > 1:
            from shapely.geometry import Polygon as ShapelyPolygon
            from shapely.ops import unary_union as _unary_union
            olat0, olon0 = area_polygons[assigned[0]][0]
            def _to_xy_local(pt):
                x = math.radians(pt[1] - olon0) * EARTH_R * math.cos(math.radians(olat0))
                y = math.radians(pt[0] - olat0) * EARTH_R
                return x, y
            nfz_list = [ShapelyPolygon([_to_xy_local(p) for p in nfz]) for nfz in no_fly_zones if len(nfz) >= 3]
            if nfz_list:
                nfz_union = _unary_union(nfz_list)
                all_wps = _add_nfz_detours(all_wps, nfz_union, olat0, olon0, uav_alt)

        full_wps = [
            {"lat": start[0], "lon": start[1], "alt_m": 0, "action": "takeoff", "strip_id": -1},
            *all_wps,
            {"lat": land[0], "lon": land[1], "alt_m": 0, "action": "land", "strip_id": -1},
        ]
        full_wps = _add_phases(full_wps)

        stats = estimate_stats(full_wps, speed_ms=spec.cruise_speed_ms, wind_ms=wind_speed_ms)
        effective_time_s = stats["time_s"] * stats.get("wind_power_factor", 1.0)
        if effective_time_s > spec.max_flight_time_min * 60 * 0.85:
            stats["warning"] = "exceeds_battery"

        first_zone_poly = area_polygons[assigned[0]]
        metrics = _mission_metrics(
            sub_polygon=first_zone_poly,
            altitude_m=uav_alt,
            focal_mm=spec.default_focal_mm,
            sensor_w_mm=spec.default_sensor_w_mm,
            sensor_h_mm=spec.default_sensor_h_mm,
            overlap_side=overlap_side,
            overlap_front=overlap_front,
            waypoints=full_wps,
        )
        metrics["area_km2"] = round(total_area, 3)
        metrics["assigned_zones"] = assigned

        missions.append({
            "uav_id": spec.id,
            "uav_name": spec.name,
            "uav_type": spec.type,
            "takeoff_type": spec.takeoff_type,
            "landing_type": spec.landing_type,
            "altitude_m": uav_alt,
            "strip_angle_deg": zone_angles[assigned[0]] if assigned else 0,
            "waypoints": full_wps,
            "stats": stats,
            "metrics": metrics,
            "start_latlon": start,
            "land_latlon": land,
            "sub_polygon": first_zone_poly,
            "reserve_landing_areas": reserve_landing_areas,
            "assigned_zones": assigned,
            "n_zones": len(assigned),
        })

    return missions
