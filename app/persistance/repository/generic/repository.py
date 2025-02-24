from typing import Any, Type
from datetime import datetime, date
from mysql.connector.pooling import MySQLConnectionPool, Error
import logging
from dataclasses import dataclass, field
import inflection
import binascii

logging.basicConfig(level=logging.INFO)


@dataclass
class CrudRepository:
    connection_pool: MySQLConnectionPool
    entity: type
    entity_type: Type[Any] = field(init=False)

    def __post_init__(self):
        self.entity_type = type(self.entity())

    def insert(self, item: Any) -> int:
        print(f"{self._columns_names_for_insert()=}")
        print(f"{self._column_values_for_insert(item)=}")

        if equal_item_id := self.find_item_id(item):
            print(f"{equal_item_id=}")
            return equal_item_id

        try:
            sql = f"""
                insert into {self._table_name()} ({self._columns_names_for_insert()})
                values ({self._column_values_for_insert(item)});
            """
            connection = self.connection_pool.get_connection()
            print(f"{connection=}")
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                return cursor.lastrowid
        except Error as err:

            logging.error(err)
            connection.rollback()

        finally:
            if connection.is_connected():

                cursor.close()
                connection.close()

    def insert_many(self, items: list[Any]) -> list[int]:

        try:
            values = ", ".join([self._column_values_for_insert(item) for item in items])
            sql = f"""
                insert into {self._table_name()} ({self._columns_names_for_insert()})
                values ({values});
            """
            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                return self.find_last_n(len(items))
        except Error as err:
            logging.error(err)
            connection.rollback()

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update(self, old_item: Any, updated_item: Any) -> int:

        if equal_item_id := self.find_item_id(updated_item):
            print(f"{equal_item_id=}")
            return equal_item_id
        try:

            old_item_id = self.find_item_id(old_item)
            print(f'{old_item_id=}')

            print(f'{self._table_name()=}')
            sql = f"update {self._table_name()} set {self._column_names_and_values_for_update(updated_item)} where id={old_item_id}"
            print(f'{self._field_names()=}')
            print(f'{sql=}')
            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                return old_item_id
        except Error as err:
            logging.error(err)
            connection.rollback()

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete(self, item_id: int) -> int:

        if not item_id or not self._contains_id(item_id):
            raise ValueError("Cannot delete not existing item")
        try:
            sql = f"delete from {self._table_name()} where id = {item_id}"

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                return item_id
        except Error as err:
            logging.error(err)
            connection.rollback()

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def delete_all(self) -> list[int]:
        try:
            all_ids = self._find_all_ids()
            sql = f"delete from {self._table_name()} where id > 0"

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()
                return all_ids
        except Error as err:
            logging.error(err)
            connection.rollback()

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def drop_table(self):
        try:
            print(f" {self._table_name()=}")
            sql = f" drop table {self._table_name()}"
            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                connection.commit()

        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def find_all(self) -> list[Any]:
        try:
            sql = f" select * from ({self._table_name()}) "
            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [self.entity(*row) for row in cursor.fetchall()]
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def find_one(self, item_id: int) -> Any:
        try:
            sql = f" select * from ({self._table_name()}) where id = {item_id}"
            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                result = cursor.fetchone()

                if not result:
                    raise ValueError("Not found")
                return self.entity(*result)
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def find_last_n(self, n: int) -> list[Any]:
        try:

            sql = f" select * from {self._table_name()} order by id desc limit {n}"

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                return [self.entity(*row) for row in cursor.fetchall()]
        except Error as err:
            logging.error(err)
            connection.rollback()
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def _contains_id(self, item_id: int) -> bool:
        return item_id in self._find_all_ids()

    def _find_all_ids(self) -> list[int]:
        try:
            sql = f" select id  from {self._table_name()}"

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)

                return [row[0] for row in cursor.fetchall()]

        except Error as err:
            logging.error(err)
            connection.rollback()

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def _table_name(self) -> str:
        return inflection.tableize(self.entity_type.__name__)

    def _field_names(self) -> list[str]:
        return self.entity().__dict__.keys()

    def find_item_id(self, item: Any) -> int | None:
        print(f"{self._columns_and_values_for_selecting(item)=}")

        try:
            sql = f" select id  from {self._table_name()} where {self._columns_and_values_for_selecting(item)}"

            connection = self.connection_pool.get_connection()
            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(sql)
                item_id = cursor.fetchall()
                print(f"{item_id=}")

                return item_id[0][0] if item_id else None

        except Error as err:
            logging.error(err)
            connection.rollback()

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def _columns_names_for_insert(self) -> str:
        keys = [key for key in self._field_names() if key.lower() != "id_"]
        return ", ".join(keys)

    @staticmethod
    def _to_str(value: Any) -> str:
        if value is None:
            return "null"
        if isinstance(value, bytes):
            return f"X'{binascii.hexlify(value).decode()}'"
        return (
            f"'{value}'"
            if isinstance(value, (str, date, datetime, bytes))
            else str(value)
        )

    def _column_values_for_insert(self, item: Any) -> str:
        return ", ".join(
            [
                self._to_str(value)
                for keys, value in item.__dict__.items()
                if keys.lower() != "id_"
            ]
        )

    def _column_names_and_values_for_update(self, item: Any) -> str:
        return ", ".join(
            [
                f"{key}={self._to_str(value)}"
                for key, value in item.__dict__.items()
                if key.lower() != "id_"
            ]
        )

    def _columns_and_values_for_selecting(self, item: Any) -> str:
        return " ".join(
            [
                f"{key}={self._to_str(value)} and " if value else f"{key} is null and"
                for key, value in item.__dict__.items()
                if key.lower() not in ["id_", "addition_date"]
            ]
        )[:-4]
