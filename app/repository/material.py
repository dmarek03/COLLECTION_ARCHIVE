from .generic.repository import CrudRepository
from app.model import Material
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class MaterialRepository(CrudRepository):

    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, Material)
        self._create_table()

    def _create_table(self):
        try:
            create_material_table = '''
                create table if not exists materials(
                    id integer primary key auto_increment,
                    name varchar(50) not null
                )

            '''

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

