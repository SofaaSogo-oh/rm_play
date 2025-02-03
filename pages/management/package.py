from flask import Blueprint, render_template, redirect, url_for, request
from data import db_session
import flask_login
from flask_login import login_user, login_required
from sqlalchemy.exc import IntegrityError
import sqlalchemy as sa
from sqlalchemy import select 

management_blueprint = Blueprint("management", __name__,
                  template_folder="template")