from handlers import base
from handlers import decorators
import constants

from models.content import Content


class ContentPageHandler(base.BaseHandler):
    def get(self):
        cursor = self.request.get('cursor')
        self.tv['contents'], self.tv['next_cursor'] = Content.get_list(cursor=cursor)
        self.render('pages/content.html')


    @decorators.login_required
    def post(self):
        content = self.request.get('content')
        title = self.request.get('title')

        content = Content.create_content(
            owner_key=self.user.key,
            title=title,
            text_content=content
            )

        self.redirect(self.uri_for(constants.ROUTE_CONTENT_WITH_ID, content_id=content.key.urlsafe()))


class SingleContentPageHandler(base.BaseHandler):
    def get(self, content_id):
        self.tv['content'] = Content.get_with_id(content_id)
        self.render('pages/single_content.html')
        