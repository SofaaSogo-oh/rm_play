from flask import Blueprint, render_template, redirect
from data import db_session
import flask_login
from flask_login import login_user, login_required
from pages.personal_acc.forms import LoginForm
from sqlalchemy.exc import IntegrityError
import sqlalchemy as sa
from sqlalchemy import select 

personal_acc_blueprint = Blueprint("login", __name__,
                  template_folder="template")