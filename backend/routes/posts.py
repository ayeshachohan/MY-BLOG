from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.database import db
from bson import ObjectId
from starlette.templating import Jinja2Templates
from fastapi import status

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    user_id = request.session.get("user_id")
    if user_id:
        user_posts = db.posts.find({"author_id": ObjectId(user_id)})
        posts = list(user_posts)
        for post in posts:
            post["_id"] = str(post["_id"])
        return templates.TemplateResponse("dashboard.html", {"request": request, "posts": posts})
    return RedirectResponse(url="/login", status_code=303)

@router.post("/dashboard")
async def create_post(request: Request, title: str = Form(...), content: str = Form(...)):
    user_id = request.session.get("user_id")
    if user_id:
        new_post = {"title": title, "content": content, "author_id": ObjectId(user_id)}
        db.posts.insert_one(new_post)
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@router.get("/posts/{post_id}", response_class=HTMLResponse)
async def get_post_detail(request: Request, post_id: str):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if post:
        post["_id"] = str(post["_id"])
        return templates.TemplateResponse("post_detail.html", {"request": request, "post": post})
    return RedirectResponse(url="/dashboard", status_code=303)

@router.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def get_edit_post(request: Request, post_id: str):
    post = db.posts.find_one({"_id": ObjectId(post_id)})
    if post:
        post["_id"] = str(post["_id"])
        return templates.TemplateResponse("edit_post.html", {"request": request, "post": post})
    return RedirectResponse(url="/dashboard", status_code=303)

@router.post("/posts/{post_id}/edit")
async def post_edit_post(request: Request, post_id: str, title: str = Form(...), content: str = Form(...)):
    user_id = request.session.get("user_id")
    if user_id:
        db.posts.update_one({"_id": ObjectId(post_id)}, {"$set": {"title": title, "content": content}})
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

@router.post("/posts/{post_id}/delete")
async def delete_post(request: Request, post_id: str):
    user_id = request.session.get("user_id")
    if user_id:
        db.posts.delete_one({"_id": ObjectId(post_id)})
        return RedirectResponse(url="/dashboard", status_code=303)
    return RedirectResponse(url="/login", status_code=303)
