from flask_restful import Resource, abort
from data import db_session
from flask import jsonify
from api.parsers.reg_login_parser import reg_login_parser
from data.user import User

class PersonalData(Resource):
    def post(self):
        args = reg_login_parser.parse_args()
        

    def get(self):
        args = reg_login_parser.parse_args()