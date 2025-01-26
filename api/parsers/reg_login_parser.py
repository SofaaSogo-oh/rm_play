from flask_restful import Resource, abort
from data import db_session
from flask import jsonify
from flask_restful import reqparse


reg_login_parser = reqparse.RequestParser()
reg_login_parser.add_argument("login", required=True)
reg_login_parser.add_argument("password", required=True)