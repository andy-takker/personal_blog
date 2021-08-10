from typing import Dict, Optional

from flask import Flask, render_template, url_for
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
admin = Admin(name='Адвокат', template_mode='bootstrap4')


def create_app(config, test_config: Optional[Dict] = None):
    app = Flask(
        __name__,
        static_url_path='',
        static_folder='frontend/static',
        template_folder='frontend/templates',
    )
    app.config.from_object(config)
    if test_config is not None:
        app.config.update(test_config)

    register_extensions(app)
    register_commands(app)
    register_blueprints(app)
    register_handlers(app)
    register_routers(app)
    register_shell_context(app)

    return app


def register_extensions(app):
    db.init_app(app)

    login_manager.login_view = 'auth.login_get_view'
    login_manager.login_message = 'Пожалуйста, войдите, чтобы получить доступ к странице'
    login_manager.session_protection = 'strong'
    login_manager.init_app(app)

    migrate.init_app(app, db)
    from .admin_panel import initialize_admin
    initialize_admin(app, db)
    from .admin_panel.user import UserModelView
    from .admin_panel.login import LoginLink
    from .models import User

def register_commands(app):
    pass


def register_blueprints(app):
    from .auth import auth_bp
    app.register_blueprint(auth_bp)


def register_handlers(app):
    pass


def register_routers(app):
    @app.get('/')
    def index_view():
        """Главная страница"""
        return render_template(
            'app/public/index.html',
            title='Главная',
        )


def register_shell_context(app):
    """Регистрация моделей для использования в Flask shell"""
    from .models import User

    def shell_context():
        return {
            'db': db,
            'User': User,
        }

    app.shell_context_processor(shell_context)
