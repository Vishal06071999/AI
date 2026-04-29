from helpers.views import user

class Info:
    @staticmethod
    def dashboard(request, flash_message):
        return user(
            "dashboard",
            {
                "request": request,
                "flash": flash_message,
                "title" : "Dashboard"
            }
        )