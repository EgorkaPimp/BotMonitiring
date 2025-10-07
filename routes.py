from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import get_active_users, get_expenses, get_expense_counts, get_wish, del_wish, get_every_waste, get_table
from auth import authenticate

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

@router.get("/test/")
async def tests(request: Request):
    spending = await get_every_waste()
    table = await get_table()
    
    return templates.TemplateResponse("users.html", {
        "request": request,
        "spending": spending,
        "table": table
        })