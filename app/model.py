from dataclasses import dataclass
from datetime import datetime
from abc import ABC



@dataclass
class BaseTable(ABC):
    id_: int | None = None
    name: str | None = None


@dataclass
class FoundedItems(BaseTable):
    description: str | None = None
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
    latitude: float | None = None
    longitude: float | None = None
    latitude_direction: str | None = None
    longitude_direction: str | None = None


@dataclass
class Material(BaseTable):
    pass


@dataclass
class Dating(BaseTable):
    year: int |  str = 'indefinite'


@dataclass
class FinalItem(BaseTable):
    description: str | None = None
    image_data: bytes | None = None
    quantity: int | None = 0
    addition_date: datetime | None = None
    finder_name: str | None = None
    locality_name: str | None = None
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    latitude_direction: str | None = None
    longitude_direction: str | None = None
    material_name: str | None = None
    epoch_name: str |  None =  None
    year: int | str = None


    def __repr__(self):
        return f'''
            Name: {self.name},
            Description: {self.description},
            Image date: {self.image_data},
            Quantity: {self.quantity=},
            Date of addition: {self.addition_date},
            Name of finder: {self.finder_name},
            Name of locality: {self.locality_name},
            Name of location: {self.location_name},
            Coordinates: {self.latitude}°{self.latitude_direction} , {self.longitude}°{self.longitude_direction},
            Name of material: {self.material_name},
            Name of the epoch: {self.epoch_name},
            Year: {self.year}

        '''






