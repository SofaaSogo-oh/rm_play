from .package import *
from .forms import RegisterForm
from data.client import Client
from data.user import User
import datetime

def convert_error(err: IntegrityError) -> str:
    err_ = str(err)
    if "unique constraint" in err and "user_login_key" in err_:
        return "пользователь с таким логином существует"
    return err_

@personal_acc_blueprint.route("/register", methods=["GET", "POST"])
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
            current_user.register_date = datetime.datetime.now()
            current_client = Client()
            current_client.user = current_user
            session.add(current_user)
            session.add(current_client)
            try:
                session.commit()
            except IntegrityError as e:
                session.rollback() 
                return render_err(f"Ошибка добавления пользователя: {convert_error(str(e))}")
            login_user(current_user, remember=False)
            return nxt_redir()
    return render_template("register.html", title="Регистрация", form=form)