from flask_restful import Resource, abort
from data import db_session
from flask import jsonify
from api.parsers.reg_login_parser import reg_login_parser
from data.user import User
from api.token import generate_token

def abort_if_user_not_found(id_name):
    session = db_session.create_session()
    current_user = session.query(User).filter(id_name == User.login).first()
    if not current_user:
        abort(404, message=f"User with {id_name} login not found")

def abort_if_user_found(id_name):
    session = db_session.create_session()
    current_user = session.query(User).filter(User.login == id_name).first()
    if current_user:
        abort(404, message=f"User {id_name} is already registered")

def check_password_for_args(id_name, password):
    session = db_session.create_session()
    current_user = session.query(User).filter(User.login == id_name).first()
    current_user.check_password(password)

class UserReg(Resource):
    def post(self):
        args = reg_login_parser.parse_args()
        
        abort_if_user_found(args["login"])
        
        session = db_session.create_session()
        current_user = User()

        current_user.login = args["login"]
        current_user.token = generate_token()
        current_user.set_password(args["password"])

        session.add(current_user)
        session.commit()

        response = {"message": "success",
                    "token": current_user.token}
        return jsonify(response)
    

class UserLogin(Resource):
    def post(self):
        args = reg_login_parser.parse_args()

        abort_if_user_not_found(args["login"])

        session = db_session.create_session()
        current_user = session.query(User).filter(User.login == args["login"]).first()
        current_user.check_password(args["password"])

        response = {
            "message": "success",
            "token": current_user.token
        }  
        return jsonify(response)