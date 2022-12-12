_message = {
    'login-failed': 'There is no user with that e-mail and password! Try another one',
    'user-not-found': 'There is no user with that e-mail! Try another one',
    'link-expired': 'Reset link expired! Try Again...',
    'restore-link-sent': 'Check email for reset password link!',
    'restore-password-failed': 'Password has not been changed',
    'not-valid-link': 'Link not valid or expired!',
    'success': 'Password was changed. Try to Log In!',
}


def external_template_arguments(d: dict):
    r = {}
    if 'notification' in d and d['notification'] in _message:
        r['notification_message'] = _message[d['notification']]
    if 'error' in d and d['error'] in _message:
        r['error_message'] = _message[d['error']]
    return r
