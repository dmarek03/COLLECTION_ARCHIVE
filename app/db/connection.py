from mysql.connector.pooling import MySQLConnectionPool
from typing import Self
from dataclasses import dataclass

@dataclass
class MySqlConnectionPoolBuilder:
    pool_config = {
        'pool_name' : 'mysql_connection_pool',
        'pool_size': 5,
        'pool_reset_session': True,
        'host': 'localhost',
        'user': 'user',
        'password': 'user1234',
        'database': 'db_2',
        'port': 3307
    }


    def set_pool_size(self, new_pool_size: int) -> Self:
        self.pool_config['pool_size'] = new_pool_size
        return Self


    def set_user(self, new_user: str) -> Self:
        self.pool_config['new_user'] = new_user
        return Self


    def set_password(self,new_password: str) -> Self:
        self.pool_config['password'] = new_password
        return Self


    def set_database(self, new_db: str) -> Self:
        self.pool_config['database'] = new_db
        return Self


    def set_port(self, new_port: int) -> Self:
        self.pool_config['new_port'] = new_port
        return Self


    def build(self) -> MySQLConnectionPool:
        return MySQLConnectionPool(**self.pool_config)


def get_connection_pool():
    return MySqlConnectionPoolBuilder().build()


def get_connection_test_pool():
    return MySqlConnectionPoolBuilder().set_port(3308).build()
