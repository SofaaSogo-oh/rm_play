from .package import *
from data.personal_data import PersonalData
from .forms import PersonalDataForm

@personal_acc_blueprint.route("/personal_page", methods=["GET", "POST"])
def personal_page():
    form = PersonalDataForm()
    return render_template("personal_page.html", title="foo", form=form)
