from app.model_selection import preferred_models
from app.models import PointOfInterest


def test_gb_prefers_high_resolution_models_first() -> None:
    point = PointOfInterest("Londres", 51.5, -0.12, "GB")
    models = preferred_models(point)
    assert models[:2] == ["ukmo_uk_deterministic_2km", "icon_eu"]
    assert models[-2:] == ["ecmwf_ifs04", "gfs_seamless"]


def test_us_prefers_hrrr_and_nam() -> None:
    point = PointOfInterest("Chicago", 41.8, -87.6, "US")
    models = preferred_models(point)
    assert models[:2] == ["hrrr", "nam_conus"]


def test_non_hr_country_falls_back_to_global() -> None:
    point = PointOfInterest("Tokyo", 35.6, 139.6, "JP")
    models = preferred_models(point)
    assert models == ["ecmwf_ifs04", "gfs_seamless"]
