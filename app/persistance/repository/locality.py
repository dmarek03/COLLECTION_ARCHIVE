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
            create_locality_table = '''
             create table if not exists localities(
                    id integer primary key auto_increment,
                    name varchar(50) not null,
                    location_id integer,
                    unique (name),
                    foreign key (location_id) references locations(id) on delete cascade on update cascade 
                )'''



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




