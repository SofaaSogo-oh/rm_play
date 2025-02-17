from data.db_session import SqlAlchemyBase
from sqlalchemy import Column, Integer
import sqlalchemy as sa
from data.views import *
from data.tape import Tape
from data.tape_condition import TapeCondition
from data.store import Store
from data.movie import Movie
from data.client import Client
from data.rent import Rent

class AvailableTapes(SqlAlchemyBase):
    __table__ = view(
        "available_tape_view",
        SqlAlchemyBase.metadata,
        sa.select(
            Tape.id.label("tape_id"),
            Store.id.label("store_id"),
            Movie.id.label("movie_id"),
        ).select_from(
            Tape.__table__.
                join(TapeCondition.__table__).
                join(Store.__table__)
        ).where(
            TapeCondition.cond_end == None
        )
    )

    __mapper_args__ = {
        'primary_key': (Tape.id,)
    }

class RentClientTapes(SqlAlchemyBase):
    __table__ = view(
        "rent_client_tapes",
        SqlAlchemyBase.metadata,
        sa.select(
            Tape.id.label("tape_id"),
            Rent.id.label("rent_id"),
            Client.id.label("client_id")
        ).select_from(
            Tape.__table__.
                join(TapeCondition.__table__).
                join(Rent.__table__).
                join(Client.__table__)
        ).where(
            TapeCondition.cond_end == None
        )
    )