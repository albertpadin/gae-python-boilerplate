from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor


class Content(ndb.Model):
    p_created = ndb.DateTimeProperty(auto_now_add=True, name='created')
    p_updated = ndb.DateTimeProperty(auto_now=True, name='updated')
    p_owner = ndb.KeyProperty(kind='User', name='owner')
    p_title = ndb.StringProperty(name='title')
    p_content = ndb.TextProperty(name='content')


    @property
    def owner(self):
        return self.p_owner

    @owner.setter
    def owner(self, value):
        if value:
            self.p_owner = value


    @property
    def title(self):
        return self.p_title

    @title.setter
    def title(self, value):
        if value:
            self.p_title = value.strip()


    @property
    def content(self):
        return self.p_content

    @content.setter
    def content(self, value):
        if value:
            self.p_content = value.strip()


    @classmethod
    def create_content(cls, owner_key, title, text_content=None):
        content = cls()
        content.owner = owner_key
        content.title = title
        content.content = text_content
        content.put()
        return content


    @classmethod
    def get_list(cls, n=50, cursor=None):
        if cursor:
            cursor = Cursor(urlsafe=cursor)
            results, next_cursor, more = cls.query().fetch_page(n, start_cursor=cursor)
        else:
            results, next_cursor, more = cls.query().fetch_page(n)

        return results, next_cursor.urlsafe() if next_cursor else None


    @classmethod
    def get_with_id(cls, content_id):
        return cls.get_by_id(ndb.Key(urlsafe=content_id).id())
        