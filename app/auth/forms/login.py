import string

from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, BooleanField, SubmitField, ValidationError

alphabet = string.ascii_letters + string.digits + '_'


class LoginForm(FlaskForm):
    class Meta:
        csrf = False

    login = StringField(
        label='Логин',
        validators=[validators.DataRequired(message='Это обязательное поле!')],
        description='Логин пользователя для входа',
    )
    password = PasswordField(
        label='Пароль',
        validators=[validators.DataRequired(message='Это обязательное поле!')],
        description='Пароль от аккаунта',
    )
    remember = BooleanField(
        label='Запомнить пользователя?',
    )
    submit = SubmitField(
        label='Войти',
    )

    def validate_login(self, login):
        for s in login.data:
            if s not in alphabet:
                raise ValidationError('Логин должен состоять латинских строчных или прописных символов'
                                      ' и знака подчеркивания!')
