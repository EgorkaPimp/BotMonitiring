from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from db import get_active_users, get_expenses, get_expense_counts, get_wish, del_wish, get_every_waste, get_table
from auth import authenticate
import json
import re
import datetime
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, username: str = Depends(authenticate)):
    users = await get_active_users()
    expenses = await get_expenses()
    expense_counts = await get_expense_counts()
    wishes = await get_wish()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "users": users,
            "expenses": expenses,
            "expense_counts": expense_counts,
            "username": username,
            "wishes": wishes
        }
    )

@router.delete("/wishes/{wish_id}")
async def delete_wish(wish_id: int):
    result = await del_wish(wish_id=wish_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Wish not found")

@router.get("/budget/{user_id}")
async def budget_dashboard(request: Request, user_id: int):
    spending = await get_every_waste(user_id)
    table = await get_table(user_id)

    json_dir = Path.home() / "my_bot" / "SmartBudge_bot" / "json"
    pattern = f"report_{user_id}_*.json"
    files = list(json_dir.glob(pattern))

    reports = []

    if files:
        # Извлекаем дату из имени
        def extract_date(path: Path):
            match = re.search(rf"report_{user_id}_(\d{{4}}-\d{{2}}-\d{{2}})\.json", path.name)
            if match:
                try:
                    return datetime.date.fromisoformat(match.group(1))
                except ValueError:
                    return datetime.date.min
            return datetime.date.min

        # Сортируем файлы (новые первыми)
        files.sort(key=extract_date, reverse=True)

        # Собираем данные по каждому отчёту
        for f in files:
            with open(f, encoding="utf-8") as json_file:
                report = json.load(json_file)
            date_str = extract_date(f).strftime("%Y-%m-%d")
            monthly_data = [
                {
                    "category": c["name"],
                    "planned": c["planned"],
                    "spent": c["spent"]
                }
                for c in report["budget"]["categories"]
            ]
            reports.append({
                "date": date_str,
                "data": monthly_data
            })

    # Возвращаем шаблон всегда, даже если reports пустой
    return templates.TemplateResponse("users.html", {
        "request": request,
        "spending": spending,
        "table": table,
        "reports": reports  # список всех json'ов, может быть пустым
    })
