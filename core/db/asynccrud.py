import asyncio
import psycopg
from psycopg.rows import dict_row
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database config (⚠️ Use environment variables in real projects)
DB_CONFIG = {
    "host": "db-postgresql-blr1-stringdocs-do-user-23264149-0.i.db.ondigitalocean.com",
    "port": 25060,
    "dbname": "stringdocs",
    "user": "doadmin",
    "password": "AVNS_BiF3gopbW8oOjMUxUYg",
    "sslmode": "require",
}


def get_dsn():
    return " ".join(f"{k}={v}" for k, v in DB_CONFIG.items())


# --- ASYNC CRUD FUNCTIONS ---


async def select_all(table):
    async with await psycopg.AsyncConnection.connect(
        get_dsn(), row_factory=dict_row
    ) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM {table}")
            return await cur.fetchall()


async def select_where(table, where_clause, params):
    query = f"SELECT * FROM {table} WHERE {where_clause}"
    async with await psycopg.AsyncConnection.connect(
        get_dsn(), row_factory=dict_row
    ) as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            return await cur.fetchall()


async def insert(table, data: dict):
    keys = ", ".join(data.keys())
    placeholders = ", ".join(f"%({k})s" for k in data)
    query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders}) RETURNING *"
    logger.info(query)

    async with await psycopg.AsyncConnection.connect(
        get_dsn(), row_factory=dict_row
    ) as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, data)
            return await cur.fetchone()


async def update(table, data: dict, where_clause, where_params: dict):
    set_clause = ", ".join(f"{k} = %({k})s" for k in data)
    query = f"UPDATE {table} SET {set_clause} WHERE {where_clause} RETURNING *"
    async with await psycopg.AsyncConnection.connect(
        get_dsn(), row_factory=dict_row
    ) as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, {**data, **where_params})
            return await cur.fetchone()


async def delete(table, where_clause, params):
    query = f"DELETE FROM {table} WHERE {where_clause} RETURNING *"
    async with await psycopg.AsyncConnection.connect(
        get_dsn(), row_factory=dict_row
    ) as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            return await cur.fetchone()


async def select_where_single(table, where_clause, params):
    query = f"SELECT * FROM {table} WHERE {where_clause}"
    async with await psycopg.AsyncConnection.connect(
        get_dsn(), row_factory=dict_row
    ) as conn:
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            return await cur.fetchone()


async def custom_query_one(query, params=None):
    if params is None:
        params = ()
    async with await psycopg.AsyncConnection.connect(
        get_dsn(), row_factory=dict_row
    ) as conn:
        async with conn.cursor() as cur:
            # Log the query and its parameters for debugging
            logger.info(f"Executing query (one): {query}, Params: {params}")
            await cur.execute(query, params)
            return await cur.fetchone()


async def custom_query_all(query, params=None):
    if params is None:
        params = ()
    async with await psycopg.AsyncConnection.connect(
        get_dsn(), row_factory=dict_row
    ) as conn:
        async with conn.cursor() as cur:
            # Log the query and its parameters for debugging
            logger.info(f"Executing query (all): {query}, Params: {params}")
            await cur.execute(query, params)
            return await cur.fetchall()
