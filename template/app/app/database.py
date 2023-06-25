import uuid
from typing import Callable, List, Type

from flask import current_app as app
from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import Query

db = SQLAlchemy(app._get_current_object())


def id_column() -> Column:
    if db.engine.name == "sqlite":
        return Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def automigrate() -> None:
    db.create_all()


def query_with_filter(
    model: Type[Model], filter: Callable[[Model], bool], first_only: bool = False
) -> List[Model]:
    filtered_query = Query(model, model.query.session).filter(filter)

    if first_only:
        return filtered_query.first()

    return filtered_query.all()
