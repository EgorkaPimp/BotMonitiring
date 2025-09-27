from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=False)


async def get_active_users():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT * FROM users;"))
            rows = [dict(row) for row in result.mappings().all()]
            return rows
    except Exception as e:
        print("DB ERROR:", e)
        return []


async def get_expenses():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT COUNT(*) FROM shares;"))
            rows = result.fetchall()
            return rows[0][0] if rows else 0
    except Exception as e:
        print("DB ERROR:", e)
        return 0


async def get_expense_counts():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT COUNT(*) FROM expenses;"))
            rows = result.fetchall()
            return rows[0][0] if rows else 0
    except Exception as e:
        print("DB ERROR:", e)
        return 0
