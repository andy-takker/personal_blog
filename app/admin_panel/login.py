from flask import url_for, request, flash, redirect
from flask_admin import BaseView, expose
from flask_admin.menu import MenuLink
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from app.auth.forms.login import LoginForm
from app.models import User


class LoginLink(MenuLink):
    def is_visible(self):
        return not current_user.is_authenticated

    def is_accessible(self):
        return not current_user.is_authenticated

    def get_url(self):
        return url_for('login.index')


class LogoutLink(MenuLink):
    def is_visible(self):
        return current_user.is_authenticated

    def is_accessible(self):
        return current_user.is_authenticated

    def get_url(self):
        return url_for('login.logout')


class LoginView(BaseView):
    def is_visible(self):
        return False

    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))

        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate_on_submit():
            user = User.query.filter_by(login=form.login.data).first()
            if not user or not user.check_password(password=form.password.data):
                flash('Проверьте правильность введённых данных!', 'warning')
                return self.render('admin_panel/login.html', form=form)
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin.index')
            return redirect(next_page)
        return self.render('admin_panel/login.html', form=form)

    @expose('/logout',)
    def logout(self):
        logout_user()
        flash('Вы вышли из аккаунта!')
        return redirect(url_for('login.index'))
