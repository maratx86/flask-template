import datetime

from flask import request, redirect, url_for, render_template
from flask_login import current_user, login_user
from flask_mail import Message

from .. import storage, utils, logger, mail
from ..storage.database import models
from . import forms
from .. import utils


def main():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return redirect(url_for('other.index'))


def login():
    logger.info('login page {} {}'.format(current_user, request.args))
    if current_user.is_authenticated:
        return redirect(url_for('other.index'))
    error_message = None
    form = forms.LoginForm()
    if form.validate_on_submit():
        logger.info('login form submit for {}'.format(form.email.data))
        user = models.User.query.filter_by(email=form.email.data).first()
        logger.info('login form submit user {}'.format(user))
        if not user:
            error_message = 'The user with this email was not found!'
        elif user.check_password(form.password.data):
            logger.info('login form submit {} password correct'.format(form.email.data))
            user.login(
                request.user_agent.string,
                False, datetime.timedelta(days=1))
            return redirect(
                request.args.get('next', url_for('other.index'))
            )
        else:
            error_message = 'Password is not correct!'
    logger.info('login form submit error {}'.format(form.email.data))
    return render_template(
        'auth/login.html',
        form=form, error_message=error_message,
    )


def reg():
    error_message = None
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user:
            error_message = 'User with this email already exists! Try to log in.'
        else:
            user = models.User(
                email=form.email.data,
                firstname=form.firstname.data or None,
                lastname=form.lastname.data or None,
            )
            user.change_password(form.password.data)
            if not models.User.query.filter_by(username=form.username.data).first():
                user.username = form.username.data
            storage.db.session.add(user)
            storage.db.session.commit()
            login_user(user)
            return redirect(url_for('other.index'))
    return render_template(
        'auth/registration.html',
        form=form, error_message=error_message,
    )


def logout():
    if current_user.is_authenticated:
        current_user.logout()
        message = "Log out successful"
    else:
        message = "You are not logged in"
    return render_template(
        'auth/logout.html',
        notification_message=message,
    )


def reset_post():
    form = forms.ResetRequestForm()
    if not form.validate_on_submit():
        return render_template(
            'auth/reset_request.html',
            current_user=current_user,
            form=form
        )
    logger.info('reset form submit {}'.format(form.email.data))
    email = form.email.data
    user = models.User.query.filter_by(email=email).first()
    logger.info('reset form submit user {}'.format(user))
    if user:
        confirmation = storage.database.models.Confirmation(
            storage.database.models.Confirmation.Types.Password,
            user_id=user.id)
        logger.info('reset form submit user {} letter sending'.format(user))
        _url = utils.urls.construct_with_host(
            request.host_url,
            url_for('auth.reset'),
            token=confirmation.token
        )
        message = Message('Reset Password')
        message.add_recipient(user.email)
        message.body = render_template('email/reset_password.txt', link=_url)
        message.html = render_template('email/reset_password.html', link=_url)
        mail.send(message)
        logger.info('reset form submit user {} letter sent'.format(user))
        return redirect(
            utils.urls.construct(
                url_for('auth.reset'),
                notification='restore-link-sent',
            )
        )
    return redirect(
        utils.urls.construct(
            url_for('auth.login'),
            notification='restore-password-failed',
        )
    )


def reset():
    token = request.args.get('token', default=None)
    if token:
        return reset_password(token)
    form = forms.ResetRequestForm()
    logger.info('reset form request {}'.format(current_user))
    return render_template(
        'auth/reset_request.html',
        current_user=current_user,
        form=form,
        **utils.auth.external_template_arguments(request.args)
    )


def reset_next_post():
    form = forms.ResetPasswordForm()

    if not form.validate_on_submit():
        return render_template(
            'auth/reset_password.html',
            current_user=current_user,
            form=form,
            **utils.auth.external_template_arguments(request.args)
        )
    token = storage.database.models.Confirmation.get(
        storage.database.models.Confirmation.Types.Password,
        form.token.data,
    )
    if not token:
        return redirect(utils.urls.construct(
            url_for('auth.reset'),
            notification='success',
        ))
    password = form.password.data

    if token.user:
        token.user.change_password(password)
        storage.db.session.remove(token)
        storage.db.session.commit()
        return redirect(
            utils.urls.construct(
                url_for('auth.login'),
                notification='success'
            )
        )
    return redirect(
        utils.urls.construct(
            url_for('auth.login'),
            notification='restore-password-failed',
        )
    )


def reset_password(token=None):
    if not token:
        return redirect(url_for('auth.reset'))
    logger.info('reset form password reset {}'.format(current_user))
    confirmation = storage.database.models.Confirmation.get(
        storage.database.models.Confirmation.Types.Password,
        token
    )
    if not confirmation or not confirmation.is_valid():
        logger.info('reset form password token invalid {}'.format(current_user))
        return redirect(
            utils.urls.construct(
                url_for('auth.reset'),
                error='link-expired',
            )
        )
    logger.info('reset form password request {}'.format(current_user))
    form = forms.ResetPasswordForm()
    form.set_token(token)
    return render_template(
        'auth/reset_password.html',
        current_user=current_user,
        form=form,
        **utils.auth.external_template_arguments(request.args)
    )
