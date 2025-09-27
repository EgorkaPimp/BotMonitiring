from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

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
        print("DB ERROR:", e)  # выведет ошибку в консоль
        return {"error": str(e)}

@app.get("/users")
async def connections():
    data = await get_active_users()
    text_data = "\n".join(str(row) for row in data)
    return PlainTextResponse(content=text_data)