from data.db_session import SqlAlchemyBase
import sqlalchemy as sa
from data.views import *
from data.user import User
from data.client import Client
from data.personal_data import PersonalData

class ClientView(SqlAlchemyBase):
    __table__ = view(
        "client_view",
        SqlAlchemyBase.metadata,
        sa.select(
            User.id,
            User.login,
            User.register_date
        ).select_from(User.__table__.join(Client.__table__)))

class PersonClientView(SqlAlchemyBase):
    __table__ = view(
        "client_view",
        SqlAlchemyBase.metadata,
        sa.select(
            User.id,
            User.login,
            User.register_date,
            PersonalData.first_name,
            PersonalData.last_name,
            PersonalData.middle_name,
            PersonalData.date_of_birth,
            PersonalData.phone_namber,
        ).select_from(User.__table__.join(Client.__table__).join(PersonalData.__table__)))