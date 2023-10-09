import os
import uuid
from typing import Callable, List, Type

from alembic import command
from flask import Flask
from flask import current_app as app
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import Query

db = SQLAlchemy(app._get_current_object())


def id_column() -> Column:
    if db.engine.name == "sqlite":
        return Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    return Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


def automigrate(app: Flask) -> None:
    migrate = Migrate()
    migrate.init_app(app, db)

    if not os.path.exists("migrations"):
        command.init(migrate.get_config(), "migrations", template="flask")

    command.upgrade(migrate.get_config(), "head")


def query_with_filter(
    model: Type[db.Model], filter: Callable[[db.Model], bool], first_only: bool = False
) -> List[db.Model]:
    filtered_query = Query(model, model.query.session).filter(filter)

    if first_only:
        return filtered_query.first()

    return filtered_query.all()
