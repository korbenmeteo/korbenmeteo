from __future__ import annotations

import json
from pathlib import Path

from app.models import PointOfInterest


DEFAULT_CONFIG_PATH = Path("config/points.json")


def load_points(config_path: Path = DEFAULT_CONFIG_PATH) -> list[PointOfInterest]:
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    return [
        PointOfInterest(
            name=item["name"],
            latitude=float(item["latitude"]),
            longitude=float(item["longitude"]),
            country_code=item["country_code"],
        )
        for item in raw["points"]
    ]
