import os
import sys
import logging


basedir = os.path.abspath(os.path.dirname(__file__))
log_dir = os.path.join(basedir, '../log')

try:
    os.makedirs(log_dir)
except OSError as error:
    print(error)


modes = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

names = {
    'debug': 'debug.log',
    'info': 'info.log',
    'warning': 'warning.log',
    'error': 'error.log',
    'critical': 'critical.log',
}

full_names = {
    'debug': os.path.join(log_dir, names['debug']),
    'info': os.path.join(log_dir, names['info']),
    'warning': os.path.join(log_dir, names['warning']),
    'error': os.path.join(log_dir, names['error']),
    'critical': os.path.join(log_dir, names['critical']),
}


class Logger:
    def __init__(self):
        self.loggers = {}
        for mode_name, mode in modes.items():
            logger = logging.getLogger("on-menu-{}".format(mode_name))
            logger.setLevel(mode)
            file_handler = logging.FileHandler(full_names[mode_name])
            if mode_name not in ('error', 'critical'):
                console_handler = logging.StreamHandler(sys.stdout)
            else:
                console_handler = logging.StreamHandler(sys.stderr)
            file_handler.setFormatter(
                logging.Formatter(fmt='[%(asctime)s] %(name)-15s %(message)s'))
            console_handler.setFormatter(
                logging.Formatter(fmt='[%(asctime)s] %(levelname)-8s %(name)-15s %(message)s'))
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            self.loggers[mode_name] = logger

    def debug(self, *args, **kwargs):
        self.loggers['debug'].debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        self.loggers['info'].info(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.loggers['warning'].warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.loggers['error'].error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.loggers['critical'].critical(*args, **kwargs)

    def exception(self, e, *args, **kwargs):
        self.loggers['error'].exception(e, *args, **kwargs)

    def close_file(self, mode):
        if mode not in self.loggers:
            return False
        file_handler = self.loggers[mode].handlers[-1]
        file_handler.close()
        return True

    def open_file(self, mode):
        if mode not in self.loggers:
            return False
        file_handler = logging.FileHandler(full_names[mode])
        file_handler.setFormatter(
            logging.Formatter(fmt='[%(asctime)s] %(name)-15s %(message)s'))
        self.loggers[mode].addHandler(file_handler)
        return True
