from os.path import basename

from flask import redirect, url_for, request
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AdminBashBoardView(AdminIndexView):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        super(AdminBashBoardView, self).__init__(*args, **kwargs)

    @expose('/')
    def index(self):
        self.app.uspace.logger.info('admin index (success): {}'.format(current_user))
        return self.render(
            'admin/index.html',
        )

    def inaccessible_callback(self, name, **kwargs):
        self.app.uspace.logger.info('admin index (fail): {}'.format(current_user))
        return redirect(
            self.utils.url_params(
                url_for('auth.login'),
                next=self.utils.url_params(
                    request.path,
                    **request.args
                )
            )
        )

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return current_user.is_admin


class SecureModelView(ModelView):
    def __init__(self, *args, **kwargs):
        if 'inner_properties' in kwargs:
            for k, v in kwargs['inner_properties'].items():
                setattr(self, k, v)
            kwargs.pop('inner_properties')
        super(SecureModelView, self).__init__(*args, **kwargs)

    def inaccessible_callback(self, name, **kwargs):
        self.logger.info('admin entity <{}> (failed): {}'.format(self.endpoint, current_user))
        return redirect(url_for('auth.login'))

    def render(self, template, **kwargs):
        self.logger.info('admin entity <{}> (render): {}'.format(self.endpoint, current_user))
        return super(SecureModelView, self).render(template, **kwargs)

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return current_user.is_admin


class SecureFileAdmin(FileAdmin):
    def __init__(self, *args, **kwargs):
        if 'inner_properties' in kwargs:
            for k, v in kwargs['inner_properties'].items():
                setattr(self, k, v)
            kwargs.pop('inner_properties')
        super(SecureFileAdmin, self).__init__(*args, **kwargs)
        self.view_name = 'SecureFileAdmin'

    def render(self, template, **kwargs):
        self.logger.info('admin file <{}> (render): {}'.format(self.view_name, current_user))
        return super(SecureFileAdmin, self).render(template, **kwargs)

    def inaccessible_callback(self, name, **kwargs):
        self.logger.info('admin file <{}> (fail): {}'.format(self.view_name, current_user))
        return redirect(url_for('auth.login'))

    def is_accessible(self):
        if not current_user.is_authenticated:
            return False
        return current_user.is_admin


class Static(SecureFileAdmin):
    def __init__(self, *args, **kwargs):
        super(SecureFileAdmin, self).__init__(*args, **kwargs)
        self.view_name = 'Static'


class Log(SecureFileAdmin):
    def __init__(self, *args, **kwargs):
        super(SecureFileAdmin, self).__init__(*args, **kwargs)
        self.view_name = 'Logging'
        self.can_upload = True
        self.can_mkdir = False

    def delete_file(self, file_path):
        filename = basename(file_path)
        self.logger.info(filename)
        if filename not in ('debug.log', 'info.log', 'warning.log', 'error.log', 'critical.log'):
            super(Log, self).delete_file(file_path)
            return
        mode = basename(file_path).split('.')[0]
        self.logger.close_file(mode)
        super(Log, self).delete_file(file_path)
        self.logger.open_file(mode)

    def on_rename(self, full_path, dir_base, filename):
        old_file = basename(full_path)
        if old_file in ('debug.log', 'info.log', 'warning.log', 'error.log', 'critical.log'):
            mode = old_file.split('.')[0]
            self.logger.open_file(mode)

    def render(self, template, **kwargs):
        if template == self.rename_template:
            name = kwargs.get('name')
            if name in ('debug.log', 'info.log', 'warning.log', 'error.log', 'critical.log'):
                mode = name.split('.')[0]
                self.logger.close_file(mode)
        return super(Log, self).render(template, **kwargs)


class UserSecModView(SecureModelView):
    column_list = ('id', 'sessions', 'email', 'firstname', 'lastname', 'username', 'reg_date')

    column_editable_list = ('email', 'firstname', 'lastname', 'username')
    form_columns = ('email', 'firstname', 'lastname', 'username', 'reg_date', 'sessions', )

    def __init__(self, app, *args, **kwargs):
        super(UserSecModView, self).__init__(
            app.uspace.storage.database.models.User,
            app.uspace.storage.db.session,
            name='Users', *args, **kwargs)

    def _on_model_change(self, form, model, is_created):
        if model.password != form.password.data:
            model.change_password(form.password.data)
        return


class UserPswdSecModView(SecureModelView):
    column_list = ('id', 'fullname', 'email', 'password')
    form_columns = ('password',)
    column_editable_list = ('password',)

    def __init__(self, app, *args, **kwargs):
        super(UserPswdSecModView, self).__init__(
            app.uspace.storage.database.models.User,
            app.uspace.storage.db.session, name='User Passwords',
            endpoint='userpassword', *args, **kwargs
        )

    def _on_model_change(self, form, model, is_created):
        model.change_password(form.password.data)


class UserSession(SecureModelView):
    column_list = ('id', 'session_id', 'user', 'expire_date', 'ip_address', 'last_active', 'user_agent')
    column_editable_list = ('session_id',)

    def __init__(self, app, *args, **kwargs):
        super(UserSession, self).__init__(
            app.uspace.storage.database.models.UserSession,
            app.uspace.storage.db.session, *args,
            name='Sessions', **kwargs
        )
