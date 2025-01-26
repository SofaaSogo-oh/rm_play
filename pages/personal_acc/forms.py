from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password_again = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироватьтся")


class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомните меня")
    submit = SubmitField("Войти")

class PersonalDataForm(FlaskForm):
    first_name = StringField("Имя", validators=[DataRequired()])
    last_name = StringField("Фамилия", validators=[DataRequired()])
    middle_name = StringField("Отчество")
    phone_number = StringField("Номер телефона")
    date_of_birth = DateField("Дата рождения")

    submit = SubmitField("Внести изменения")