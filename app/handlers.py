from flask import render_template

from .view_models import error as view_models_error


def exception_handler(e):
    view = view_models_error.ErrorView(e)
    return render_template(
        'error.html', view=view,
    )


def os_exception_handler(e):
    view = view_models_error.ErrorView(e)
    return render_template(
        'error.html',
        view=view,
    )


def not_found_handler(e):
    view = view_models_error.ErrorView(
        e, error_title='Not Found',
        reportable=False,
    )
    return render_template(
        'error.html', view=view,
    ), 404


def init_app(app):
    app.register_error_handler(OSError, os_exception_handler)
    app.register_error_handler(Exception, exception_handler)
    app.register_error_handler(404, not_found_handler)
