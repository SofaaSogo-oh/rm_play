import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_session import SqlAlchemyBase

from data.user import User
from data.role import Role

class Employee(SqlAlchemyBase):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))
    user: Mapped[User] = relationship()
    roles: Mapped[list[Role]] = relationship(secondary="employee_role")