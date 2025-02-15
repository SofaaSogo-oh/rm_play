from flask import Flask
from data import db_session
from data.user import User
from flask_restful import Api
from flask_login import LoginManager
from pages.personal_acc import *
from pages.management import *
import jinja2, os

app = Flask(__name__)
app.config["SECRET_KEY"] = "FOOBarGashaIsTheBest"
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with db_session.create_session() as session:
        return session.query(User).get(user_id)

@app.route("/", methods=["GET","POST"])
def hh_page():
  return render_template("hh.html", title="RandPlayInfo")

@app.errorhandler(404)
def page_not_found(e):
  return render_template('message.html', 
                         title="Ошибка", 
                         header="404", 
                         message="Страница не найдена"), 404

@app.template_filter('script')
def script(script_path, data=None):
    path, filename = os.path.split(script_path)
    return  jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(data = data)

if __name__ == "__main__":
    app.register_blueprint(personal_acc_blueprint)
    app.register_blueprint(management_blueprint)
    db_session.global_init("randomp_db")
    app.run(debug=True)