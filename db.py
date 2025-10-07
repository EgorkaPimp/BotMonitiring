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

async def get_wish():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT * FROM wishes;"))
            rows = [dict(row) for row in result.mappings().all()]
            return rows
    except Exception as e:
        print("DB ERROR:", e)
        return []
    
async def del_wish(wish_id: int):
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT * FROM wishes WHERE id = :id"), 
                                        {"id": wish_id})
            wish = result.mappings().first()
            if not wish: 
                return None
            await conn.execute(text("DELETE FROM wishes WHERE id = :id"), 
                               {"id": wish_id})
            await conn.commit()
            return {"success": True, "wish_id": wish_id}
    except Exception as e:
        print("DB ERROR:", e)
        return []
    
async def get_every_waste():
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT * FROM every_waste;"))
            rows = [dict(row) for row in result.mappings().all()]
            return rows
    except Exception as e:
        print("DB ERROR:", e)
        return []
    

async def get_table():
    try:
        async with engine.connect() as conn:
            # Получаем все расходы
            expenses_result = await conn.execute(text("SELECT category, amount_expenses FROM expenses;"))
            expenses_rows = expenses_result.mappings().all()

            # Превращаем в словарь {category: amount_expenses}
            expenses = {e["category"]: e["amount_expenses"] for e in expenses_rows}

            # Получаем все планы
            plans_result = await conn.execute(text("SELECT category, amount_money FROM plan_spending;"))
            plans_rows = plans_result.mappings().all()

            # Превращаем в словарь {category: amount_money}
            plans = {p["category"]: p["amount_money"] for p in plans_rows}

            # Формируем итоговый список
            comparison = []
            all_categories = set(expenses.keys()) | set(plans.keys())

            for cat in all_categories:
                spent = expenses.get(cat, 0)
                plan = plans.get(cat, 0)
                remaining = plan - spent
                comparison.append({
                    "category": cat,
                    "spent": spent,
                    "plan": plan,
                    "remaining": remaining
                })

            return comparison

    except Exception as e:
        print("DB ERROR:", e)
        return []