import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from data.db_session import SqlAlchemyBase
from data.client import Client

class Rent(SqlAlchemyBase):
    __tablename__ = "rent"

    id: Mapped[int] = mapped_column(primary_key=True)

    client_id: Mapped[int] = mapped_column(sa.ForeignKey("client.id"))
    client: Mapped[Client] = relationship()
