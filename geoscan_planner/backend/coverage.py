"""
Coverage path planning.
Boustrophedon (lawn-mower) for fixed-wing; grid with hover points for multirotor.
All coordinates in lat/lon. Local XY in metres for geometry ops.
"""
import math
from typing import Any, Optional

from shapely.affinity import rotate as affine_rotate
from shapely.geometry import LineString, MultiPolygon, Point, Polygon
from shapely.ops import unary_union

EARTH_R = 6_371_000.0


# ── Coordinate helpers ────────────────────────────────────────────────────────

def _to_xy(lat, lon, olat, olon):
    x = math.radians(lon - olon) * EARTH_R * math.cos(math.radians(olat))
    y = math.radians(lat - olat) * EARTH_R
    return x, y


def _to_ll(x, y, olat, olon):
    lat = olat + math.degrees(y / EARTH_R)
    lon = olon + math.degrees(x / (EARTH_R * math.cos(math.radians(olat))))
    return lat, lon


def _rot(x, y, a):
    c, s = math.cos(a), math.sin(a)
    return x * c - y * s, x * s + y * c


def _rotate_poly(poly: Polygon, a: float) -> Polygon:
    c, s = math.cos(a), math.sin(a)
    return Polygon([(x * c - y * s, x * s + y * c) for x, y in poly.exterior.coords])


# ── Camera ────────────────────────────────────────────────────────────────────

def swath_width(alt_m: float, focal_mm: float, sensor_w_mm: float, overlap: float) -> float:
    return (sensor_w_mm / focal_mm) * alt_m * (1 - overlap)


def photo_interval(alt_m: float, focal_mm: float, sensor_h_mm: float, overlap: float) -> float:
    return (sensor_h_mm / focal_mm) * alt_m * (1 - overlap)


# ── Main entry ────────────────────────────────────────────────────────────────

def compute_coverage_strips(
    area_polygon: list[list[float]],
    no_fly_zones: list[list[list[float]]],
    airspace_boundary: Optional[list[list[float]]],
    altitude_m: float,
    focal_mm: float,
    sensor_w_mm: float,
    sensor_h_mm: float,
    overlap_side: float = 0.3,
    overlap_front: float = 0.7,
    strip_angle_deg: float = 0.0,
    uav_type: str = "fixed_wing",
) -> list[dict[str, Any]]:
    """
    Returns ordered waypoints with action labels:
      takeoff | climb | cruise | survey | photo | rtl | land
    """
    olat, olon = area_polygon[0][0], area_polygon[0][1]

    def to_xy(pt): return _to_xy(pt[0], pt[1], olat, olon)
    def to_ll(x, y): return _to_ll(x, y, olat, olon)

    poly = Polygon([to_xy(p) for p in area_polygon])

    # Clip to airspace boundary
    if airspace_boundary and len(airspace_boundary) >= 3:
        ab = Polygon([to_xy(p) for p in airspace_boundary])
        poly = poly.intersection(ab)

    # Subtract no-fly zones
    nfz_union = None
    if no_fly_zones:
        nfz_list = [Polygon([to_xy(p) for p in nfz]) for nfz in no_fly_zones if len(nfz) >= 3]
        if nfz_list:
            nfz_union = unary_union(nfz_list)
            poly = poly.difference(nfz_union)

    if poly.is_empty or poly.area < 1:
        return []

    sw = swath_width(altitude_m, focal_mm, sensor_w_mm, overlap_side)
    pi = photo_interval(altitude_m, focal_mm, sensor_h_mm, overlap_front)

    angle_rad = math.radians(strip_angle_deg)
    # affine_rotate preserves holes and handles MultiPolygon — _rotate_poly only did exterior
    rotated = affine_rotate(poly, -strip_angle_deg, origin=(0, 0))
    minx, miny, maxx, maxy = rotated.bounds

    # Build strips
    strips: list[LineString] = []
    y = miny + sw / 2
    while y <= maxy + sw / 2:
        line = LineString([(minx - sw, y), (maxx + sw, y)])
        clipped = rotated.intersection(line)
        if clipped.is_empty:
            y += sw
            continue
        if clipped.geom_type == "LineString":
            strips.append(clipped)
        elif clipped.geom_type == "MultiLineString":
            strips.extend(clipped.geoms)
        y += sw

    if not strips:
        return []

    strips.sort(key=lambda s: s.bounds[1])

    waypoints: list[dict] = []
    for i, strip in enumerate(strips):
        coords = list(strip.coords)
        if i % 2 == 1:
            coords = coords[::-1]
        rot_back = [_rot(c[0], c[1], angle_rad) for c in coords]

        # Strip start/end nav points
        for j, (x, y) in enumerate(rot_back):
            lat, lon = to_ll(x, y)
            action = "survey_start" if j == 0 else "survey_end"
            waypoints.append({"lat": lat, "lon": lon, "alt_m": altitude_m,
                              "action": action, "strip_id": i})

        # Photo trigger points along strip
        seg = LineString(rot_back)
        d = 0.0
        while d <= seg.length:
            pt = seg.interpolate(d)
            lat, lon = to_ll(pt.x, pt.y)
            waypoints.append({"lat": lat, "lon": lon, "alt_m": altitude_m,
                              "action": "photo", "strip_id": i})
            d += pi

    # Insert NFZ-avoidance waypoints on inter-strip transitions
    if nfz_union is not None:
        waypoints = _add_nfz_detours(waypoints, nfz_union, olat, olon, altitude_m)

    return _dedup(waypoints)


