from app.db.connection import connection_pool, initialize_triggers
from .repository.dating import DatingRepository
from .repository.finder import FinderRepository
from .repository.locality import LocalityRepository
from .repository.location import LocationRepository
from .repository.material import MaterialRepository
from .repository.founded_items import FoundedItemRepository

dating_repository = DatingRepository(connection_pool=connection_pool)
finder_repository = FinderRepository(connection_pool=connection_pool)
locality_repository = LocalityRepository(connection_pool=connection_pool)
location_repository = LocationRepository(connection_pool=connection_pool)
material_repository = MaterialRepository(connection_pool=connection_pool)
founded_items_repository = FoundedItemRepository(connection_pool=connection_pool)


trigger_initialized = False
if not trigger_initialized:
    initialize_triggers(connection_pool=connection_pool)
    trigger_initialized = True
