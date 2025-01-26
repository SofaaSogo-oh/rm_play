import random
from flask_restful import abort
from data import db_session
from data.user import User


def generate_token():
    session = db_session.create_session()
    token = ''.join([chr(random.randint(44, 90)) for _ in range(random.randint(30, 50))])
    current_user_token = session.query(User).filter(User.token == token).first()
    if current_user_token:
        generate_token()
    return token


def abort_if_token_is_not_correct(id_name, user_token):
    session = db_session.create_session()
    correct_user = session.query(User).filter(User.id_name == id_name,
                                              User.token == user_token).first()
    if not correct_user:
        return abort(404, message="your token or id_name isn't correct")
