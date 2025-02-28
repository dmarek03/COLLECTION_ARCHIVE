from dataclasses import dataclass
from datetime import datetime, date
from abc import ABC


@dataclass
class BaseTable(ABC):
    id_: int | None = None
    name: str | None = None


@dataclass
class FoundedItem(BaseTable):
    description: str | None = None
    first_image_data: bytes | None = None
    second_image_data: bytes | None = None
    quantity: int | None = 0
    finding_date: date | None = None
    addition_date: datetime | None = None
    finder_id: int | None = None
    location_id: int | None = None
    material_id: int | None = None
    dating_id: int | None = None


@dataclass
class Finder(BaseTable):
    pass


@dataclass
class Locality(BaseTable):
    pass


@dataclass
class Location(BaseTable):
    latitude: float | None = None
    longitude: float | None = None
    latitude_direction: str | None = None
    longitude_direction: str | None = None
    locality_id: int | None = None


@dataclass
class Material(BaseTable):
    pass


@dataclass
class Dating(BaseTable):
    year: int | None = None


@dataclass
class WishItem(BaseTable):
    image_data: bytes | None = None
    season_id: int | None = None


@dataclass
class Season(BaseTable):
    pass
