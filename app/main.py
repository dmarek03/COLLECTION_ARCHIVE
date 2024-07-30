from service.founded_items_service import FoundedItemsService
from app.persistance.configuration import (
    dating_repository,
    finder_repository,
    location_repository,
    locality_repository,
    material_repository,
    founded_items_repository
)
import logging

logging.basicConfig(level=logging.INFO)



def main() -> None:

    founded_items_service = FoundedItemsService(
        dating_repository,
        finder_repository,
        location_repository,
        locality_repository,
        material_repository,
        founded_items_repository
    )

    # founded_items_service.location_repo.insert(Location(name='Grabie', latitude=49.70320308312001, longitude= 21.561587589660267, latitude_direction='N', longitude_direction='E'))
    # founded_items_service.locality_repo.insert(Locality(name='Umieszcz', location_id=location_repo.find_last_n(1)[0].id_))
    # founded_items_service.dating_repo.insert(Dating(name='Middle Ages',year=1340))
    # founded_items_service.finder_repo.insert(Finder(name='Adam'))
    # founded_items_service.material_repo.insert(Material(name='silver'))

    # finder_id = founded_items_service.finder_repo.find_last_n(1)[0].id_
    # dating_id = founded_items_service.dating_repo.find_last_n(1)[0].id_
    # material_id = founded_items_service.material_repo.find_last_n(1)[0].id_
    # locality_id = founded_items_service.locality_repo.find_last_n(1)[0].id_
    # founded_items_service.founded_items_repo.insert(FoundedItems(
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

    # founded_items_service.founded_items_repo.delete(item_id=2)

    #

    print(founded_items_service.founded_items_repository.get_all_items_order_by('item name', descending=True))
    print(founded_items_service.founded_items_repository.get_all_item_where_value_equals('year',variable=1340, descending=False))
    print(founded_items_service.dating_repository.get_all_years(descending=False))

    x = founded_items_service.dating_repository.get_all_years(descending=False)
    print(f'{x[0]}')
if __name__ == '__main__':
    main()
