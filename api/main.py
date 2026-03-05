"""
FastAPI backend for Human Design chart calculation.

Real pipeline: UserData → Calculator → Converters → JSON response.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .user_data import local_to_utc
from .geocode import search_places, geocode
from hd_calculator import calculate
from hd_converters import convert_graph, convert_words

app = FastAPI(title="Human Design Chart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChartRequest(BaseModel):
    name: str = ""
    birth_date: str  # "YYYY-MM-DD"
    birth_time: str  # "HH:MM"
    longitude: float
    latitude: float
    utc_offset: float = 8.0  # default China +8


@app.post("/api/chart")
def get_chart(req: ChartRequest):
    """Full HD chart pipeline: input → UTC → calculate → convert → JSON."""
    try:
        birth_utc = local_to_utc(req.birth_date, req.birth_time, req.utc_offset)
    except (ValueError, OverflowError) as e:
        raise HTTPException(status_code=400, detail=f"日期时间格式错误: {e}")

    try:
        calc_output = calculate(
            birth_utc=birth_utc,
            latitude=req.latitude,
            longitude=req.longitude,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"计算错误: {e}")

    graph_data = convert_graph(calc_output)
    words_data = convert_words(calc_output)

    return {
        "input": {
            "name": req.name,
            "birth_date": req.birth_date,
            "birth_time": req.birth_time,
            "longitude": req.longitude,
            "latitude": req.latitude,
            "utc_offset": req.utc_offset,
        },
        "graph": graph_data.to_dict(),
        "words": words_data.to_dict(),
    }


@app.get("/api/places")
def search(q: str = ""):
    """Search places via 高德地图 API (or built-in fallback)."""
    if not q.strip():
        return {"results": []}
    return {"results": search_places(q.strip())}


@app.get("/api/geocode")
def geocode_address(address: str = ""):
    """Geocode address → {longitude, latitude, utc_offset}."""
    if not address.strip():
        raise HTTPException(status_code=400, detail="address 参数不能为空")
    result = geocode(address.strip())
    if not result:
        raise HTTPException(status_code=404, detail=f"找不到地址: {address}")
    return result


@app.get("/api/health")
def health():
    return {"status": "ok"}
