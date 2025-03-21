from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    username = StringField("Логін", validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Зареєструватися")


class LoginForm(FlaskForm):
    username = StringField("Логін", validators=[DataRequired(), Length(min=4, max=100)])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Увійти")