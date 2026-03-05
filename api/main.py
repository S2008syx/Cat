"""
FastAPI backend for Human Design chart calculation.

Demo mode: returns mock data. Switch to real calculator later.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .mock_data import MOCK_CHART_RESPONSE

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
    """Return HD chart data. Currently returns mock data for demo."""
    # TODO: wire up real pipeline:
    #   1. user_data.local_to_utc(req.birth_date, req.birth_time, req.utc_offset)
    #   2. hd_calculator.calculate(birth_utc, req.latitude, req.longitude)
    #   3. convert_graph(output) + convert_words(output)
    return {
        "input": {
            "name": req.name,
            "birth_date": req.birth_date,
            "birth_time": req.birth_time,
            "longitude": req.longitude,
            "latitude": req.latitude,
            "utc_offset": req.utc_offset,
        },
        **MOCK_CHART_RESPONSE,
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
