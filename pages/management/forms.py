from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired, NumberRange


class ViewCathalog(FlaskForm):
    per_page = IntegerField(
        "Фильмов на странице: ",
        validators=[DataRequired(), NumberRange(min=1, max=50)],
        default=10,
    )
    submit = SubmitField("Применить")


class MovieEd(FlaskForm):
    name = StringField("Название фильма", validators=[DataRequired()])
    description = TextAreaField("Описание фильма")
    price = FloatField("Цена", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Готово!")
