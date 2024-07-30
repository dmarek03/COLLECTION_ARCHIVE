from dataclasses import dataclass
from app.persistance.repository.dating import DatingRepository
from app.persistance.repository.finder import FinderRepository
from app.persistance.repository.location import LocationRepository
from app.persistance.repository.locality import LocalityRepository
from app.persistance.repository.material import MaterialRepository
from app.persistance.repository.founded_items import FoundedItemsRepository

@dataclass
class FoundedItemsService:
    dating_repository: DatingRepository
    finder_repository: FinderRepository
    location_repository: LocationRepository
    locality_repository: LocalityRepository
    material_repository: MaterialRepository
    founded_items_repository: FoundedItemsRepository

