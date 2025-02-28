from .generic.repository import CrudRepository
from app.persistance.model import Season
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class SeasonRepository(CrudRepository):
    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Season)
        self._create_table()

    def _create_table(self):
        try:
            create_season_table = """
                create table if not exists seasons(
                    id integer primary key auto_increment,
                    name varchar(50) not null,
                    unique(name)
                )

            """

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(create_season_table)
                connection.commit()
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_seasons_name(self) -> list[str]:
        return [s.name for s in self.find_all()]
