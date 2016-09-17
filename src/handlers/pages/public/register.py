from handlers import base
from handlers import decorators
import constants

from models.user import User
from models.user import EmailAlreadyRegisteredError


class RegisterPageHandler(base.BaseHandler):
    @decorators.public_only
    def get(self):
        self.render('pages/register.html')


    @decorators.public_only
    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')

        try:
            user = User.create_user(
                    first_name=None,
                    middle_name=None,
                    last_name=None,
                    email=email,
                    password=password
                )
        except EmailAlreadyRegisteredError:
            self.redirect(self.uri_for(constants.ROUTE_REGISTER, error=constants.ALERT_EMAIL_ALREADY_REGISTERED))
            return
        self.login(user)
        self.redirect(self.uri_for(constants.ROUTE_FRONT))