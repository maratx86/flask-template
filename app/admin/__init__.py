from os import path
from flask_admin import Admin

import config
from . import views


def create_admin(app):
    admin = Admin(name='Marat Ash', template_mode='bootstrap3')

    admin.init_app(app, index_view=views.AdminBashBoardView(app))
    admin.add_view(views.UserSecModView(app))
    admin.add_view(views.UserSession(app))
    admin.add_view(views.UserPswdSecModView(app))
    __path = path.join(config.basedir, 'app', 'static')
    path_log = path.join(config.basedir, 'log')
    admin.add_view(views.Static(__path, name='Static Files'))
    admin.add_view(views.Log(path_log, name='Log Files'))
