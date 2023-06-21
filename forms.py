from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField,PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[Email('Некорректная почта')])
    psw = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4,max=100)])
    remember = BooleanField('Запомнить', default=False)
    sumbit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=4,max=20)])
    email = StringField('Email:', validators=[Email('Некорректная почта')])
    psw = PasswordField('Пароль', validators=([DataRequired(), Length(min=4, max=20)]))
    psw2 = PasswordField('Повтор пароля', validators=([DataRequired(),EqualTo('psw', message='Пароли не совпадают')]))
    register = SubmitField('Регистрация')







