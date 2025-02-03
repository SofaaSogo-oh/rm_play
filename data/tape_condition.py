from sqlalchemy.orm import Mapped, mapped_column

from data.db_session import SqlAlchemyBase

from data.tape import Tape
from data.store import Store
from data.rent import Rent
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship

class TapeCondition(SqlAlchemyBase):
    __tablename__ = "table_condition"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    cond_begin: Mapped[datetime]
    cond_end: Mapped[datetime | None]

    tape_id: Mapped[int | None] = mapped_column(sa.ForeignKey("tape.id"))
    tape: Mapped[Tape] = relationship()

    store_id: Mapped[int | None] = mapped_column(sa.ForeignKey("store.id"))
    store: Mapped[Store] = relationship()

    rent_id: Mapped[int | None] = mapped_column(sa.ForeignKey("rent.id"))
    rent: Mapped[Rent] = relationship()

