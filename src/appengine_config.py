from google.appengine.ext import vendor
import credentials


# Add any libraries installed in the "lib" folder.
vendor.add('vendor_lib')


from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key=credentials.COOKIE_KEY)
    return app
    