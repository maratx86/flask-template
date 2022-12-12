import datetime

from flask import url_for

from .. import utils, logger

message_template \
    = '''Time: {time}
Error ID: {error_id}
'''


class ErrorView():
    def __init__(self, e, *args, **kwargs):
        self._title = 'Error'
        self.reportable = kwargs.get('reportable', True)
        if self.reportable:
            self.error_id = utils.generate_random_token(10)
            message = message_template.format(
                time=datetime.datetime.utcnow().strftime('%d.%m.%Y %H:%M:%S.%f %z'),
                error_id=self.error_id
            )
            logger.error('error {}'.format(self.error_id))
            logger.exception(e)
            self.report_link = utils.url_params(
                url_for('other.contact'),
                subject='Bug',
                message=message,
            )
        self.error_title = kwargs.get('error_title') or 'Error Occurs'
        self.message = str(e)
