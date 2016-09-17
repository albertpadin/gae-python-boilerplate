import webapp2
from webapp2_extras import routes

from handlers.pages.public import front
from handlers.pages.public import login
from handlers.pages.public import register

from handlers.pages.public import content

import constants


app = webapp2.WSGIApplication([
    routes.DomainRoute(r'<:.*>', [
        webapp2.Route('/', handler=front.FrontPageHandler, name=constants.ROUTE_FRONT),
        webapp2.Route('/login', handler=login.LoginPageHandler, name=constants.ROUTE_LOGIN),
        webapp2.Route('/register', handler=register.RegisterPageHandler, name=constants.ROUTE_REGISTER),
        webapp2.Route('/logout', handler=login.LogoutPageHandler, name=constants.ROUTE_LOGOUT),

        webapp2.Route('/content', handler=content.ContentPageHandler, name=constants.ROUTE_CONTENT),
        webapp2.Route('/content/<content_id>', handler=content.SingleContentPageHandler, name=constants.ROUTE_CONTENT_WITH_ID),
    ])
], debug=True)
