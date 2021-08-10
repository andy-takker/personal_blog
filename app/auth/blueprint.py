from flask import Blueprint

auth_bp = Blueprint(
    'auth',
    __name__,
    static_folder='frontend/static',
    static_url_path='static',
    template_folder='frontend/templates',
    url_prefix='/auth',
)