import pytest
import logging
from app.db.connection import connection_test_pool, create_tables, drop_tables
from app.persistance.repository.dating import DatingRepository
from app.persistance.repository.finder import FinderRepository
from app.persistance.repository.locality import LocalityRepository
from app.persistance.repository.location import LocationRepository
from app.persistance.repository.material import MaterialRepository
from app.persistance.repository.founded_items import FoundedItemsRepository


@pytest.fixture(scope="module")
def fake_connection():
    return connection_test_pool


@pytest.fixture(scope="module")
def fake_dating_repository(fake_connection):
    return DatingRepository(connection_pool=fake_connection)


@pytest.fixture(scope="module")
def fake_finder_repository(fake_connection):
    return FinderRepository(connection_pool=fake_connection)


@pytest.fixture(scope="module")
def fake_locality_repository(fake_connection):
    return LocalityRepository(connection_pool=fake_connection)


@pytest.fixture(scope="module")
def fake_location_repository(fake_connection):
    return LocationRepository(connection_pool=fake_connection)


@pytest.fixture(scope="module")
def fake_material_repository(fake_connection):
    return MaterialRepository(connection_pool=fake_connection)


@pytest.fixture(scope="module")
def fake_founded_item_repository(fake_connection):
    return FoundedItemsRepository(connection_pool=fake_connection)


@pytest.fixture(scope="module")
def run_before_and_after_all_test(fake_connection):
    logging.info("BEFORE ALL")
    create_tables(fake_connection)
    yield
    drop_tables(fake_connection)
    logging.info("AFTER ALL")
