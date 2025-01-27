from .package import *
from data.personal_data import PersonalData
from data.client_view import PersonView
from .forms import PersonalDataForm

@personal_acc_blueprint.route("/personal_page", methods=["GET", "POST"])
def personal_page():
    if not flask_login.current_user.is_authenticated:
        return redirect("/register")
    curr_id = flask_login.current_user.id
    personal_data = None
    with db_session.create_session() as session:
        personal_data  = session.query(PersonView).get(curr_id)
    return render_template("personal_page.html", personal_data=personal_data)

@personal_acc_blueprint.route("/edit_personal_data", methods=["GET", "POST"])
def edit_personal_data():
    if not flask_login.current_user.is_authenticated:
        return redirect("/register")
    curr_id = flask_login.current_user.id
    curr_user = flask_login.current_user
    form = PersonalDataForm()
    render_page = lambda msg = None: render_template("edit_personal_data.html", message=msg, form=form)
    personal_data = None
    if form.validate_on_submit():
        with db_session.create_session() as session:
            personal_data = session.query(PersonalData).filter(PersonalData.user_id == curr_id).first()
            try: 
                new_data = False
                if personal_data is None:
                    personal_data = PersonalData()
                    personal_data.user = curr_user
                    new_data = True
                personal_data.first_name = form.first_name.data
                personal_data.last_name = form.last_name.data
                personal_data.middle_name = form.middle_name.data
                personal_data.phone_number = form.phone_number.data
                personal_data.date_of_birth = form.date_of_birth.data
                if new_data: session.add(personal_data)
                session.commit()
                return render_page("Все окей!")
            except IntegrityError as e:
                return render_page(f"Что-тт пошло не так: {e}")

    return render_page()
    
