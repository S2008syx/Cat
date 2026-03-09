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


# === [FALLBACK] 离线城市数据降级方案 ===
# 当 AMAP_API_KEY 未设置或高德 API 请求失败时，使用本地 cities_db.py
# 提供基础的中国城市搜索和地理编码。
# 如果部署环境始终有 API key，以下代码和 cities_db.py 可安全删除。

from .cities_db import CITIES as _ALL_CITIES

_CHINA_CITIES = [c for c in _ALL_CITIES if c.get("country") == "CN"]


def _city_to_result(city: dict) -> dict:
    return {
        "name": city["name"],
        "address": "",
        "district": city.get("province", ""),
        "location": f"{city['lng']},{city['lat']}",
        "utc_offset": city.get("utc_offset", 8),
    }


def _fallback_search(query: str) -> list[dict]:
    """Search Chinese cities when no API key."""
    results = []
    for city in _CHINA_CITIES:
        if query in city["name"] or query in city.get("province", "") or query in city.get("name_en", "").lower():
            results.append(_city_to_result(city))
            if len(results) >= 10:
                break
    return results


def _fallback_geocode(address: str) -> dict | None:
    """Geocode from Chinese cities when no API key."""
    for city in _CHINA_CITIES:
        if city["name"] in address or address in city["name"]:
            return {
                "longitude": city["lng"],
                "latitude": city["lat"],
                "utc_offset": city["utc_offset"],
                "formatted_address": city.get("province", "") + city["name"],
            }
    return None
