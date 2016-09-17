#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
import datetime
import logging
import time
import json

import constants
import settings

from models.session import Session


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader('frontend/templates/'), autoescape=True, trim_blocks=True)
jinja_environment.globals['uri_for'] = webapp2.uri_for


class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        logging.debug('Request ID: ' + str(self.request.get('request_id')))

        self.session = None
        self.cookie_session = None
        self.get_current_session()

        # template values
        self.tv = {"current_uri": os.environ['PATH_INFO']} # Global
        self.api_response = {}

        logging.debug('<===== HEADERS =====>')
        logging.debug(self.request.headers)

        logging.debug('<===== ARGUMENTS =====>')
        arguments = self.request.arguments()
        for argument in arguments:
            try:
                logging.debug(argument + ': ' + self.request.get(argument))
            except:
                logging.debug(argument)
                logging.exception('error in logging above argument')

        self.now = datetime.datetime.now()
        self.user = self.get_current_user()

        self.ip_address = os.environ.get('REMOTE_ADDR')
        self.http_user_agent = os.environ.get('HTTP_USER_AGENT')

        logging.debug('<===== USER =====>')
        if self.user:
            logging.debug('USER NAME: ' + str(self.user.name))
        else:
            logging.debug('USER: ANONYMOUS')


    def check_etag(self):
        self.response.md5_etag()
        etag = self.response.etag
        logging.debug('etag: ' + etag)

        etag_with_quotes = '"' + etag + '"'
        if 'If-None-Match' in self.request.headers and self.request.headers['If-None-Match']:
            if self.request.headers['If-None-Match'] in [etag, etag_with_quotes]:
                # match! tell request to use cache!
                self.response.clear()
                self.response.status = '304 Not Modified'
                return

        self.response.headers['Cache-Control'] = "private"


    def render(self, template_path=None, force=False):
        self.tv["user"] = self.user
        self.tv["current_timestamp"] = time.mktime(self.now.timetuple())
        self.tv["current_url"] = self.request.uri
        self.tv["constants"] = constants

        if self.request.get('msg'):
            msg = self.request.get('msg')
            self.tv['alert'] = msg

        template = jinja_environment.get_template(template_path)
        self.response.out.write(template.render(self.tv))
        self.check_etag()


    def api_render(self):
        self.response.headers['Content-Type'] = "application/json"
        if self.custom_code and self.custom_code != 200:
            logging.debug('code: ' + str(self.custom_code))
            self.response.set_status(self.custom_code)

        elif 'code' in self.api_response and self.api_response['code'] != 200:
            logging.debug('code: ' + str(self.api_response['code']))
            self.response.set_status(self.api_response['code'])
        try:
            logging.info("API Response >> ")
            logging.info(self.api_response)
        except:
            logging.exception('error logging api_response')
        self.response.out.write(json.dumps(self.api_response))
        self.check_etag()


    def get_current_session(self):
        from gaesessions import get_current_session
        self.cookie_session = get_current_session()
        if 'session_token' in self.cookie_session and self.cookie_session['session_token']:
            self.session = Session.get_session_by_token(self.cookie_session['session_token'])


    def get_current_user(self):
        if self.session:
            return self.session.user
        return None


    def login(self, user):
        if self.session:
            self.session.logout_session()

        if not settings.ALLOW_MULTIPLE_USER_LOGINS:
            # invalidate all other sessions
            Session.make_all_sessions_inactive_of_user(user.key)

        self.session = Session.create_session(user.key, self.http_user_agent, self.ip_address)
        self.user = self.session.user
        self.cookie_session['session_token'] = self.session.session_token
        return


    def logout(self):
        if self.session:
            self.session.logout_session()
        if self.user:
            Session.make_all_sessions_inactive_of_user(self.user.key)
        self.cookie_session.terminate()



