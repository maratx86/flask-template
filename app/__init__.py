import os

from flask import Flask
from flask_login import LoginManager, current_user
from flask_mail import Mail

from .log import Logger
from . import storage, utils
from .uspace import USpace

mail = Mail()
login = LoginManager()
logger = Logger()


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopmentConfig')

    mail.init_app(app)
    storage.init_app(app)
    login.init_app(app)
    login.login_view = 'auth.login'
    login.login_message = 'Please log in to access this page.'

    setattr(app, 'uspace', USpace(
        mail, login, logger, storage,
        utils.admin.get()))

    @login.user_loader
    def load_user(user_id):
        return storage.database.models.User.load(user_id)

    def before_request():
        if not current_user.is_authenticated:
            return
        if 'current_session' not in current_user.__dict__:
            current_user.current_session = None
        if current_user.current_session:
            current_user.current_session.set_utc()

    app.before_request_funcs = {
        None: (before_request,),
    }

    from . import handlers
    from . import cli

    from .auth import create_blueprint as auth_create_blueprint
    from .other import create_blueprint as other_create_blueprint
    from .admin import create_admin

    create_admin(app)
    cli.init_app(app)

    app.register_blueprint(
        auth_create_blueprint(url_prefix='/auth'))
    app.register_blueprint(
        other_create_blueprint(url_prefix='/'))
    handlers.init_app(app)
    app.app_context().push()
    utils.admin.init(app)
    return app
