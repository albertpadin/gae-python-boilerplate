from handlers import base
from handlers import decorators
import constants

from models.user import User
from models.user import InvalidCredentialsError


class LoginPageHandler(base.BaseHandler):
    @decorators.public_only
    def get(self):
        self.render('pages/login.html')


    @decorators.public_only
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        try:
            user = User.get_user_with_email_password(email, password)
        except InvalidCredentialsError:
            self.redirect(self.uri_for(constants.ROUTE_LOGIN, msg=constants.ALERT_INCORRECT_CREDENTIALS))
            return

        self.login(user)
        self.redirect(self.uri_for(constants.ROUTE_FRONT))


class LogoutPageHandler(base.BaseHandler):
    @decorators.login_required
    def get(self):
        self.logout()
        self.redirect(self.uri_for(constants.ROUTE_LOGIN, msg=constants.ALERT_LOGGED_OUT))

