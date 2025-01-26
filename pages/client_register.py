from flask import Blueprint, render_template, redirect
from data.user import User
from data.client import Client
from data import db_session
import flask_login
from flask_login import login_user
from pages.forms import RegisterForm
from sqlalchemy.exc import IntegrityError

register_blueprint = Blueprint("register", __name__,
                     template_folder="template")

def convert_error(err: IntegrityError) -> str:
    err_ = str(err)
    if "unique constraint" in err and "user_login_key" in err_:
        return "пользователь с таким логином существует"

@register_blueprint.route("/client/register", methods=["GET", "POST"])
def register():
    nxt_redir = lambda: redirect("/personal_page")
    if flask_login.current_user.is_authenticated:
        return nxt_redir()
    form = RegisterForm()
    render_err = lambda msg: render_template("register.html", message=msg, form=form)
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_err("Пароли должны совпадать")
        with db_session.create_session() as session:
            current_user = User()
            current_user.login = form.login.data
            current_user.set_password(form.password.data)
            session.add(current_user)
            current_client = Client()
            current_client.user = current_user
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback() 
                return render_err(f"Ошибка добавления пользователя: {convert_error(str(e))}")
            login_user(current_user, remember=False)
            return nxt_redir()
    return render_template("register.html", title="Регистрация", form=form)
