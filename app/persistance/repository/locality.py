from .generic.repository import CrudRepository
from app.persistance.model import Locality
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class LocalityRepository(CrudRepository):

    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Locality)
        self._create_table()

    def _create_table(self):
        try:
            create_locality_table = """
             create table if not exists localities(
                    id integer primary key auto_increment,
                    name varchar(50) not null, 
                    unique (name)
                   
                )"""

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(create_locality_table)
                connection.commit()
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_locality_name(self, descending: bool) -> list[str]:

        try:
            sql = f" select name from localities order by name {'desc' if descending else ''}"

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)

                return [l_name[0] for l_name in cursor.fetchall()]
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
