from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from config.config import Config

# Templates root folder
templates = Jinja2Templates(directory="views")

# Global PROJECT variable har template me available
templates.env.globals['PROJECT'] = Config.PROJECT


def admin(template_name: str, context: dict, role: str = "Admin"):
    request = context.get("request")
    if not request:
        raise ValueError("Request object is required in context dictionary")

    # Optionally handle extra context if passed
    extra = context.get("extra", None)
    if extra:
        context.update(extra)

    template_path = f"{role}/{template_name}.html"
    return templates.TemplateResponse(template_path, context)

def user(template_name: str, context: dict, role: str = "User"):
    request = context.get("request")
    if not request:
        raise ValueError("Request object is required in context dictionary")

    # Optionally handle extra context if passed
    extra = context.get("extra", None)
    if extra:
        context.update(extra)

    template_path = f"{role}/{template_name}.html"
    return templates.TemplateResponse(template_path, context)


def site(template_name: str, context: dict, role: str = "Site"):
    request = context.get("request")
    if not request:
        raise ValueError("Request object is required in context dictionary")

    # Optionally handle extra context if passed
    extra = context.get("extra", None)
    if extra:
        context.update(extra)

    template_path = f"{role}/{template_name}.html"
    return templates.TemplateResponse(template_path, context)