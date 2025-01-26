from .package import *
from data.user import User

@personal_acc_blueprint.route("/login", methods=["GET", "POST"])
def login():
    nxt_redir = lambda: redirect("/personal_page")
    if flask_login.current_user.is_authenticated:
        return nxt_redir()
    form = LoginForm()
    render_err = lambda msg: render_template("login.html", message=msg, form=form)
    if form.validate_on_submit():
        with db_session.create_session() as session:
            current_user = session.query(User).filter(User.login == form.login.data).first()
            if not current_user:
                return render_err("Пользователя с таким логином не существует")
            if not current_user.check_password(form.password.data):
                return render_err("Пароль неккоректен")
            login_user(current_user, remember=form.remember_me.data)
            return nxt_redir()
    return render_template("login.html", title="Вход", form=form)
