from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UAVSpec:
    id: str
    name: str
    type: str  # "fixed_wing" | "multirotor"
    max_flight_time_min: float
    cruise_speed_ms: float          # nominal cruise speed m/s
    min_speed_ms: Optional[float]   # None for multirotors
    max_speed_ms: float
    max_wind_ms: float
    max_altitude_agl_m: float
    min_altitude_agl_m: float
    takeoff_type: str               # "catapult" | "vtol"
    landing_type: str               # "parachute" | "vtol"
    max_range_km: float
    # Camera defaults for coverage calculation
    default_focal_mm: float
    default_sensor_w_mm: float
    default_sensor_h_mm: float
    supported_payloads: list[str] = field(default_factory=list)


PAYLOAD_SPECS: dict[str, dict] = {
    "rgb": {
        "name": "Фото видимого диапазона (RGB)",
        "camera": "Sony RX1R II",
        "resolution_mp": 42.4,
        "focal_mm": 35.0,
        "sensor_mm": "35.9 × 24.0 (полный кадр)",
        "pixel_um": 4.51,
        "bands": "R / G / B",
        "gsd_150m_cm": 1.7,
        "notes": "Геопривязка через PPK/RTK",
    },
    "multispectral": {
        "name": "Мультиспектральная съёмка",
        "camera": "MicaSense RedEdge-MX",
        "resolution_mp": 1.2,
        "focal_mm": 5.5,
        "sensor_mm": "4.80 × 3.60 (1/2.9″)",
        "pixel_um": 3.75,
        "bands": "Blue 475 нм / Green 560 нм / Red 668 нм / Red-Edge 717 нм / NIR 840 нм",
        "gsd_150m_cm": 8.3,
        "notes": "5 каналов одновременно, включает датчик облучённости DLS",
    },
    "ir": {
        "name": "Инфракрасная (тепловая) съёмка",
        "camera": "FLIR Vue Pro R 640",
        "resolution_mp": 0.33,
        "focal_mm": 9.0,
        "sensor_mm": "VOx болометр 640 × 512",
        "pixel_um": 17.0,
        "bands": "LWIR 7.5 – 13.5 мкм",
        "gsd_150m_cm": 21.0,
        "notes": "Точность температуры ±5°C, RadiometricJPEG",
    },
    "lidar": {
        "name": "Лазерное сканирование (LiDAR)",
        "camera": "Velodyne VLP-16 (Puck)",
        "resolution_mp": None,
        "focal_mm": None,
        "sensor_mm": "16 каналов, ±15° верт., 360° гориз.",
        "pixel_um": None,
        "bands": "905 нм, до 100 м, 300 000 точек/с",
        "gsd_150m_cm": None,
        "notes": "Точность ±2 см (1σ), совмещается с IMU/GNSS APX-15",
    },
    "geophysical": {
        "name": "Геофизическая (магнитная) съёмка",
        "camera": "Магнитометр GSMC-02",
        "resolution_mp": None,
        "focal_mm": None,
        "sensor_mm": "Квантовый оптический, 3 оси",
        "pixel_um": None,
        "bands": "Чувствительность 0.01 нТл / Диапазон 20 000–100 000 нТл",
        "gsd_150m_cm": None,
        "notes": "Шаг сетки 10–50 м, совместно с барометром и GNSS",
    },
}

UAV_FLEET: dict[str, UAVSpec] = {
    "geoscan_201": UAVSpec(
        id="geoscan_201",
        name="Геоскан 201",
        type="fixed_wing",
        max_flight_time_min=180,
        cruise_speed_ms=25.0,      # ~90 km/h nominal
        min_speed_ms=17.8,         # 64 km/h
        max_speed_ms=36.1,         # 130 km/h
        max_wind_ms=12.0,
        max_altitude_agl_m=4000,
        min_altitude_agl_m=100,
        takeoff_type="catapult",
        landing_type="parachute",
        max_range_km=210,
        default_focal_mm=35.0,
        default_sensor_w_mm=35.9,
        default_sensor_h_mm=24.0,
        supported_payloads=["rgb", "multispectral"],
    ),
    "geoscan_gemini": UAVSpec(
        id="geoscan_gemini",
        name="Геоскан Gemini",
        type="multirotor",
        max_flight_time_min=40,
        cruise_speed_ms=10.0,      # conservative cruise
        min_speed_ms=None,
        max_speed_ms=15.0,
        max_wind_ms=10.0,
        max_altitude_agl_m=500,
        min_altitude_agl_m=20,
        takeoff_type="vtol",
        landing_type="vtol",
        max_range_km=5.0,
        default_focal_mm=20.0,
        default_sensor_w_mm=23.5,
        default_sensor_h_mm=15.6,
        supported_payloads=["rgb", "multispectral"],
    ),
    "geoscan_401": UAVSpec(
        id="geoscan_401",
        name="Геоскан 401",
        type="fixed_wing",
        max_flight_time_min=240,
        cruise_speed_ms=22.0,      # ~80 км/ч крейсерская
        min_speed_ms=15.0,
        max_speed_ms=33.3,         # 120 км/ч макс
        max_wind_ms=15.0,
        max_altitude_agl_m=5000,
        min_altitude_agl_m=100,
        takeoff_type="catapult",
        landing_type="parachute",
        max_range_km=350,
        default_focal_mm=35.0,
        default_sensor_w_mm=35.9,
        default_sensor_h_mm=24.0,
        supported_payloads=["rgb", "multispectral", "lidar", "ir"],
    ),
    "geoscan_801": UAVSpec(
        id="geoscan_801",
        name="Геоскан 801",
        type="multirotor",
        max_flight_time_min=55,    # octorotor heavy-lift class, ~55 min no payload
        cruise_speed_ms=10.0,
        min_speed_ms=None,
        max_speed_ms=15.0,
        max_wind_ms=12.0,
        max_altitude_agl_m=500,
        min_altitude_agl_m=20,
        takeoff_type="vtol",
        landing_type="vtol",
        max_range_km=8.0,
        default_focal_mm=24.0,
        default_sensor_w_mm=35.9,
        default_sensor_h_mm=24.0,
        supported_payloads=["rgb", "lidar", "multispectral", "ir", "geophysical"],
    ),
}
