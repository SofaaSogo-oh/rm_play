from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ViewCathalog(FlaskForm):
    per_page = IntegerField("Фильмов на странице: ", 
                            validators=[DataRequired(), NumberRange(min=1, max=50)],
                              default=10)
    submit = SubmitField("Применить")
