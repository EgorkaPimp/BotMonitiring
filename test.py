from fastapi import FastAPI
import asyncpg

app = FastAPI()

# Конфиг подключения
DB_CONFIG = {
    "user": "myuser",
    "password": "mypassword",
    "database": "mydatabase",
    "host": "127.0.0.1",  # или IP сервера
    "port": "5432"
}

# Функция подключения
async def get_connection():
    return await asyncpg.connect(**DB_CONFIG)

@app.get("/get_data/")
async def get_data(id: int):
    conn = await get_connection()
    rows = await conn.fetch("SELECT * FROM mytable WHERE id = $1;", id)
    await conn.close()
    return [dict(r) for r in rows]