from mysql.connector.pooling import MySQLConnectionPool
from typing import Self, Any
import os
from dotenv import load_dotenv

load_dotenv()

connection_params = dict(
    pool_name='my_pool',
    pool_size=5,
    pool_reset_session=True,
    host=os.getenv('HOST', default='localhost'),
    database=os.getenv('DATABASE', default='db_1'),
    user=os.getenv('USER',default='user'),
    password=os.getenv('PASSWORD',default='user1234'),
    port=int(os.getenv('PORT',default=3307))

)


class MySqlConnectionPoolBuilder:
    def __init__(self, params:dict[str, Any] = None):
        params = {} if not params else params
        self.pool_config = {
            'pool_name' : 'mysql_connection_pool',
            'pool_size': 5,
            'pool_reset_session': True,
            'host': 'localhost',
            'database': 'db_2',
            'user': 'user',
            'password': 'user1234',
            'port': 3307
        } | params


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


    @classmethod
    def builder(cls) -> Self:
        return cls()


def get_connection_pool():
    return MySqlConnectionPoolBuilder(connection_params).builder().build()


def get_connection_test_pool():
    return MySqlConnectionPoolBuilder().builder().set_port(3308).build()



connection_pool = get_connection_pool()
