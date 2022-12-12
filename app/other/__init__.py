from flask import Blueprint


from .routes import (
    index, about, contact
)


def create_blueprint(*args, **kwargs):
    blueprint = Blueprint('other', __name__, *args, **kwargs)
    blueprint.route('/')(index)
    blueprint.route('/about/')(about)
    blueprint.route('/contact/')(contact)
    return blueprint
