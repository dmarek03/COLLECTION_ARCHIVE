from mysql.connector.pooling import MySQLConnectionPool, Error
import logging
from typing import Self, Any
import os
from dotenv import load_dotenv

load_dotenv()

connection_params = dict(
    pool_name="my_pool",
    pool_size=5,
    pool_reset_session=True,
    host=os.getenv("HOST", default="localhost"),
    database=os.getenv("DATABASE", default="db_1"),
    user=os.getenv("USER", default="user"),
    password=os.getenv("PASSWORD", default="user1234"),
    port=int(os.getenv("PORT", default=3307)),
)


class MySqlConnectionPoolBuilder:
    def __init__(self, params: dict[str, Any] = None):
        params = {} if not params else params
        self.pool_config = {
            "pool_name": "mysql_connection_pool",
            "pool_size": 5,
            "pool_reset_session": True,
            "host": "localhost",
            "database": "db_2",
            "user": "user",
            "password": "user1234",
            "port": 3307,
        } | params

    def set_pool_size(self, new_pool_size: int) -> Self:
        self.pool_config["pool_size"] = new_pool_size
        return self

    def set_user(self, new_user: str) -> Self:
        self.pool_config["user"] = new_user
        return self

    def set_password(self, new_password: str) -> Self:
        self.pool_config["password"] = new_password
        return self

    def set_database(self, new_db: str) -> Self:
        self.pool_config["database"] = new_db
        return self

    def set_port(self, new_port: int) -> Self:
        self.pool_config["port"] = new_port
        return self

    def build(self) -> MySQLConnectionPool:
        return MySQLConnectionPool(**self.pool_config)

    @classmethod
    def builder(cls) -> Self:
        return cls()


def get_connection_pool():
    return MySqlConnectionPoolBuilder(connection_params).builder().build()


def get_connection_test_pool():
    return (
        MySqlConnectionPoolBuilder(connection_params).builder().set_port(3308).build()
    )


def initialize_triggers(connection_pool: MySQLConnectionPool) -> int:

    with open("db/triggers.sql", "r") as f:
        print(f"{f=}")
        triggers_sql = f.read()

    try:
        connection = connection_pool.get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(triggers_sql)
    except Error as err:
        logging.error(err)
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return 1


def create_tables(connection_pool: MySQLConnectionPool):

    try:
        create_datings_table_sql = """
            create table if not exists datings(
                id integer primary key auto_increment,
                name varchar(50) not null,
                year integer default null,
                unique (name, year)
            )

        """

        create_finders_table_sql = """
                       create table if not exists finders(
                           id integer primary key auto_increment,
                           name varchar(50) not null ,
                           unique (name)
                       )

                   """

        create_localities_table_sql = """
                    create table if not exists localities(
                           id integer primary key auto_increment,
                           name varchar(50) not null, 
                           unique (name)

                       )"""

        create_locations_table_sql = """
                        create table if not exists locations(
                            id integer primary key auto_increment,
                            name varchar(50) default null,
                            latitude double default null,
                            longitude double default null,
                            latitude_direction varchar(3) default null, 
                            longitude_direction varchar(3) default null,
                            locality_id integer,
                            unique(name,latitude,longitude,latitude_direction, longitude_direction),
                            foreign key (locality_id) references localities(id) on delete cascade on update cascade
                        )

                    """

        create_materials_table_sql = """
                       create table if not exists materials(
                           id integer primary key auto_increment,
                           name varchar(50) not null,
                           unique(name)
                       )

                   """

        create_founded_items_table_sql = """
                        create table if not exists founded_items(
                            id integer primary key auto_increment,
                            name varchar(50) not null,
                            description varchar(500) not null,
                            image_data LONGBLOB not null, 
                            addition_date datetime not null,
                            quantity integer default 0,
                            finder_id integer, 
                            material_id integer, 
                            dating_id integer,
                            location_id integer,
                            unique (name,description,addition_date, quantity),
                            foreign key (finder_id) references finders(id) on delete cascade on update cascade,
                            foreign key (material_id) references materials(id) on delete cascade on update cascade,
                            foreign key (dating_id) references datings(id) on delete cascade on update cascade,
                            foreign key (location_id) references locations(id) on delete cascade on update cascade 
                        )

                    """

        connection = connection_pool.get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(create_datings_table_sql)
            cursor.execute(create_finders_table_sql)
            cursor.execute(create_localities_table_sql)
            cursor.execute(create_locations_table_sql)
            cursor.execute(create_materials_table_sql)
            cursor.execute(create_founded_items_table_sql)
            connection.commit()

    except Error as err:
        logging.error(err)
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def drop_tables(connection_pool: MySQLConnectionPool):
    try:
        drop_datings_table_sql = "drop table if exists datings"
        drop_finders_table_sql = "drop table if exists finders"
        drop_localities_table_sql = "drop table if exists localities"
        drop_locations_table_sql = "drop table if exists locations"
        drop_materials_table_sql = "drop table if exists materials"
        drop_founded_items_table_sql = "drop table if exists founded_items"
        connection = connection_pool.get_connection()
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(drop_founded_items_table_sql)
            cursor.execute(drop_datings_table_sql)
            cursor.execute(drop_finders_table_sql)
            cursor.execute(drop_locations_table_sql)
            cursor.execute(drop_localities_table_sql)
            cursor.execute(drop_materials_table_sql)

            connection.commit()
    except Error as err:
        logging.error(err)
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


connection_pool = get_connection_pool()
connection_test_pool = get_connection_test_pool()
