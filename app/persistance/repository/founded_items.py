from .generic.repository import CrudRepository
from app.persistance.model import FoundedItems, FinalItem
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging


class FoundedItemsRepository(CrudRepository):

    def __init__(self, connection_pool:MySQLConnectionPool):
        super().__init__(connection_pool, FoundedItems)
        self._create_table()
        self.select_all_items_info_sql_statement = f'''
                select f.id, f.name, f.description, f.image_data, f.quantity, f.addition_date,fd.name, l.name,ll.name,
                ll.latitude, ll.longitude, ll.latitude_direction, ll.longitude_direction, m.name, d.name, d.year
                from founded_items f
                join datings d on d.id = f.dating_id
                join finders fd on fd.id = f.finder_id
                join localities l on l.id = f.locality_id
                join locations ll on l.location_id = ll.id
                join materials m on m.id = f.material_id
            '''

    def _create_table(self):
        try:
            create_founded_item_table = '''
                create table if not exists founded_items(
                    id integer primary key auto_increment,
                    name varchar(50) not null,
                    description varchar(500) not null,
                    image_data LONGBLOB not null, 
                    addition_date datetime not null,
                    quantity integer default 0,
                    finder_id integer, 
                    material_id integer, 
                    dating_id integer,
                    locality_id integer,
                    unique (name,description,addition_date, quantity),
                    foreign key (finder_id) references finders(id) on delete cascade on update cascade,
                    foreign key (material_id) references materials(id) on delete cascade on update cascade,
                    foreign key (dating_id) references datings(id) on delete cascade on update cascade,
                    foreign key (locality_id) references localities(id) on delete cascade on update cascade 
                )

            '''

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(create_founded_item_table)
                connection.commit()
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_items_order_by(self, column_name: str | None = None, descending:bool = False) -> list[FinalItem]:

        try:
            connection = self.connection_pool.get_connection()
            sql = self.select_all_items_info_sql_statement
            if column_name:
                sql += f'order by {column_name}'
                if descending:
                    sql += ' desc'
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [FinalItem(*row) for row in cursor.fetchall()]


        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_items_where_value_between(self, column_name: str, range_min: int, range_max: int, descending: bool = False) -> list[FinalItem]:

        try:
            connection = self.connection_pool.get_connection()
            sql = self.select_all_items_info_sql_statement
            sql += f'where {column_name} between {range_min} and {range_max} order by {column_name}' + ' desc' if descending else ""

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [FinalItem(*row) for row in cursor.fetchall()]


        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_items_where_value_equals(self, column_name: str, variable: str | int, descending: bool = False) -> list[FinalItem]:

        try:
            connection = self.connection_pool.get_connection()
            sql = self.select_all_items_info_sql_statement
            sql += f'''where {column_name} = '{variable}' order by {column_name}''' + ' desc' if descending else ''

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [FinalItem(*row) for row in cursor.fetchall()]


        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_items_order_by(self, value: str | None, descending: bool) -> list[FinalItem]:
        match value:
            case 'item name':
                return self.fetch_items_order_by(column_name='f.name', descending=descending)

            case 'addition date':
                 return self.fetch_items_order_by(column_name='f.addition_date', descending=descending)

            case 'quantity':
                return self.fetch_items_order_by(column_name='f.addition_date', descending=descending)

            case 'finder name':
                return self.fetch_items_order_by(column_name='fd.name', descending=descending)

            case 'locality name':
                return self.fetch_items_order_by(column_name='l.name', descending=descending)

            case 'location name':
                return self.fetch_items_order_by(column_name='ll.name', descending=descending)

            case 'material name':
                return self.fetch_items_order_by(column_name='m.name', descending=descending)

            case 'epoch name':
                return self.fetch_items_order_by(column_name='d.name', descending=descending)

            case 'year':
                return self.fetch_items_order_by(column_name='year', descending=descending)

            case _ :
                return self.fetch_items_order_by()





    def get_all_item_where_value_between(self, value: str, range_min: int, range_max: int, descending:bool) -> list[FinalItem]:

        match value:
            case 'quantity':
                return self.fetch_items_where_value_between('f.quantity', range_min, range_max, descending)

            case 'year':
                return self.fetch_items_where_value_between('d.year', range_min, range_max, descending)


            case 'latitude':
                return self.fetch_items_where_value_between('ll.latitude', range_min, range_max, descending)


            case 'longitude':
                return self.fetch_items_where_value_between('ll.longitude', range_min, range_max, descending)


    def get_all_item_where_value_equals(self, value: str, variable: str | int, descending: bool) -> list[FinalItem]:

        match value:
            case 'item name':
                return self.fetch_items_where_value_equals(column_name='f.id', variable=variable, descending=descending)

            case 'finder name':
                return self.fetch_items_where_value_equals(column_name='fd.name', variable=variable, descending=descending)

            case 'locality name':
                return self.fetch_items_where_value_equals(column_name='l.name', variable=variable,descending=descending)

            case 'location name':
                return self.fetch_items_where_value_equals(column_name='ll.name', variable=variable,descending=descending)

            case 'latitude direction':
                return self.fetch_items_where_value_equals(column_name='ll.latitude_direction', variable=variable, descending=descending)

            case 'longitude direction':
                return self.fetch_items_where_value_equals(column_name='ll.longitude_direction', variable=variable, descending=descending)

            case 'material name':
                return self.fetch_items_where_value_equals(column_name='m.name', variable=variable, descending=descending)

            case 'epoch name':
                return self.fetch_items_where_value_equals(column_name='d.name', variable=variable,descending=descending)

            case 'year':
                return self.fetch_items_where_value_equals(column_name='d.year', variable=variable,descending=descending)




    def get_all_items_order_by_name(self, descending:bool) -> list[FinalItem]:
        return self.fetch_items_order_by(column_name='f.name', descending=descending)


    def get_all_items_order_by_addition_date(self, descending:bool) -> list[FinalItem]:
        return self.fetch_items_order_by(column_name='f.addition_date', descending=descending)


    def get_all_items_order_by_quantity(self, descending:bool) -> list[FinalItem]:
        return self.fetch_items_order_by(column_name='f.quantity', descending=descending)


    def get_all_items_order_by_finder_name(self, descending: bool) -> list[FinalItem]:
        return self.fetch_items_order_by(column_name='fd.name', descending=descending)


    def get_all_items_order_by_locality_name(self, descending: bool) -> list[FinalItem]:
        return self.fetch_items_order_by(column_name='l.name', descending=descending)


    def get_all_items_order_by_location_name(self,descending:bool) -> list[FinalItem]:
        return self.fetch_items_order_by(column_name='ll.name', descending=descending)


    def get_all_items_order_by_material_name(self, descending:bool) -> list[FinalItem]:
        return self.fetch_items_order_by(column_name='m.name', descending=descending)

    def get_all_items_order_by_epoch_name(self, descending: bool) -> list[FinalItem]:
        return self.fetch_items_order_by(column_name='d.name', descending=descending)

    def get_all_items_order_by_year(self, descending: bool) -> list[FinalItem]:
        return self.fetch_items_order_by(column_name='year', descending=descending)






