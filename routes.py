from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import get_active_users, get_expenses, get_expense_counts
from auth import authenticate

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, username: str = Depends(authenticate)):
    users = await get_active_users()
    expenses = await get_expenses()
    expense_counts = await get_expense_counts()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "users": users,
            "expenses": expenses,
            "expense_counts": expense_counts,
            "username": username
        }
    )
