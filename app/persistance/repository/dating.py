from .generic.repository import CrudRepository
from app.persistance.model import Dating
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class DatingRepository(CrudRepository):

    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Dating)
        self.create_table()

    def create_table(self):
        try:
            create_dating_table = """
                create table if not exists datings(
                    id integer primary key auto_increment,
                    name varchar(50) not null,
                    year integer default null,
                    unique (name, year)
                )
            
            """

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(create_dating_table)
                connection.commit()
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_epoch_name(self, descending: bool = False) -> list[str]:
        try:
            sql = f""" select distinct name from datings order by name"""
            sql += " desc" if descending else ""
            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [e_name[0] for e_name in cursor.fetchall()]

        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_years(self, descending: bool = False) -> list[int]:
        try:
            sql = f" select distinct year from datings order by year {'desc' if descending else ''}"

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)

                return [year[0] for year in cursor.fetchall()]
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
