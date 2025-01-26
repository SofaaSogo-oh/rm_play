import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from data.db_session import SqlAlchemyBase

class Movie(SqlAlchemyBase):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    description: Mapped[str | None]