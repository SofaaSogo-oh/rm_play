import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.db_session import SqlAlchemyBase

class Role(SqlAlchemyBase):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

class EmployeeRole(SqlAlchemyBase):
    __tablename__ = "employee_role"
    employee_id: Mapped[int] = mapped_column(sa.ForeignKey("employee.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"), primary_key=True)

class Privelege(SqlAlchemyBase):
    __tablename__ = "privelege"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]

class RolePrivelege(SqlAlchemyBase):
    __tablename__ = "role_privelege"
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"), primary_key=True)
    privelege_id: Mapped[int] = mapped_column(sa.ForeignKey("privelege.id"), primary_key=True)
