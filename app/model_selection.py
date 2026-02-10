from __future__ import annotations

from typing import List

from app.models import PointOfInterest


GLOBAL_MODELS: List[str] = [
    "ecmwf_ifs04",
    "gfs_seamless",
]

COUNTRY_HIGH_RES_MODELS: dict[str, list[str]] = {
    # Royaume-Uni / Londres
    "GB": ["ukmo_uk_deterministic_2km", "icon_eu"],
    "UK": ["ukmo_uk_deterministic_2km", "icon_eu"],
    # États-Unis
    "US": ["hrrr", "nam_conus"],
}


def preferred_models(point: PointOfInterest) -> list[str]:
    """Retourne la liste des modèles météo à tenter, du plus fin au plus large."""
    country_models = COUNTRY_HIGH_RES_MODELS.get(point.country_code.upper(), [])
    return [*country_models, *GLOBAL_MODELS]
