from app.db.connection import MySqlConnectionPoolBuilder
from mysql.connector.errors import InterfaceError
import pytest


class TestConnectionBuilder:

    def test_when_builder_dict_structure_has_expected_pool_size(self):
        expected_pool_size = 10
        connection_pool_builder = MySqlConnectionPoolBuilder.builder().set_pool_size(
            expected_pool_size
        )
        assert connection_pool_builder.pool_config["pool_size"] == expected_pool_size

    def test_when_builder_dict_structure_has_expected_user(self):
        expected_user = "Adam"
        connection_pool_builder = MySqlConnectionPoolBuilder.builder().set_user(
            expected_user
        )
        assert connection_pool_builder.pool_config["user"] == expected_user

    def test_when_builder_dict_structure_has_expected_password(self):
        expected_password = "adam1234"
        connection_pool_builder = MySqlConnectionPoolBuilder.builder().set_password(
            expected_password
        )
        assert connection_pool_builder.pool_config["password"] == expected_password

    def test_when_builder_dict_structure_has_expected_db_name(self):
        expected_db_name = "my_db_3"
        connection_pool_builder = MySqlConnectionPoolBuilder.builder().set_database(
            expected_db_name
        )
        assert connection_pool_builder.pool_config["database"] == expected_db_name

    def test_when_builder_dict_structure_has_expected_items(self):
        expected_port = 3308
        connection_pool_builder = MySqlConnectionPoolBuilder.builder().set_port(
            expected_port
        )
        assert connection_pool_builder.pool_config["port"] == expected_port

    def test_when_connection_builder_works(self):
        connection_pool = (
            MySqlConnectionPoolBuilder.builder()
            .set_pool_size(31)
            .set_port(3308)
            .build()
        )
        assert connection_pool.get_connection() is not None

    def test_when_connection_builder_has_invalid_port(self):
        with pytest.raises(InterfaceError) as err:
            MySqlConnectionPoolBuilder.builder().set_port(3309).build()

        assert "Can't connect to MySQL server" in str(err.value)

    def test_when_connection_builder_has_invalid_pool_size(self):
        negative_pool_size = -10
        too_large_pool_size = 33
        with pytest.raises(AttributeError) as err:
            MySqlConnectionPoolBuilder.builder().set_pool_size(
                negative_pool_size
            ).build()
            assert "Pool size should be higher than 0" in str(err.value)

            MySqlConnectionPoolBuilder.builder().set_pool_size(
                too_large_pool_size
            ).build()
            assert "Pool size should be lower or equal to 32" in str(err.value)
