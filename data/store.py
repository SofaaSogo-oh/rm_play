from sqlalchemy.orm import Mapped, mapped_column

from data.db_session import SqlAlchemyBase

class Store(SqlAlchemyBase):
    __tablename__ = "store"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]
    description: Mapped[str | None]
