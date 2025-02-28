from .generic.repository import CrudRepository
from app.persistance.model import WishItem
from app.service.dto import CreatFinalWishItemDto
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class WishItemsRepository(CrudRepository):
    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, WishItem)
        self._create_table()

    def _create_table(self):
        try:
            create_wishlist_table = """
                create table if not exists wish_items(
                    id integer primary key auto_increment,
                    name varchar(50) not null,
                    image_data LONGBLOB  not null ,
                    season_id integer,
                    unique(name),
                    foreign key (season_id) references seasons(id) on delete cascade on update cascade 
                   
                )

            """

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(create_wishlist_table)
                connection.commit()
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_items_where_value_equals(self, season_name: str) -> list[CreatFinalWishItemDto]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            sql = f""" 
                       select w.id, w.name, w.image_data, s.name from wish_items w 
                       join seasons s on s.id = w.season_id where s.name = '{season_name}' order by s.name desc 
                   """
            cursor.execute(sql)

            return [CreatFinalWishItemDto(*row) for row in cursor.fetchall()]

        except Error as err:
            logging.error(err)
            connection.rollback()

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
