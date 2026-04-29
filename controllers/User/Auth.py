from fastapi.responses import RedirectResponse
from passlib.hash import bcrypt
from model.super_model import SuperModel
from helpers.message import flash
from helpers.views import user

class AuthController:

    # -----------------------
    # Login Page
    # -----------------------
    @staticmethod
    def login_page_with_flash(request, flash_message):
        return user("login",
            {
                "request": request,
                "flash": flash_message,
                'title' : 'Login'
            }
        )

    # -----------------------
    # Login Process
    # -----------------------
    @staticmethod
    def login_user(request, form_data):

        email = form_data.get("email")
        password = form_data.get("password")

        if not email or not password:
            flash(request, "Email and Password required", "error")
            return RedirectResponse(url="/login", status_code=302)

        user = SuperModel.get_single_record("users", {"email": email})

        if not user:
            flash(request, "Invalid Email or Password", "error")
            return RedirectResponse(url="/login", status_code=302)

        # Password Verify
        # if not bcrypt.verify(password, user["password"]):
        #     flash(request, "Invalid Email or Password", "error")
        #     return RedirectResponse(url="/login", status_code=302)

        # Session set
        request.session["user_id"] = user["id"]
        request.session["user_name"] = user["name"]

        flash(request, f"Welcome {user['name']} 🎉", "success")
        return RedirectResponse(url="/dashboard", status_code=302)

    # -----------------------
    # Logout
    # -----------------------
    @staticmethod
    def logout(request):
        request.session.clear()
        flash(request, "Logged out successfully", "success")
        return RedirectResponse(url="/login", status_code=302)