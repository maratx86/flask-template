import types
from flask_login import LoginManager
from flask_mail import Mail

from .log import Logger


class USpace:
    login: LoginManager
    mail: Mail
    logger: Logger
    storage: types.ModuleType
    admins_email: tuple

    def __init__(self, *args):
        for arg in args:
            if isinstance(arg, LoginManager): self.login = arg
            elif isinstance(arg, Mail): self.mail = arg
            elif isinstance(arg, Logger): self.logger = arg
            elif isinstance(arg, tuple): self.admins_email = arg
            else: self.storage = arg
