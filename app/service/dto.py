from dataclasses import dataclass
from datetime import datetime, date


@dataclass
class CreateFinalItemDto:
    id: int | None = None
    name: str | None = None
    description: str | None = None
    first_image_data: bytes | None = None
    second_image_data: bytes | None = None
    quantity: int | None = 0
    finding_date: date | None = None
    addition_date: datetime = datetime.now()
    finder_name: str | None = None
    locality_name: str | None = None
    location_name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    latitude_direction: str | None = None
    longitude_direction: str | None = None
    material_name: str | None = None
    epoch_name: str | None = None
    year: int | str = None

    @staticmethod
    def coordinates_to_dms(value: float) -> tuple[float, float, float]:
        degrees = int(value)
        minutes_full = abs(value - degrees) * 60
        minutes = int(minutes_full)
        seconds = abs(minutes_full - minutes) * 60

        return degrees, minutes, seconds

    def __repr__(self):
        lat_deg, lat_min, lat_sec = self.coordinates_to_dms(value=self.latitude)
        log_deg, log_min, log_sec = self.coordinates_to_dms(value=self.longitude)
        return f"""
               Name: {self.name}
               Description: {self.description}
               First image bytes: {len(self.first_image_data)}
               Second image bytes: {len(self.second_image_data)}
               Quantity: {self.quantity}
               Date of addition: {self.addition_date}
               Date of finding: {self.finding_date}
               Name of finder: {self.finder_name}
               Name of locality: {self.locality_name}
               Name of location: {self.location_name if self.location_name else 'Indefinite'}
               Coordinates: 
               {lat_deg}°{lat_min}′{lat_sec}″ {self.latitude_direction} , 
               {log_deg}°{log_min}′{log_sec}″{self.longitude_direction}
               Name of material: {self.material_name}
               Name of the epoch: {self.epoch_name}
               Year: {self.year if self.year else 'Indefinite'}

           """
