from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


from .database import models


def init_app(app):
    db.init_app(app)
    app.app_context().push()
    db.create_all()
    migrate.init_app(
        app, db, 'app/storage/database/migrations',
        render_as_batch=app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:'),
    )
