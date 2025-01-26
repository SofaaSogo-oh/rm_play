from flask import Flask
from data import db_session
from data.user import User
from flask_restful import Api
from flask_login import LoginManager
from pages import client_register, login

app = Flask(__name__)
app.config["SECRET_KEY"] = "FOOBarGashaIsTheBest"
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with db_session.create_session() as session:
        return session.query(User).get(user_id)

@app.route("/")
def main():
    return "FOO!"

if __name__ == "__main__":
    db_session.global_init("randomp_db")
    app.register_blueprint(client_register.register)
    app.register_blueprint(login.login)
    app.run(debug=True)