def _add_nfz_detours(
    waypoints: list[dict],
    nfz_union,
    olat: float,
    olon: float,
    altitude_m: float,
) -> list[dict]:
    """Insert cruise waypoints around NFZ for inter-strip transitions."""
    if nfz_union.is_empty:
        return waypoints

    # Routing waypoints placed 80 m outside the NFZ boundary
    routing_hull = nfz_union.buffer(80).convex_hull
    hull_pts = list(routing_hull.exterior.coords)[:-1]

    def xy(wp):
        return _to_xy(wp["lat"], wp["lon"], olat, olon)

    def clear(p1, p2):
        # Clear if path doesn't pass through NFZ interior
        # (endpoint touching the boundary is OK — strip endpoints sit on it)
        inter = LineString([p1, p2]).intersection(nfz_union)
        return inter.is_empty or inter.length < 0.1

    result = []
    for i, wp in enumerate(waypoints):
        result.append(wp)
        if i + 1 >= len(waypoints):
            continue
        nxt = waypoints[i + 1]
        if wp["strip_id"] == nxt["strip_id"]:
            continue  # within same strip — already clipped correctly

        p1 = xy(wp)
        p2 = xy(nxt)
        if clear(p1, p2):
            continue

        # Try 1-vertex detour via convex hull
        best1, best1_len = None, float("inf")
        for v in hull_pts:
            if clear(p1, v) and clear(v, p2):
                d = math.hypot(v[0] - p1[0], v[1] - p1[1]) + math.hypot(v[0] - p2[0], v[1] - p2[1])
                if d < best1_len:
                    best1_len, best1 = d, v

        if best1:
            lat, lon = _to_ll(best1[0], best1[1], olat, olon)
            result.append({"lat": lat, "lon": lon, "alt_m": altitude_m, "action": "cruise", "strip_id": -1})
            continue

        # Try 2-vertex detour
        best2, best2_len = None, float("inf")
        for j, v1 in enumerate(hull_pts):
            for v2 in hull_pts[j + 1:]:
                if clear(p1, v1) and clear(v1, v2) and clear(v2, p2):
                    d = (math.hypot(v1[0] - p1[0], v1[1] - p1[1]) +
                         math.hypot(v2[0] - v1[0], v2[1] - v1[1]) +
                         math.hypot(v2[0] - p2[0], v2[1] - p2[1]))
                    if d < best2_len:
                        best2_len, best2 = d, (v1, v2)

        if best2:
            for v in best2:
                lat, lon = _to_ll(v[0], v[1], olat, olon)
                result.append({"lat": lat, "lon": lon, "alt_m": altitude_m, "action": "cruise", "strip_id": -1})

    return result


def _dedup(wps: list[dict]) -> list[dict]:
    seen: set = set()
    out = []
    for wp in wps:
        if wp["action"] == "cruise":
            out.append(wp)
            continue
        k = (round(wp["lat"], 7), round(wp["lon"], 7), wp["action"])
        if k not in seen:
            seen.add(k)
            out.append(wp)
    return out


# ── Stats ─────────────────────────────────────────────────────────────────────

def estimate_stats(
    waypoints: list[dict],
    speed_ms: float,
    wind_ms: float = 0.0,
) -> dict[str, float]:
    nav = [wp for wp in waypoints
           if wp["action"] in ("takeoff", "climb", "cruise", "survey_start", "survey_end", "rtl", "land")]
    if len(nav) < 2:
        return {"distance_m": 0.0, "time_s": 0.0, "survey_dist_m": 0.0, "survey_pct": 0}

    survey_actions = {"survey_start", "survey_end"}
    total_dist = 0.0
    survey_dist = 0.0
    for i in range(1, len(nav)):
        a, b = nav[i - 1], nav[i]
        dlat = math.radians(b["lat"] - a["lat"])
        dlon = math.radians(b["lon"] - a["lon"])
        mlat = math.radians((a["lat"] + b["lat"]) / 2)
        d = math.sqrt((dlat * EARTH_R) ** 2 + (dlon * EARTH_R * math.cos(mlat)) ** 2)
        total_dist += d
        if a["action"] in survey_actions or b["action"] in survey_actions:
            survey_dist += d

    eff_speed = math.sqrt(max(0.5, speed_ms ** 2 - (min(wind_ms, speed_ms * 0.9) * 0.5) ** 2))
    survey_pct = round(survey_dist / total_dist * 100) if total_dist > 0 else 0
    # Wind power factor: aerodynamic drag model (power ~ v_air^2.5)
    power_factor = 1.0
    if wind_ms > 0 and speed_ms > 0:
        v_head = speed_ms + wind_ms
        v_tail = max(speed_ms - wind_ms, 1.0)
        power_factor = round(((v_head ** 2.5 + v_tail ** 2.5) / 2) / (speed_ms ** 2.5), 3)
    return {
        "distance_m": total_dist,
        "time_s": total_dist / eff_speed,
        "survey_dist_m": round(survey_dist, 1),
        "survey_pct": survey_pct,
        "wind_power_factor": power_factor,
    }
