import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from data.db_session import SqlAlchemyBase
from data.movie import Movie

class TapeType(SqlAlchemyBase):
    __tablename__ = "tape_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

class Tape(SqlAlchemyBase):
    __tablename__ = "tape"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(sa.ForeignKey("movie.id"))
    movie: Mapped[Movie] = relationship()
    tape_type_id: Mapped[int] = mapped_column(sa.ForeignKey("tape_type.id"))
    tape_type: Mapped[TapeType] = relationship()
   