"""
FastAPI backend for Human Design chart calculation.

Real pipeline: UserData → Calculator → Converters → JSON response.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

from typing import Optional

from .user_data import local_to_utc
from .geocode import search_places, geocode
from hd_calculator import calculate, calculate_transit, calculate_solar_return
from hd_converters import convert_graph, convert_words
from hd_converters.chart_image import generate_chart_svg

app = FastAPI(title="Human Design Chart API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

    graph_dict = graph_data.to_dict()
    words_dict = words_data.to_dict()

    # Generate inline SVG for the chart image
    chart_svg = generate_chart_svg(
        graph_data=graph_dict,
        words_data=words_dict,
        name=req.name,
        birth_info=f"{req.birth_date} {req.birth_time}",
    )

    return {
        "input": {
            "name": req.name,
            "birth_date": req.birth_date,
            "birth_time": req.birth_time,
            "longitude": req.longitude,
            "latitude": req.latitude,
            "utc_offset": req.utc_offset,
        },
        "graph": graph_dict,
        "words": words_dict,
        "chart_svg": chart_svg,
    }


@app.post("/api/chart/image")
def get_chart_image(req: ChartRequest):
    """Generate bodygraph SVG image. Returns image/svg+xml."""
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

    graph_dict = convert_graph(calc_output).to_dict()
    words_dict = convert_words(calc_output).to_dict()

    svg = generate_chart_svg(
        graph_data=graph_dict,
        words_data=words_dict,
        name=req.name,
        birth_info=f"{req.birth_date} {req.birth_time}",
    )
    return Response(content=svg, media_type="image/svg+xml")


class TransitRequest(BaseModel):
    transit_date: str       # "YYYY-MM-DD"
    transit_time: str       # "HH:MM"
    utc_offset: float = 8.0
    # Optional: overlay onto a natal chart
    natal_birth_date: Optional[str] = None
    natal_birth_time: Optional[str] = None
    natal_longitude: Optional[float] = None
    natal_latitude: Optional[float] = None
    natal_utc_offset: float = 8.0


@app.post("/api/transit")
def get_transit(req: TransitRequest):
    """Calculate planetary transit for a given moment, optionally overlaid on a natal chart."""
    try:
        transit_utc = local_to_utc(req.transit_date, req.transit_time, req.utc_offset)
    except (ValueError, OverflowError) as e:
        raise HTTPException(status_code=400, detail=f"流日日期时间格式错误: {e}")

    # If natal parameters are provided, compute natal chart first
    natal_gates = None
    if req.natal_birth_date and req.natal_birth_time and req.natal_longitude is not None and req.natal_latitude is not None:
        try:
            natal_utc = local_to_utc(req.natal_birth_date, req.natal_birth_time, req.natal_utc_offset)
        except (ValueError, OverflowError) as e:
            raise HTTPException(status_code=400, detail=f"本命日期时间格式错误: {e}")
        try:
            natal = calculate(birth_utc=natal_utc, latitude=req.natal_latitude, longitude=req.natal_longitude)
            natal_gates = set(natal.all_active_gates)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"本命盘计算错误: {e}")

    try:
        result = calculate_transit(transit_utc=transit_utc, natal_gates=natal_gates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"流日计算错误: {e}")

    # Serialize: convert datetime to ISO string
    serialized = {
        "transit_utc": result["transit_utc"].isoformat(),
        "activations": result["activations"],
        "active_gates": result["active_gates"],
        "transit_channels": result["transit_channels"],
        "transit_defined_centers": result["transit_defined_centers"],
    }
    if "completed_channels" in result:
        serialized["completed_channels"] = result["completed_channels"]
        serialized["overlay_defined_centers"] = result["overlay_defined_centers"]
        serialized["overlay_undefined_centers"] = result["overlay_undefined_centers"]

    return serialized


class SolarReturnRequest(BaseModel):
    name: str = ""
    birth_date: str        # "YYYY-MM-DD"
    birth_time: str        # "HH:MM"
    longitude: float
    latitude: float
    utc_offset: float = 8.0
    year: int              # Target year, e.g. 2026


@app.post("/api/solar-return")
def get_solar_return(req: SolarReturnRequest):
    """Calculate Solar Return chart for a given year."""
    try:
        birth_utc = local_to_utc(req.birth_date, req.birth_time, req.utc_offset)
    except (ValueError, OverflowError) as e:
        raise HTTPException(status_code=400, detail=f"日期时间格式错误: {e}")

    try:
        result = calculate_solar_return(
            birth_utc=birth_utc,
            year=req.year,
            latitude=req.latitude,
            longitude=req.longitude,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"太阳回归计算错误: {e}")

    chart = result["chart"]
    graph_data = convert_graph(chart)
    words_data = convert_words(chart)
    graph_dict = graph_data.to_dict()
    words_dict = words_data.to_dict()

    chart_svg = generate_chart_svg(
        graph_data=graph_dict,
        words_data=words_dict,
        name=req.name,
        birth_info=f"Solar Return {req.year}",
    )

    return {
        "input": {
            "name": req.name,
            "birth_date": req.birth_date,
            "birth_time": req.birth_time,
            "longitude": req.longitude,
            "latitude": req.latitude,
            "utc_offset": req.utc_offset,
            "year": req.year,
        },
        "return_utc": result["return_utc"].isoformat(),
        "year": result["year"],
        "graph": graph_dict,
        "words": words_dict,
        "chart_svg": chart_svg,
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


class TransitRequest(BaseModel):
    transit_date: str       # "YYYY-MM-DD"
    transit_time: str       # "HH:MM"
    utc_offset: float = 8.0
    # Optional: overlay onto a natal chart
    natal_birth_date: str | None = None
    natal_birth_time: str | None = None
    natal_longitude: float | None = None
    natal_latitude: float | None = None
    natal_utc_offset: float = 8.0


@app.post("/api/transit")
def get_transit(req: TransitRequest):
    """Calculate transit (planetary weather) activations, optionally overlaid on a natal chart."""
    try:
        transit_utc = local_to_utc(req.transit_date, req.transit_time, req.utc_offset)
    except (ValueError, OverflowError) as e:
        raise HTTPException(status_code=400, detail=f"流日日期时间格式错误: {e}")

    natal_gates: set[int] | None = None

    # If natal info provided, compute natal chart first
    if req.natal_birth_date and req.natal_birth_time and req.natal_longitude is not None and req.natal_latitude is not None:
        try:
            natal_utc = local_to_utc(req.natal_birth_date, req.natal_birth_time, req.natal_utc_offset)
        except (ValueError, OverflowError) as e:
            raise HTTPException(status_code=400, detail=f"本命日期时间格式错误: {e}")
        try:
            natal = calculate(birth_utc=natal_utc, latitude=req.natal_latitude, longitude=req.natal_longitude)
            natal_gates = set(natal.all_active_gates)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"本命盘计算错误: {e}")

    try:
        result = calculate_transit(transit_utc=transit_utc, natal_gates=natal_gates)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"流日计算错误: {e}")

    # Serialize datetime to ISO string
    result["transit_utc"] = result["transit_utc"].isoformat()
    return result


class SolarReturnRequest(BaseModel):
    name: str = ""
    birth_date: str        # "YYYY-MM-DD"
    birth_time: str        # "HH:MM"
    longitude: float
    latitude: float
    utc_offset: float = 8.0
    year: int              # Target year, e.g. 2026


@app.post("/api/solar-return")
def get_solar_return(req: SolarReturnRequest):
    """Calculate a Solar Return chart for a given year."""
    try:
        birth_utc = local_to_utc(req.birth_date, req.birth_time, req.utc_offset)
    except (ValueError, OverflowError) as e:
        raise HTTPException(status_code=400, detail=f"日期时间格式错误: {e}")

    try:
        sr_result = calculate_solar_return(
            birth_utc=birth_utc,
            year=req.year,
            latitude=req.latitude,
            longitude=req.longitude,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"太阳回归计算错误: {e}")

    chart = sr_result["chart"]
    graph_data = convert_graph(chart)
    words_data = convert_words(chart)
    graph_dict = graph_data.to_dict()
    words_dict = words_data.to_dict()

    chart_svg = generate_chart_svg(
        graph_data=graph_dict,
        words_data=words_dict,
        name=req.name,
        birth_info=f"Solar Return {req.year}",
    )

    return {
        "input": {
            "name": req.name,
            "birth_date": req.birth_date,
            "birth_time": req.birth_time,
            "longitude": req.longitude,
            "latitude": req.latitude,
            "utc_offset": req.utc_offset,
            "year": req.year,
        },
        "return_utc": sr_result["return_utc"].isoformat(),
        "year": sr_result["year"],
        "natal_sun_longitude": sr_result["natal_sun_longitude"],
        "graph": graph_dict,
        "words": words_dict,
        "chart_svg": chart_svg,
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
