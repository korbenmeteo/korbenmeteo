from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from app.model_selection import preferred_models
from app.models import PointOfInterest
from app.storage import JsonStorage


class WeatherModelService:
    def __init__(self, points: list[PointOfInterest], storage_path: Path) -> None:
        self.points = points
        self.storage = JsonStorage(storage_path)

    def refresh_all(self) -> dict[str, Any]:
        updated_at = datetime.now(timezone.utc).isoformat()
        results: list[dict[str, Any]] = []

        for point in self.points:
            results.append(self._fetch_for_point(point))

        payload = {
            "updated_at": updated_at,
            "results": results,
        }
        self.storage.write(payload)
        return payload

    def get_latest(self) -> dict[str, Any]:
        return self.storage.read()

    def _fetch_for_point(self, point: PointOfInterest) -> dict[str, Any]:
        attempted = preferred_models(point)
        errors: list[dict[str, str]] = []

        for model in attempted:
            try:
                data = self._request_open_meteo(point, model)
                return {
                    "point": asdict(point),
                    "selected_model": model,
                    "data": data,
                    "errors": errors,
                }
            except RuntimeError as exc:
                errors.append({"model": model, "error": str(exc)})

        return {
            "point": asdict(point),
            "selected_model": None,
            "data": None,
            "errors": errors,
        }

    @staticmethod
    def _request_open_meteo(point: PointOfInterest, model: str) -> dict[str, Any]:
        params = {
            "latitude": point.latitude,
            "longitude": point.longitude,
            "hourly": "temperature_2m,precipitation_probability,wind_speed_10m",
            "timezone": "UTC",
            "forecast_days": 3,
            "models": model,
        }
        url = f"https://api.open-meteo.com/v1/forecast?{urlencode(params)}"

        try:
            with urlopen(url, timeout=20) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}")
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            raise RuntimeError(f"HTTPError {exc.code}") from exc
        except URLError as exc:
            raise RuntimeError(f"URLError {exc.reason}") from exc

        if "hourly" not in payload:
            raise RuntimeError("Réponse invalide: clé 'hourly' absente")

        return payload
