def flash(request, message, category="success"):
    request.session["flash"] = {
        "message": message,
        "category": category
    }


def get_flash(request):
    data = request.session.pop("flash", None)
    return data