import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from data.db_session import SqlAlchemyBase
from data.movie import Movie

class Tape(SqlAlchemyBase):
    __tablename__ = "tape"

    id: Mapped[int] = mapped_column(primary_key=True)
    movie_id: Mapped[int] = mapped_column(sa.ForeignKey("movie.id"))
    movie: Mapped[Movie] = relationship()