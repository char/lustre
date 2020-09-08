from .global_state import current_request
from .templating import template_global


def flash(category: str, message: str):
    flashes = current_request().session.setdefault("flashes", [])
    flashes.append((category, message))


@template_global("get_flashes")
def get_and_clear_flashes():
    request = current_request()

    flashes = request.session.get("flashes")
    request.session["flashes"] = []

    return flashes
