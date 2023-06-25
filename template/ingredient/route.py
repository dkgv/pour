from flask import Blueprint

from app.features.{{ feature }}.domain import {{ name }}_service

bp = Blueprint("{{ name }}", __name__)


@bp.get("/{{ name }}s")
def get_{{ name }}s():
    return {{ name }}_service.get_{{ name }}s()
