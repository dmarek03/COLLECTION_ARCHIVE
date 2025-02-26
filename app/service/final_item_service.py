from dataclasses import dataclass
from app.persistance.model import (
    Dating,
    Finder,
    Locality,
    Location,
    Material,
    FoundedItem,
)
from app.persistance.repository.dating import DatingRepository
from app.persistance.repository.finder import FinderRepository
from app.persistance.repository.locality import LocalityRepository
from app.persistance.repository.location import LocationRepository
from app.persistance.repository.material import MaterialRepository
from app.persistance.repository.founded_items import FoundedItemRepository
from app.service.dto import CreateFinalItemDto


@dataclass
class FinalItemService:
    dating_repository: DatingRepository
    finder_repository: FinderRepository
    locality_repository: LocalityRepository
    location_repository: LocationRepository
    material_repository: MaterialRepository
    founded_items_repository: FoundedItemRepository

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
            FoundedItem(
                name=create_final_item_dto.name,
                description=create_final_item_dto.description,
                first_image_data=create_final_item_dto.first_image_data,
                second_image_data=create_final_item_dto.second_image_data,
                quantity=create_final_item_dto.quantity,
                finding_date=create_final_item_dto.finding_date,
                addition_date=create_final_item_dto.addition_date,
                finder_id=finder_id,
                location_id=location_id,
                dating_id=dating_id,
                material_id=material_id,
            )
        )

    def update_final_item(self, old_item_id: int, updated_item: CreateFinalItemDto) -> int:
        new_finder_id = self.finder_repository.find_or_create(
            item=Finder(name=updated_item.finder_name)
        )

        new_dating_id = self.dating_repository.find_or_create(
            item=Dating(name=updated_item.epoch_name, year=updated_item.year)
        )

        new_locality_id = self.locality_repository.find_or_create(
            item=Locality(name=updated_item.locality_name)
        )

        new_location_id = self.location_repository.find_or_create(
            item=Location(
                name=updated_item.location_name,
                latitude=updated_item.latitude,
                longitude=updated_item.longitude,
                latitude_direction=updated_item.latitude_direction,
                longitude_direction=updated_item.longitude_direction,
                locality_id=new_locality_id
            )
        )

        new_material_id = self.material_repository.find_or_create(
            item=Material(name=updated_item.material_name)
        )

        return self.founded_items_repository.update(
            old_item_id=old_item_id,
            updated_item=FoundedItem(
                name=updated_item.name,
                description=updated_item.description,
                first_image_data=updated_item.first_image_data,
                second_image_data=updated_item.second_image_data,
                quantity=updated_item.quantity,
                finding_date=updated_item.finding_date,
                addition_date=updated_item.addition_date,
                finder_id=new_finder_id,
                location_id=new_location_id,
                dating_id=new_dating_id,
                material_id=new_material_id
            )
        )

    def delete_final_item(self, item_id: int) -> int:
        return self.founded_items_repository.delete(item_id=item_id)
