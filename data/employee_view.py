from data.db_session import SqlAlchemyBase
import sqlalchemy as sa
from data.views import *
from data.user import User
from data.role import Privelege, Role, EmployeeRole, RolePrivelege
from data.employee import Employee
from data.personal_data import PersonalData

class UserPriveleges(SqlAlchemyBase):
    __table__ = view(
        "user_privelege_view",
        SqlAlchemyBase.metadata,
        sa.select(
            User.id,
            Privelege.name,
            Privelege.description
        ).select_from(
            User.__table__.
                join(Employee.__table__).
                join(EmployeeRole.__table__).
                join(Role.__table__).
                join(RolePrivelege.__table__).
                join(Privelege.__table__)))
    
    def check_user_privelege(user_id, privelege_name, session):
        return session.query(UserPriveleges).filter(
            (UserPriveleges.id == user_id) & (UserPriveleges.name == privelege_name)
        ).first()