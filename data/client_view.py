from data.db_session import SqlAlchemyBase
import sqlalchemy as sa
from data.views import *
from data.user import User
from data.client import Client

class ClientView(SqlAlchemyBase):
    __table__ = view(
        "client_view",
        SqlAlchemyBase.metadata,
        sa.select(
            User.id,
            User.login
        ).select_from(User.__table__.join(Client.__table__))
    )