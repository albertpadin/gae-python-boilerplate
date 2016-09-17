from google.appengine.api import users
import settings
import constants


def login_required(fn):
    '''self.user has to resolve to True. Otherwise, return 401'''
    def wrapper(self, *args, **kwargs):
        if not self.user:
            self.error(401)
            self.redirect(self.uri_for(constants.ROUTE_LOGIN))
            return
        else:
            return fn(self, *args, **kwargs)
    return wrapper


def public_only(fn):
    '''self.user has to resolve to False. Otherwise, redirect to default page for logged in user'''
    def wrapper(self, *args, **kwargs):
        if self.user:
            self.redirect(self.uri_for(settings.DEFAULT_PAGE_FOR_LOGGED_IN_USER))
            return
        else:
            return fn(self, *args, **kwargs)
    return wrapper


def mockable(fn):
    '''Set self.mockable to True if current user is admin according to Google Users'''
    def wrapper(self, *args, **kwargs):
        self.mockable = False
        if self.request.get("mock") == "1":
            # for testing
            admin_user = users.get_current_user()
            if admin_user and users.is_current_user_admin():
                self.mockable = True
        return fn(self, *args, **kwargs)
    return wrapper




