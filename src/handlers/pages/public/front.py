from handlers import base


class FrontPageHandler(base.BaseHandler):
    def get(self):
        self.render('pages/front.html')
