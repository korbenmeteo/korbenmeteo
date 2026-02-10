from dataclasses import dataclass


@dataclass(frozen=True)
class PointOfInterest:
    name: str
    latitude: float
    longitude: float
    country_code: str
