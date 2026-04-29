from fastapi.responses import RedirectResponse
from model.super_model import SuperModel
from passlib.hash import bcrypt
from helpers.message import flash
from helpers.views import user




class RegisterController:

    @staticmethod
    def register_page_with_flash(request, flash_message):
        return user(
            "register",
            {
                "request": request,
                "flash": flash_message,
                "title" : "Register"
            }
        )

    @staticmethod
    def register_user(request, form_data):

        name = form_data.get("name")
        email = form_data.get("email")
        password = form_data.get("password")

        if not name or not email or not password:
            flash(request, "All fields are required", "error")
            return RedirectResponse(url="/register", status_code=302)

        user = SuperModel.get_single_record("users", {"email": email})

        if user:
            flash(request, "Email already exists", "error")
            return RedirectResponse(url="/register", status_code=302)

        # hashed_password = bcrypt.hash(password)

        SuperModel.add("users", {
            "name": name,
            "email": email,
            "password": password
        })

        flash(request, "Registration Successful 🎉", "success")
        return RedirectResponse(url="/register", status_code=302)