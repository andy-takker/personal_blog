from flask import url_for, request, render_template, flash
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from .blueprint import auth_bp
from .forms.login import LoginForm
from app.models import User


@auth_bp.get('/login')
def login_get_view():
    if current_user.is_authenticated:
        return redirect('/admin')
    form = LoginForm(request.form)
    return render_template('auth/public/login.html', title='Вход', form=form)


@auth_bp.post('/login')
def login_post_view():
    if current_user.is_authenticated:
        return redirect('/')

    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if not user or not user.check_password(password=form.password.data):
            flash('Проверьте правильность введённых данных!')
            return redirect(url_for('.login_get_view'))
        login_user(user, remember=form.remember.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/admin'
        return redirect(next_page)
    flash(form.errors)
    return redirect(url_for('auth.login_get_view'))


@auth_bp.get('/logout')
@login_required
def logout_view():
    logout_user()
    flash('Вы вышли из аккаунта!')
    return redirect(url_for('auth.login_get_view'))
