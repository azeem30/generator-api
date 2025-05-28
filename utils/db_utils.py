from dbutils.pooled_db import PooledDB
import pymysql
from config import DB_CONFIG

def create_db_pool():
    """Create and Return a Database connection pool for MySQL"""
    return PooledDB(
        creator = pymysql,
        maxconnections = 10,
        mincached = 2,
        host = DB_CONFIG["HOST"],
        port = DB_CONFIG["PORT"],
        user = DB_CONFIG["USER"],
        password = DB_CONFIG["PASSWORD"],
        database = DB_CONFIG["DATABASE"],
        cursorclass = pymysql.cursors.DictCursor,
        ping = 1,
    )

def get_db_connection(pool):
    """Get a connection from the pool"""
    return pool.connection()
