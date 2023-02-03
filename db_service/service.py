import asyncio
import os
from dataclasses import dataclass
import asyncpg
from dotenv import load_dotenv

DB_HOST = os.getenv('DB_HOST', None)
DB_PORT = '5432'
DB_USER = 'postgres'
DB_PASS = 'wsiz#1234'
DB_DB = 'postgres'


async def create_pool():
    print(f'creating pool for db:{DB_HOST}:{DB_PORT}, db={DB_DB}')
    pool = await asyncpg.create_pool(host=DB_HOST, port=DB_PORT, database=DB_DB, user=DB_USER, password=DB_PASS)
    print(f'pool created')
    return pool


class DbService:
    pool: asyncpg.pool.Pool

    async def initalize(self):
        self.pool = await create_pool()

    async def get_all_users(self) -> list[dict]:
        async with self.pool.acquire() as c:
            rows = await c.fetch('select * from users order by id')
        return [dict(r) for r in rows]


async def run_it():
    db = DbService()
    await db.initalize()

    print(await db.get_all_users())


if __name__ == '__main__':
    load_dotenv()
    asyncio.run(run_it())
