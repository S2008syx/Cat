"""
Geocoding via 高德地图 (Amap) REST API.

Provides place search → (longitude, latitude, utc_offset).
API key is read from environment variable AMAP_API_KEY.
"""

import os
import urllib.request
import urllib.parse
import json
from math import floor

AMAP_API_KEY = os.environ.get("AMAP_API_KEY", "")

AMAP_GEOCODE_URL = "https://restapi.amap.com/v3/geocode/geo"
AMAP_INPUT_TIPS_URL = "https://restapi.amap.com/v3/assistant/inputtips"


def _utc_offset_from_longitude(lng: float) -> float:
    """Rough UTC offset from longitude (15° per hour). Good enough for most cases."""
    return round(lng / 15)


def search_places(query: str) -> list[dict]:
    """Search places using 高德 input tips API (autocomplete).

    Args:
        query: Search text, e.g. "上海" or "北京朝阳"

    Returns:
        List of place suggestions: [{"name", "address", "location", "district"}, ...]
        Each location is "lng,lat" string.
    """
    if not AMAP_API_KEY:
        return _fallback_search(query)

    params = urllib.parse.urlencode({
        "key": AMAP_API_KEY,
        "keywords": query,
        "datatype": "all",
    })
    url = f"{AMAP_INPUT_TIPS_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode())
    except Exception:
        return _fallback_search(query)

    if data.get("status") != "1":
        return _fallback_search(query)

    results = []
    for tip in data.get("tips", []):
        location = tip.get("location", "")
        if not location or not isinstance(location, str) or "," not in location:
            continue
        results.append({
            "name": tip.get("name", ""),
            "address": tip.get("address", "") if isinstance(tip.get("address"), str) else "",
            "district": tip.get("district", ""),
            "location": location,
        })

    return results[:10]


def geocode(address: str) -> dict | None:
    """Geocode an address to coordinates using 高德 geocode API.

    Args:
        address: Full or partial address string.

    Returns:
        {"longitude": float, "latitude": float, "utc_offset": float, "formatted_address": str}
        or None if not found.
    """
    if not AMAP_API_KEY:
        return _fallback_geocode(address)

    params = urllib.parse.urlencode({
        "key": AMAP_API_KEY,
        "address": address,
    })
    url = f"{AMAP_GEOCODE_URL}?{params}"

    try:
        with urllib.request.urlopen(url, timeout=5) as resp:
            data = json.loads(resp.read().decode())
    except Exception:
        return _fallback_geocode(address)

    if data.get("status") != "1":
        return _fallback_geocode(address)

    geocodes = data.get("geocodes", [])
    if not geocodes:
        return _fallback_geocode(address)

    geo = geocodes[0]
    location = geo.get("location", "")
    if "," not in location:
        return None

    lng, lat = location.split(",")
    lng_f, lat_f = float(lng), float(lat)

    return {
        "longitude": lng_f,
        "latitude": lat_f,
        "utc_offset": _utc_offset_from_longitude(lng_f),
        "formatted_address": geo.get("formatted_address", address),
    }


# === Fallback: built-in city data when no API key ===

_BUILTIN_CITIES = [
    {"name": "上海", "lng": 121.4737, "lat": 31.2304, "utc_offset": 8},
    {"name": "北京", "lng": 116.4074, "lat": 39.9042, "utc_offset": 8},
    {"name": "广州", "lng": 113.2644, "lat": 23.1291, "utc_offset": 8},
    {"name": "深圳", "lng": 114.0579, "lat": 22.5431, "utc_offset": 8},
    {"name": "成都", "lng": 104.0665, "lat": 30.5723, "utc_offset": 8},
    {"name": "杭州", "lng": 120.1551, "lat": 30.2741, "utc_offset": 8},
    {"name": "武汉", "lng": 114.3054, "lat": 30.5931, "utc_offset": 8},
    {"name": "南京", "lng": 118.7969, "lat": 32.0603, "utc_offset": 8},
    {"name": "重庆", "lng": 106.5516, "lat": 29.5630, "utc_offset": 8},
    {"name": "西安", "lng": 108.9402, "lat": 34.2611, "utc_offset": 8},
    {"name": "香港", "lng": 114.1694, "lat": 22.3193, "utc_offset": 8},
    {"name": "台北", "lng": 121.5654, "lat": 25.0330, "utc_offset": 8},
    {"name": "东京", "lng": 139.6917, "lat": 35.6895, "utc_offset": 9},
    {"name": "首尔", "lng": 126.9780, "lat": 37.5665, "utc_offset": 9},
    {"name": "纽约", "lng": -74.0060, "lat": 40.7128, "utc_offset": -5},
    {"name": "伦敦", "lng": -0.1276, "lat": 51.5074, "utc_offset": 0},
    {"name": "巴黎", "lng": 2.3522, "lat": 48.8566, "utc_offset": 1},
    {"name": "悉尼", "lng": 151.2093, "lat": -33.8688, "utc_offset": 10},
    {"name": "洛杉矶", "lng": -118.2437, "lat": 34.0522, "utc_offset": -8},
    {"name": "新加坡", "lng": 103.8198, "lat": 1.3521, "utc_offset": 8},
]


def _fallback_search(query: str) -> list[dict]:
    """Search built-in cities when no API key."""
    results = []
    for city in _BUILTIN_CITIES:
        if query in city["name"]:
            results.append({
                "name": city["name"],
                "address": "",
                "district": "",
                "location": f"{city['lng']},{city['lat']}",
            })
    return results if results else [
        {
            "name": c["name"],
            "address": "",
            "district": "",
            "location": f"{c['lng']},{c['lat']}",
        }
        for c in _BUILTIN_CITIES[:5]
    ]


def _fallback_geocode(address: str) -> dict | None:
    """Geocode from built-in cities when no API key."""
    for city in _BUILTIN_CITIES:
        if city["name"] in address or address in city["name"]:
            return {
                "longitude": city["lng"],
                "latitude": city["lat"],
                "utc_offset": city["utc_offset"],
                "formatted_address": city["name"],
            }
    return None
