import os
import random


from . import generator

__emails = None


def init(app):
    for _email in app.uspace.admins_email:
        user = app.uspace.storage.database.models.User.query.filter_by(email=_email).first()
        if not user:
            password = generator.random_token(10)
            user = app.uspace.storage.database\
                .models.User(email=_email)
            user.change_password(password)
            app.uspace.storage.db.session.add(user)
            app.uspace.storage.db.session.commit()


def get():
    global __emails

    if __emails is not None:
        return __emails
    admins_email = os.environ.get('ADMINS_EMAIL')
    if admins_email:
        __emails = tuple(admins_email.split(';'))
    else:
        __emails = ()
    return __emails
