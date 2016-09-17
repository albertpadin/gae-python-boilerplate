from google.appengine.ext import ndb
from libraries.helpers.string_functions import generate_random_string
from settings import SESSION_TOKEN_LENGTH
import datetime
import logging


class Session(ndb.Model):
    p_created = ndb.DateTimeProperty(auto_now_add=True, name='created')
    p_updated = ndb.DateTimeProperty(auto_now=True, name='updated')
    p_user_key = ndb.KeyProperty(kind='User', name='user_key')
    p_user_agent = ndb.StringProperty(name='user_agent')
    p_ip_address = ndb.StringProperty(name='ip_address')
    p_session_token = ndb.StringProperty(name='session_token')
    p_active = ndb.BooleanProperty(default=True, name='active')
    

    @property
    def user_key(self):
        return self.p_user_key

    @user_key.setter
    def user_key(self, value):
        self.p_user_key = value


    @property
    def user(self):
        return self.p_user_key.get()


    @property
    def user_agent(self):
        return self.p_user_agent

    @user_agent.setter
    def user_agent(self, value):
        self.p_user_agent = value


    @property
    def ip_address(self):
        return self.p_ip_address

    @ip_address.setter
    def ip_address(self, value):
        self.p_ip_address = value


    @property
    def session_token(self):
        return self.p_session_token


    @property
    def active(self):
        return self.p_active


    @active.setter
    def active(self, value):
        self.p_active = value


    @classmethod
    def get_session_by_token(cls, session_token):
        return cls.get_by_id(session_token)


    @classmethod
    def create_session(
            cls,
            user_key,
            user_agent=None,
            ip_address=None
        ):
        session_token = generate_random_string(SESSION_TOKEN_LENGTH)
        session = cls(id=session_token)
        session.p_session_token = session_token
        session.user_key = user_key
        session.user_agent = user_agent
        session.ip_address = ip_address
        session.put()
        return session


    @classmethod
    def make_all_sessions_inactive_of_user(cls, user_key):
        query = cls.query(cls.p_user_key == user_key)
        query = query.filter(cls.p_active == True)
        sessions = query.fetch()

        new_sessions = []
        for session in sessions:
            session.logout_session(put=False)
            new_sessions.append(session)

        if new_sessions:
            ndb.put_multi(new_sessions)

        return True


    def logout_session(self, put=True):
        self.active = False
        if put:
            self.put()
        return self



