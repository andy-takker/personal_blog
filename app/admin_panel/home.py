from flask_admin import AdminIndexView, expose

from app.models import User


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        users = User.query.all()
        return self.render('admin_panel/home.html', users=users)
