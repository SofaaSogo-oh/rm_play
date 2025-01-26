import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import DOMAIN
from datetime import date

from data.db_session import SqlAlchemyBase

from data.user import User

phone_number_domain = DOMAIN("phone_num", sa.Text, check="VALUE ~ '^[+]?[0-9]{10,15}$'")


class PersonalData(SqlAlchemyBase):
    __tablename__ = "personal_data"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    user: Mapped[User] = relationship()

    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str]

    phone_namber: Mapped[str] = mapped_column(phone_number_domain)
    date_of_birth: Mapped[date | None]
    address: Mapped[str | None]
