from flask import Blueprint


from .routes import (
    main, login, logout,
    reg, reset, reset_post,
    reset_next_post
)

routes = (
    {
        'rule': '/',
        'handler': main,
    },
    {
        'rule': '/login/',
        'methods': ('GET', 'POST'),
        'handler': login
    },
    {
        'rule': '/reg/',
        'methods': ('GET', 'POST'),
        'handler': reg
    },
    {
        'rule': '/logout/',
        'handler': logout
    },
    {
        'rule': '/reset/',
        'methods': ('POST',),
        'handler': reset_post
    },
    {
        'rule': '/reset/',
        'methods': ('GET',),
        'handler': reset
    },
    {
        'rule': '/reset/next/',
        'methods': ('POST',),
        'handler': reset_next_post
    },
)


def create_blueprint(*args, **kwargs):
    blueprint = Blueprint('auth', __name__, *args, **kwargs)
    for route in routes:
        decor = blueprint.route(
            route['rule'],
            methods=route.get('methods', ('GET',))
        )
        decor(route['handler'])
    return blueprint
