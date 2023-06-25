from datetime import datetime

from sqlalchemy import *

from app.database import db, id_column


class {{ name_camel }}(db.Model):
    __tablename__ = "{{ name }}"

    id = id_column()
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    {% for col in cols %}{{ col[0] }} = Column({{ col[1] }})
    {% endfor %}

