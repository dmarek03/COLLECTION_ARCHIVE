from dataclasses import dataclass
from app.persistance.model import (
    Dating,
    Finder,
    Locality,
    Location,
    Material,
    FoundedItems,
)
from app.persistance.repository.dating import DatingRepository
from app.persistance.repository.finder import FinderRepository
from app.persistance.repository.locality import LocalityRepository
from app.persistance.repository.location import LocationRepository
from app.persistance.repository.material import MaterialRepository
from app.persistance.repository.founded_items import FoundedItemsRepository
from app.service.dto import CreateFinalItemDto


@dataclass
class FinalItemService:
    dating_repository: DatingRepository
    finder_repository: FinderRepository
    locality_repository: LocalityRepository
    location_repository: LocationRepository
    material_repository: MaterialRepository
    founded_items_repository: FoundedItemsRepository

    def add_final_item(self, create_final_item_dto: CreateFinalItemDto) -> int:
        finder_id = self.finder_repository.insert(
            Finder(name=create_final_item_dto.finder_name)
        )

        dating_id = self.dating_repository.insert(
            Dating(
                name=create_final_item_dto.epoch_name, year=create_final_item_dto.year
            )
        )

        locality_id = self.locality_repository.insert(
            Locality(name=create_final_item_dto.locality_name)
        )

        location_id = self.location_repository.insert(
            Location(
                name=create_final_item_dto.location_name,
                latitude=create_final_item_dto.latitude,
                longitude=create_final_item_dto.longitude,
                latitude_direction=create_final_item_dto.latitude_direction,
                longitude_direction=create_final_item_dto.longitude_direction,
                locality_id=locality_id,
            )
        )

        material_id = self.material_repository.insert(
            Material(name=create_final_item_dto.material_name)
        )

        return self.founded_items_repository.insert(
            FoundedItems(
                name=create_final_item_dto.name,
                description=create_final_item_dto.description,
                image_data=create_final_item_dto.image_data,
                quantity=create_final_item_dto.quantity,
                addition_date=create_final_item_dto.addition_date,
                finder_id=finder_id,
                location_id=location_id,
                dating_id=dating_id,
                material_id=material_id,
            )
        )

    def delete_final_item(self, item_id) -> int:
        return self.founded_items_repository.delete(item_id=item_id)
