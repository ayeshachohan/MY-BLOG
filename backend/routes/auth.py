from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.database import db
from backend.models import User
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from fastapi import FastAPI

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Add authentication dependencies and session management

@router.get("/signup", response_class=HTMLResponse)
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
async def post_signup(request: Request, email: str = Form(...), username: str = Form(...), password: str = Form(...)):
    user = db.users.find_one({"email": email})
    if user:
        return templates.TemplateResponse("signup.html", {"request": request, "msg": "Email already registered"})
    
    hashed_password = pwd_context.hash(password)
    new_user = {"email": email, "username": username, "password": hashed_password}
    db.users.insert_one(new_user)
    
    return RedirectResponse(url="/login", status_code=303)
@router.get("/login", response_class=HTMLResponse)
async def get_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def post_login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = db.users.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})
    
    request.session["user_id"] = str(user["_id"])
    return RedirectResponse(url="/dashboard", status_code=303)


@router.get("/logout")
async def logout(request: Request):
    request.session.pop("user_id", None)
    return RedirectResponse(url="/login", status_code=303)
