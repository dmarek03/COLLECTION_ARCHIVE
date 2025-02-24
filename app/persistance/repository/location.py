from .generic.repository import CrudRepository
from app.persistance.model import Location
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class LocationRepository(CrudRepository):

    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Location)
        self._create_table()

    def _create_table(self):
        try:
            create_location_table = """
                create table if not exists locations(
                    id integer primary key auto_increment,
                    name varchar(50) default null,
                    latitude double default null,
                    longitude double default null,
                    latitude_direction varchar(3) default null, 
                    longitude_direction varchar(3) default null,
                    locality_id integer,
                    unique(name,latitude,longitude,latitude_direction, longitude_direction,locality_id),
                    foreign key (locality_id) references localities(id) on delete cascade on update cascade
                )

            """

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(create_location_table)
                connection.commit()
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_location_name(self, descending: bool = False) -> list[str]:

        try:
            sql = f" select distinct name from locations order by name {'desc' if descending else ''}"

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)

                return [ll_name[0] for ll_name in cursor.fetchall()]
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_location_coordinates(
        self, descending: bool = False
    ) -> list[tuple[str, str]]:
        try:
            sql = f" select distinct latitude, longitude, latitude_direction, longitude_direction from locations order by name"
            sql += " desc" if descending else ""

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)

                return [
                    (str(lat) + "°" + lat_d, str(lon) + "°" + lon_d)
                    for lat, lon, lat_d, lon_d in cursor.fetchall()
                ]
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
