from .generic.repository import CrudRepository
from app.persistance.model import Material
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class WishListRepository(CrudRepository):
    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Material)
        self._create_table()

    def _create_table(self):
        try:
            create_material_table = """
                create table if not exists wishlist(
                    id integer primary key auto_increment,
                    name varchar(50) not null,
                    image_data longblob not null ,
                    unique(name)
                )

            """

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(create_material_table)
                connection.commit()
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
