from .generic.repository import CrudRepository
from app.persistance.model import Finder
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class FinderRepository(CrudRepository):

    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Finder)
        self._create_table()

    def _create_table(self):
        try:
            create_finder_table = """
                create table if not exists finders(
                    id integer primary key auto_increment,
                    name varchar(50) not null ,
                    unique (name)
                )

            """

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(create_finder_table)
                connection.commit()
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_finder_name(self, descending: bool = False) -> list[str]:

        try:
            sql = f" select name from finders order by name {'desc' if descending else ''}"

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [f_name[0] for f_name in cursor.fetchall()]

        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
