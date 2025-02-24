import logging
from datetime import date
from typing import Any

from .generic.repository import CrudRepository
from app.persistance.model import FoundedItem
from app.service.dto import CreateFinalItemDto
from mysql.connector.pooling import MySQLConnectionPool, Error


class FoundedItemRepository(CrudRepository):

    def __init__(self, connection_pool: MySQLConnectionPool):
        super().__init__(connection_pool, FoundedItem)
        self._create_table()
        self.select_all_items_info_sql_statement = f"""
                       select f.id, f.name, f.description, f.first_image_data,f.second_image_data,f.quantity, 
                       f.finding_date, f.addition_date,fd.name, l.name,ll.name,ll.latitude, ll.longitude, 
                       ll.latitude_direction, ll.longitude_direction, m.name, d.name, d.year
                       from founded_items f
                       join datings d on d.id = f.dating_id
                       join finders fd on fd.id = f.finder_id
                       join locations ll on ll.id = f.location_id
                       join localities l on l.id = ll.locality_id
                       join materials m on m.id = f.material_id
                       """

    def _create_table(self):
        try:
            create_founded_item_table = """
                create table if not exists founded_items(
                    id integer primary key auto_increment,
                    name varchar(50) not null,
                    description varchar(500) not null,
                    first_image_data LONGBLOB not null, 
                    second_image_data LONGBLOB not null, 
                    finding_date date,
                    addition_date datetime not null,
                    quantity integer default 0,
                    finder_id integer, 
                    material_id integer, 
                    dating_id integer,
                    location_id integer,
                    unique (name,description,addition_date, quantity),
                    foreign key (finder_id) references finders(id) on delete cascade on update cascade,
                    foreign key (material_id) references materials(id) on delete cascade on update cascade,
                    foreign key (dating_id) references datings(id) on delete cascade on update cascade,
                    foreign key (location_id) references locations(id) on delete cascade on update cascade 
                )

            """

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

    def get_images_data(self, founded_item_id: int) -> list[bytes]:
        try:
            connection = self.connection_pool.get_connection()
            cursor = connection.cursor()
            sql = f""" 
                select f.first_image_data, f.second_image_date 
                from founded_items f where f.id = {founded_item_id} 
            """
            cursor.execute(sql)

            return [image_date[0] for image_date in cursor.fetchall()]

        except Error as err:
            logging.error(err)
            connection.rollback()

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_items_order_by(
        self, column_name: str | None = None, descending: bool = False
    ) -> list[CreateFinalItemDto]:

        try:
            connection = self.connection_pool.get_connection()
            sql = self.select_all_items_info_sql_statement
            if column_name:
                sql += f"order by {column_name}"
                if descending:
                    sql += " desc"
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [CreateFinalItemDto(*row) for row in cursor.fetchall()]

        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_items_with_criteria(
        self,
        equals_criteria: dict[str, Any],
        range_criteria: dict[str, tuple[Any, Any]],
        order_column: str,
        descending: bool = False,
    ) -> list[CreateFinalItemDto]:
        try:
            connection = self.connection_pool.get_connection()
            sql = self.select_all_items_info_sql_statement + " where "
            for key, values in equals_criteria.items():
                sql += f"{key} in {values} and "

            for key, value_range in range_criteria.items():
                sql += f"{key} between '{value_range[0]}' and '{value_range[1]}' and "

            sql = sql[:-4]
            sql += f"order by {order_column} {'desc' if descending else ''}"
            print(f"{sql=}")
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [CreateFinalItemDto(*row) for row in cursor.fetchall()]

        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_items_where_value_between(
        self,
        column_name: str,
        range_min: int | str,
        range_max: int | str,
        descending: bool = False,
    ) -> list[CreateFinalItemDto]:

        try:
            connection = self.connection_pool.get_connection()
            sql = self.select_all_items_info_sql_statement
            sql += (
                f"where {column_name} between '{range_min}' and '{range_max}'"
                f" order by {column_name} {'desc' if descending else ''}"
            )

            print(sql)

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [CreateFinalItemDto(*row) for row in cursor.fetchall()]

        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def fetch_items_where_value_equals(
        self,
        column_name: str,
        variable: str | int | date,
        column_to_order: str,
        descending: bool = False,
    ) -> list[CreateFinalItemDto]:

        try:
            connection = self.connection_pool.get_connection()
            sql = self.select_all_items_info_sql_statement
            sql += f"where {column_name} = '{variable}' order by {column_to_order} {'desc' if descending else ''}"
            print(f'{sql=}')
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [CreateFinalItemDto(*row) for row in cursor.fetchall()]

        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def get_all_items_order_by(
        self, value: str | None, descending: bool = False
    ) -> list[CreateFinalItemDto]:
        match value:
            case "Item name":
                return self.fetch_items_order_by(
                    column_name="f.name", descending=descending
                )

            case "Finding_date":
                return self.fetch_items_order_by(
                    column_name="f.finding_date", descending=descending
                )

            case "Addition date":
                return self.fetch_items_order_by(
                    column_name="f.addition_date", descending=descending
                )

            case "Quantity":
                return self.fetch_items_order_by(
                    column_name="f.addition_date", descending=descending
                )

            case "Finder name":
                return self.fetch_items_order_by(
                    column_name="fd.name", descending=descending
                )

            case "Locality name":
                return self.fetch_items_order_by(
                    column_name="l.name", descending=descending
                )

            case "Location name":
                return self.fetch_items_order_by(
                    column_name="ll.name", descending=descending
                )

            case "Material name":
                return self.fetch_items_order_by(
                    column_name="m.name", descending=descending
                )

            case "Epoch name":
                return self.fetch_items_order_by(
                    column_name="d.name", descending=descending
                )

            case "Year":
                return self.fetch_items_order_by(
                    column_name="d.year", descending=descending
                )

            case _:
                return self.fetch_items_order_by(
                    column_name="f.id", descending=descending
                )

    def get_all_item_where_value_between(
        self,
        value: str,
        range_min: int | str | date,
        range_max: int | str | date,
        descending: bool = False,
    ) -> list[CreateFinalItemDto]:

        match value:
            case "Quantity":
                return self.fetch_items_where_value_between(
                    "f.quantity", range_min, range_max, descending
                )

            case "Finding_date":
                return self.fetch_items_where_value_between(
                    "f.finding_date", range_min, range_max, descending
                )

            case "Year":
                return self.fetch_items_where_value_between(
                    "d.year", range_min, range_max, descending
                )

            case "Latitude":
                return self.fetch_items_where_value_between(
                    "ll.latitude", range_min, range_max, descending
                )

            case "Longitude":
                return self.fetch_items_where_value_between(
                    "ll.longitude", range_min, range_max, descending
                )

    def get_all_item_where_value_equals(
        self,
        value: str,
        variable: str | int | date,
        column_to_order: str,
        descending: bool,
    ) -> list[CreateFinalItemDto]:

        match value:
            case "Item name":
                print(f'{variable=}')
                return self.fetch_items_where_value_equals(
                    column_name="f.name",
                    variable=variable,
                    column_to_order=column_to_order,
                    descending=descending,
                )

            case "Finder name":
                return self.fetch_items_where_value_equals(
                    column_name="fd.name",
                    variable=variable,
                    column_to_order=column_to_order,
                    descending=descending,
                )

            case "Locality name":
                return self.fetch_items_where_value_equals(
                    column_name="l.name",
                    variable=variable,
                    column_to_order=column_to_order,
                    descending=descending,
                )

            case "Location name":
                return self.fetch_items_where_value_equals(
                    column_name="ll.name",
                    variable=variable,
                    column_to_order=column_to_order,
                    descending=descending,
                )

            case "Latitude direction":
                return self.fetch_items_where_value_equals(
                    column_name="ll.latitude_direction",
                    variable=variable,
                    column_to_order=column_to_order,
                    descending=descending,
                )

            case "Longitude direction":
                return self.fetch_items_where_value_equals(
                    column_name="ll.longitude_direction",
                    variable=variable,
                    column_to_order=column_to_order,
                    descending=descending,
                )

            case "Material name":
                return self.fetch_items_where_value_equals(
                    column_name="m.name",
                    variable=variable,
                    column_to_order=column_to_order,
                    descending=descending,
                )

            case "Epoch name":
                return self.fetch_items_where_value_equals(
                    column_name="d.name",
                    variable=variable,
                    column_to_order=column_to_order,
                    descending=descending,
                )

            case "Year":
                return self.fetch_items_where_value_equals(
                    column_name="d.year",
                    variable=variable,
                    column_to_order=column_to_order,
                    descending=descending,
                )

    # def get_all_items_order_by_name(self, descending: bool) -> list[CreateFinalItemDto]:
    #     return self.fetch_items_order_by(column_name="f.name", descending=descending)
    #
    # def get_all_items_order_by_addition_date(
    #     self, descending: bool
    # ) -> list[CreateFinalItemDto]:
    #     return self.fetch_items_order_by(
    #         column_name="f.addition_date", descending=descending
    #     )
    #
    # def get_all_items_order_by_quantity(
    #     self, descending: bool
    # ) -> list[CreateFinalItemDto]:
    #     return self.fetch_items_order_by(
    #         column_name="f.quantity", descending=descending
    #     )
    #
    # def get_all_items_order_by_finder_name(
    #     self, descending: bool
    # ) -> list[CreateFinalItemDto]:
    #     return self.fetch_items_order_by(column_name="fd.name", descending=descending)
    #
    # def get_all_items_order_by_locality_name(
    #     self, descending: bool
    # ) -> list[CreateFinalItemDto]:
    #     return self.fetch_items_order_by(column_name="l.name", descending=descending)
    #
    # def get_all_items_order_by_location_name(
    #     self, descending: bool
    # ) -> list[CreateFinalItemDto]:
    #     return self.fetch_items_order_by(column_name="ll.name", descending=descending)
    #
    # def get_all_items_order_by_material_name(
    #     self, descending: bool
    # ) -> list[CreateFinalItemDto]:
    #     return self.fetch_items_order_by(column_name="m.name", descending=descending)
    #
    # def get_all_items_order_by_epoch_name(
    #     self, descending: bool
    # ) -> list[CreateFinalItemDto]:
    #     return self.fetch_items_order_by(column_name="d.name", descending=descending)
    #
    # def get_all_items_order_by_year(self, descending: bool) -> list[CreateFinalItemDto]:
    #     return self.fetch_items_order_by(column_name="year", descending=descending)
