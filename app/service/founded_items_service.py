from dataclasses import dataclass
from typing import Self

from app.repository.dating import DatingRepository, Dating
from app.repository.finder import FinderRepository, Finder
from app.repository.location import LocationRepository, Location
from app.repository.locality import LocalityRepository, Locality
from app.repository.material import MaterialRepository, Material
from app.repository.founded_items import FoundedItemsRepository, FoundedItems
from mysql.connector.pooling import MySQLConnectionPool,Error
from app.db.connection import get_connection_pool
from datetime import datetime as dt
import logging
@dataclass
class FoundedItemsService:
    dating_repository: DatingRepository
    finder_repository: FinderRepository
    location_repository: LocationRepository
    locality_repository: LocalityRepository
    material_repository: MaterialRepository
    founded_items_repository: FoundedItemsRepository


connection_pool = get_connection_pool()
print(f'{connection_pool=}')
dating_repo =  DatingRepository(connection_pool=connection_pool)
finder_repo = FinderRepository(connection_pool=connection_pool)
location_repo = LocationRepository(connection_pool=connection_pool)
locality_repo = LocalityRepository(connection_pool=connection_pool)
material_repo = MaterialRepository(connection_pool=connection_pool)
founded_items_repo = FoundedItemsRepository(connection_pool=connection_pool)
# #
# location_repo.insert(Location(name='Grabie', latitude=49.70320308312001, longitude= 21.561587589660267, latitude_direction='N', longitude_direction='E'))
# locality_repo.insert(Locality(name='Umieszcz', location_id=location_repo.find_last_n(1)[0].id_))
# dating_repo.insert(Dating(name='Middle Ages',year=1340))
# finder_repo.insert(Finder(name='Adam'))
# material_repo.insert(Material(name='silver'))

# finder_id = finder_repo.find_last_n(1)[0].id_
# dating_id = dating_repo.find_last_n(1)[0].id_
# material_id = material_repo.find_last_n(1)[0].id_
# locality_id = locality_repo.find_last_n(1)[0].id_
# founded_items_repo.insert(FoundedItems(
#     name='Prague groschen ',
#     description= 'The most popular coin at polish terrain in late Middle ages',
#     image_data=bytes([2]),
#     quantity=1,
#     addition_date=dt.now(),
#     finder_id=finder_id,
#     locality_id=locality_id,
#     material_id=material_id,
#     dating_id=dating_id
# ))

#founded_items_repo.delete(item_id=2)

#
founded_items_service =  FoundedItemsService(
    dating_repo,
    finder_repo,
    location_repo,
    locality_repo,
    material_repo,
    founded_items_repo
)


# print(founded_items_service.founded_items_repository.get_all_items_order_by('item name', descending=True))
# print(founded_items_service.founded_items_repository.get_all_item_where_value_equals('year',variable=1340, descending=False))
# print(founded_items_service.dating_repository.get_all_years(descending=False))
