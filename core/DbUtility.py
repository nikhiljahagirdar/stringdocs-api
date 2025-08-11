import os
import psycopg
import psycopg.rows
import asyncio
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def get_db_connection():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DB")
    sslmode = os.getenv("POSTGRES_SSLMODE")

    if not all([user, password, host, port, database, sslmode]):
        raise ValueError("One or more PostgreSQL environment variables are not set.")

    db_connection_string = f"host={host} port={port} dbname={database} user={user} password={password} sslmode={sslmode}"
    return await psycopg.AsyncConnection.connect(db_connection_string)


async def execute_query(query, params=None):
    conn = None
    try:
        logger.info(f"Executing query: {query} with  params {params}")
        conn = await get_db_connection()
        async with conn.cursor() as cur:
            await cur.execute(query, params)
        await conn.commit()
        return True
    except Exception as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        if conn:
            await conn.close()


async def fetch_all(query, params=None):
    conn = None
    try:
        conn = await get_db_connection()
        conn.row_factory = psycopg.rows.dict_row
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            rows = await cur.fetchall()
        return rows
    except Exception as e:
        print(f"Error fetching all: {e}")
        return None
    finally:
        if conn:
            await conn.close()


async def fetch_one(query, params=None):
    conn = None
    try:
        conn = await get_db_connection()
        conn.row_factory = psycopg.rows.dict_row
        async with conn.cursor() as cur:
            await cur.execute(query, params)
            row = await cur.fetchone()
        return row
    except Exception as e:
        print(f"Error fetching one: {e}")
        return None
    finally:
        if conn:
            await conn.close()
