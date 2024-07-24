from .generic.repository import CrudRepository
from app.model import Location
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class LocationRepository(CrudRepository):

    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Location)
        self._create_table()

    def _create_table(self):
        try:
            create_location_table = '''
                create table if not exists locations(
                    id integer primary key auto_increment,
                    name varchar(50) not null,
                    coordinates varchar(50) default null
                )

            '''

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


