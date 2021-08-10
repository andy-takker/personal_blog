from flask import Flask
from flask_admin import Admin

from app.admin_panel.home import MyAdminIndexView
from app.admin_panel.login import LoginLink, LogoutLink, LoginView
from app.admin_panel.user import UserModelView
from app.models import User


def initialize_admin(app: Flask, db):
    admin = Admin(
        app=app,
        name='Адвокат',
        template_mode='bootstrap4',
        index_view=MyAdminIndexView(name='Главная', template='admin_panel/home.html'), )
    admin.add_view(UserModelView(User, db.session, name='Пользователи'))
    admin.add_link(LoginLink(name='Вход'))
    admin.add_link(LogoutLink(name='Выход'))
    admin.add_view(LoginView(name='Войти', url='login/', endpoint='login'))
    return admin
