from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from config.database import SessionLocal
from fastapi.responses import RedirectResponse
from fastapi.responses import JSONResponse


from fastapi.responses import HTMLResponse
from controllers.User.Register import RegisterController
from controllers.User.Auth import AuthController
from controllers.User.Info import Info
from helpers.message import get_flash

from controllers.User.Assistant import AssistantController




router = APIRouter(
    tags=["Users"]
)

# DB dependency (agar yaha use karna ho)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET All Users
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return {"message": "Users route working 🚀"}

# GET Single User
# @router.get("/{user_id}")
# def get_user(user_id: int, db: Session = Depends(get_db)):
#     return {"user_id": user_id}



# Register

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    flash_message = get_flash(request)
    return RegisterController.register_page_with_flash(
        request,
        flash_message
    )


@router.post("/register")
def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    form_data = {
        "name": name,
        "email": email,
        "password": password
    }

    return RegisterController.register_user(request, form_data)



@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    flash_message = get_flash(request)
    return AuthController.login_page_with_flash(
        request,
        flash_message
    )


@router.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    form_data = {
        "email": email,
        "password": password
    }

    return AuthController.login_user(request, form_data)


@router.get("/logout")
def logout(request: Request):
    return AuthController.logout(request)


# EndAuth 

# UserDetails Start

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login", status_code=302)

    flash_message = get_flash(request)
    return Info.dashboard(request, flash_message)


# AssistantController
# Render assistant page
@router.get("/assistant")
async def assistant_page(request: Request):
    return await AssistantController.assistant_page(request)


@router.post("/assistant")
async def assistant_command(command: str = Form(...)):
    result = await AssistantController.process_command(command)
    return JSONResponse(result)