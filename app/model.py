from dataclasses import dataclass
from datetime import datetime
from abc import ABC


@dataclass
class BaseTable(ABC):
    id_: int | None = None
    name: str | None = None


@dataclass
class FoundedItems(BaseTable):
    image_data: bytes | None  = None
    quantity: int | None = 0
    addition_date: datetime | None = None
    finder_id : int | None = None
    locality_id: int | None = None
    material_id: int | None = None
    dating_id: int | None =  None


@dataclass
class Finder(BaseTable):
    pass


@dataclass
class Locality(BaseTable):
    location_id : int | None = None


@dataclass
class Location(BaseTable):
    coordinates: str | None = None


@dataclass
class Material(BaseTable):
    pass


@dataclass
class Dating(BaseTable):
    year: int |  None = None


@dataclass
class FinalItem(BaseTable):
    image_data: bytes | None = None
    quantity: int | None = 0
    addition_date: datetime | None = None
    finder_name: str | None = None
    locality_name: str | None = None
    location_name: str | None = None
    coordinates: str | None = None
    material_name: str | None = None
    epoch_name: str |  None =  None
    year: int | None = None






