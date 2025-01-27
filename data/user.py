from sqlalchemy import orm
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_restful import abort
from datetime import datetime

from sqlalchemy import UniqueConstraint

from data.db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.role import Role, EmployeeRole

class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    password: orm.Mapped[str]
    register_date: Mapped[datetime]

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if not check_password_hash(self.password, password):
            return abort(404, message="Password isn't correct")
