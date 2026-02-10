from pathlib import Path

from app.models import PointOfInterest
from app.service import WeatherModelService


def test_service_falls_back_to_next_model(monkeypatch, tmp_path: Path) -> None:
    point = PointOfInterest("Londres", 51.5, -0.12, "GB")
    service = WeatherModelService(points=[point], storage_path=tmp_path / "latest.json")

    calls: list[str] = []

    def fake_request(_point: PointOfInterest, model: str):
        calls.append(model)
        if model == "ukmo_uk_deterministic_2km":
            raise RuntimeError("unavailable")
        return {"hourly": {"temperature_2m": [10, 11]}}

    monkeypatch.setattr(WeatherModelService, "_request_open_meteo", staticmethod(fake_request))

    payload = service.refresh_all()
    result = payload["results"][0]

    assert calls[:2] == ["ukmo_uk_deterministic_2km", "icon_eu"]
    assert result["selected_model"] == "icon_eu"
    assert result["errors"][0]["model"] == "ukmo_uk_deterministic_2km"
