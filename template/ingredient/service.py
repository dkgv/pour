from typing import Callable, List

from app.features.{{ feature }}.models.{{ name }} import {{ name_camel }}
from app import database as db


def get_{{ name }}s(filter: Callable[[{{ name_camel }}], bool]) -> List[{{ name_camel }}]:
    return db.query_with_filter({{ name_camel }}, filter)


def get_first_{{ name }}(filter: Callable[[{{ name_camel }}], bool]) -> {{ name_camel }}:
    return db.query_with_filter({{ name_camel }}, filter, first_only=True)


def get_{{ name }}s() -> List[{{ name_camel }}]:
    return get_{{ name }}s(lambda x: True)
