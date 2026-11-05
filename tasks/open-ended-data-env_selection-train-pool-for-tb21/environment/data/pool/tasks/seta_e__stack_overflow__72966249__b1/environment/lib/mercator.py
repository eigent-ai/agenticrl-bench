# lib/mercator.py
import math

ZOOM = 4
MAP_SIZE = 256 * (2 ** ZOOM)  # 4096 pixels


def latlng_to_pixel(lat_deg, lng_deg, zoom=ZOOM):
    """Forward transform: geographic coordinates -> map pixel coordinates."""
    n = 2 ** zoom
    px = (lng_deg + 180.0) / 360.0 * n * 256
    lat_rad = math.radians(lat_deg)
    py = (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n * 256
    return (round(px, 5), round(py, 5))


def pixel_to_latlng(px, py, zoom=ZOOM):
    """Inverse transform: map pixel coordinates -> geographic coordinates."""
    n = 2 ** zoom
    lng_deg = px / (n * 256) * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (2 * py / (n * 256) - 1)))
    lat_deg = math.degrees(lat_rad)
    return (round(lat_deg, 5), round(lng_deg, 5))
