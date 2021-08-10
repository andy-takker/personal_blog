from flask import url_for, request, current_app
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import StringField, validators, PasswordField, ValidationError

import string

from app.models import User

alphabet = string.digits + string.ascii_letters + '_'


class UserForm(FlaskForm):
    class Meta:
        csrf = False

    name = StringField(
        label='Имя',
        validators=[validators.DataRequired(message='Это обязательное поле!')],
        description='Имя пользователя',
    )
    login = StringField(
        label='Логин',
        validators=[validators.DataRequired(message='Это обязательное поле!')],
        description='Логин пользователя для входа',
    )
    password = PasswordField(
        label='Новый пароль',
        validators=[validators.Optional(strip_whitespace=True)],
        description='Пароль от аккаунта',
    )
    password2 = PasswordField(
        label='Повторите пароля',
    )

    def validate_login(self, login: StringField):
        for s in login.data:
            if s not in alphabet:
                raise ValidationError(
                    'Логин должен состоять из цифр, латинских строчных или прописных символов и знака подчеркивания!')

    def validate_password2(self, password2: PasswordField):
        if self.password.data != password2.data:
            raise ValidationError('Пароли должны совпадать!')


class UserModelView(ModelView):
    column_exclude_list = ['password_hash']
    column_searchable_list = ['name', 'login']
    column_filters = ['login', 'name', 'created_at']
    column_descriptions = {
        'name': 'Имя пользователя',
        'login': 'Логин пользователя',
        'created_at': 'Дата и время создания пользователя',
        'updated_at': 'Дата и время последнего обновления',
    }
    column_labels = {
        'login': 'Логин',
        'name': 'Имя',
        'created_at': 'Создано',
        'updated_at': 'Обновлено',
    }
    column_formatters = {
        'created_at': lambda v, c, m, p: m.created_at.strftime('%H:%M:%S %d.%m.%Y'),
        'updated_at': lambda v, c, m, p: m.created_at.strftime('%H:%M:%S %d.%m.%Y'),
    }
    column_default_sort = ('login', False)

    can_set_page_size = True
    can_export = True
    can_view_details = True

    column_export_list = ('created_at', 'updated_at', 'login', 'name')

    create_modal = True

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login_get_view', next=request.url))

    def create_form(self, obj=None):
        return UserForm()

    def create_model(self, form: UserForm):
        u: User = self.model()
        u.login = form.login.data
        u.name = form.name.data
        u.set_password(password=form.password.data)
        self.session.add(u)
        self.session.commit()

    def update_model(self, form: UserForm, model: User):
        model.login = form.login.data
        model.name = form.name.data
        if form.password.data is not None:
            model.set_password(password=form.password.data)
        current_app.logger.info(model.name)
        self.session.commit()
        return True

    def edit_form(self, obj: User = None):
        return UserForm()

    def on_form_prefill(self, form: UserForm, id):
        user = User.query.get(id)
        form.name.data = user.name
        form.login.data = user.login
