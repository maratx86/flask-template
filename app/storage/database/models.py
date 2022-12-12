import datetime

from flask import request
from flask_login import UserMixin, logout_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from .. import db
from app import utils


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(124), unique=True)
    firstname = db.Column(db.String(124))
    lastname = db.Column(db.String(124))
    username = db.Column(db.String(124), unique=True)
    password = db.Column(db.String(102))
    reg_date = db.Column(db.DATETIME, default=datetime.datetime.utcnow)
    sessions = db.relationship('UserSession', lazy='select', backref=db.backref('user', lazy='joined'))
    confirmations = db.relationship('Confirmation', lazy='select', backref=db.backref('user', lazy='joined'))

    current_session = None

    @property
    def fullname(self):
        if self.lastname:
            return "{} {}".format(self.lastname, self.firstname)
        return self.firstname

    @property
    def is_admin(self):
        if self.is_authenticated and self.email in utils.admin.get():
            return True
        return False

    @property
    def is_authenticated(self):
        if 'current_session' not in self.__dict__ \
                or not self.current_session or self.current_session.expired:
            return False
        return self.is_active

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def change_password(self, password):
        self.password = generate_password_hash(password)
        for session in self.sessions:
            session.change()

    def get_id(self):
        if 'current_session' not in self.__dict__:
            return
        if not self.current_session:
            logout_user()
            return
        return self.current_session.session_id

    def login(self, user_agent, *login_user_args):
        td = login_user_args[1] if len(login_user_args) > 1 else None
        session = self.start_session(request.remote_addr, td)
        session.set_user_agent(user_agent)
        db.session.commit()
        login_user(self, *login_user_args)
        return True

    def logout(self):
        if self.current_session:
            db.session.delete(self.current_session)
            db.session.commit()
            self.current_session = None
        logout_user()
        return True

    def set_current_session(self, s):
        self.current_session = s

    def start_session(self, ip_address: str, expire_throw: datetime.timedelta = None):
        count = len(self.sessions)
        if count > 10:
            return None
        session = UserSession(
            user_id=self.id, ip_address=ip_address,
            expire_date=datetime.datetime.utcnow() + expire_throw if expire_throw else None,
        )
        session.change()
        db.session.add(session)
        db.session.commit()
        self.set_current_session(session)
        return session

    @staticmethod
    def load(session_id):
        session = db.session.query(UserSession) \
            .filter(UserSession.session_id == session_id).first()
        if not session:
            return
        if session.user:
            session.user.current_session = session
        return session.user

    def __str__(self):
        return 'User <{0}>'.format(self.email)


class UserSession(db.Model):
    __tablename__ = 'user_sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(32), index=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    expire_date = db.Column(db.DATETIME)
    last_active = db.Column(db.DATETIME, default=datetime.datetime.utcnow)
    ip_address = db.Column(db.String(39))
    user_agent = db.Column(db.String(150))

    @property
    def expired(self):
        return datetime.datetime.utcnow() >= self.expire_date

    def set_user_agent(self, value):
        self.user_agent = value[:150]

    def set_utc(self):
        self.last_active = datetime.datetime.utcnow()
        db.session.commit()

    def change(self):
        us = UserSessionAvailableValue.first()
        db.session.remove(us)
        self.session_id = us.id

    def __str__(self):
        return 'UserSession<{} {}>'.format(
            self.user.email if self.user else None,
            self.session_id,
        )


class Confirmation(db.Model):
    __tablename__ = 'confirmations'

    class Types:
        Email: str = 'email'
        Password: str = 'password'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(8), index=True)
    valid_from = db.Column(db.DATETIME, default=datetime.datetime.utcnow)
    valid_to = db.Column(db.DATETIME)
    token = db.Column(db.String(32), index=True, unique=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    def is_valid(self):
        if not self.valid_to:
            return True
        return self.valid_to < datetime.datetime.utcnow()

    @staticmethod
    def get(confirm_type, token):
        return Confirmation.query\
            .filter_by(
                type=confirm_type,
                token=token
        ).first()

    @staticmethod
    def check_valid(confirm_type, token):
        c = Confirmation.query.filter_by(
            type=confirm_type,
            token=token).first()
        if not c or c.valid_to < datetime.datetime.utcnow():
            return False
        return True


class UserSessionAvailableValue(db.Model):
    __tablename__ = 'user_session_id'

    id = db.Column(db.String(32), primary_key=True)


class ConfirmationAvailableValue(db.Model):
    __tablename__ = 'confirmation_tokens'

    id = db.Column(db.String(32), primary_key=True)
