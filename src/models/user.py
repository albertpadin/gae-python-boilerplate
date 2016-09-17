import logging

from google.appengine.ext import ndb
from passlib.hash import pbkdf2_sha512

import constants
import settings

from libraries.helpers.string_functions import normalize_email
from models.session import Session
from app_exceptions import CustomException


class User(ndb.Model):
    p_created = ndb.DateTimeProperty(auto_now_add=True, name='created')
    p_updated = ndb.DateTimeProperty(auto_now=True, name='updated')

    # first name, last name, middle name
    p_fname = ndb.StringProperty(name='fname')
    p_lname = ndb.StringProperty(name='lname')
    p_mname = ndb.StringProperty(name='mname')

    p_email = ndb.StringProperty(name='email')
    p_password = ndb.StringProperty(name='password')

    p_status = ndb.StringProperty(name='status')
    p_role = ndb.StringProperty(name='role')


    # properties
    @property
    def name(self):
        formatted_name = ''
        if self.first_name:
            formatted_name += self.first_name
        if self.middle_name:
            formatted_name += ' ' + self.middle_name
        if self.last_name:
            formatted_name += ' ' + self.last_name
        return formatted_name.strip()


    @property
    def first_name(self):
        return self.p_fname

    @first_name.setter
    def first_name(self, value):
        if value:
            self.p_fname = value.strip()


    @property
    def middle_name(self):
        return self.p_mname

    @middle_name.setter
    def middle_name(self, value):
        if value:
            self.p_mname = value.strip()


    @property
    def last_name(self):
        return self.p_lname

    @last_name.setter
    def last_name(self, value):
        if value:
            self.p_lname = value.strip()


    @property
    def email(self):
        return self.p_email

    @email.setter
    def email(self, value):
        if value:
            self.p_email = normalize_email(value)
    

    @property
    def password(self):
        return 'use verify_password()'

    @password.setter
    def password(self, value):
        if value:
            self.p_password = User.hash_password(value)


    @property
    def status(self):
        return self.p_status

    @status.setter
    def status(self, value):
        self.p_status = value


    @property
    def role(self):
        return self.p_role

    @role.setter
    def role(self, value):
        self.p_role = value


    @classmethod
    def hash_password(cls, given_password):
        """
            Returns a hashed password using PBKDF2 (SHA512).
        """
        return pbkdf2_sha512.encrypt(given_password)


    def verify_password(self, given_password):
        """
            Verifies the user password on the database with the give
            password on the form.
        """
        return pbkdf2_sha512.verify(given_password, self.p_password)


    @classmethod
    def user_exists(cls, email):
        email = normalize_email(email)
        if cls.query(cls.p_email == email).get(keys_only=True):
            return True
        return False


    @classmethod
    def create_user(
            cls,
            first_name,
            middle_name,
            last_name,
            email,
            password,
            status=settings.DEFAULT_USER_STATUS,
            role=settings.DEFAULT_USER_ROLE
        ):
        if cls.user_exists(email):
            logging.debug(constants.LOG_EMAIL_ALREADY_IN_SYSTEM)
            raise EmailAlreadyRegisteredError('Email address is already registered in system')

        user = cls()
        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        user.email = email
        user.password = password
        user.status = status
        user.role = role
        user.put()

        return user


    @classmethod
    def get_user_with_email_password(cls, email, password):
        email = normalize_email(email)
        user = cls.query(cls.p_email == email).get()

        if not user:
            logging.debug(constants.LOG_EMAIL_NOT_FOUND)
            raise InvalidCredentialsError('Email and password combination is incorrect')

        if not user.verify_password(password):
            logging.debug(constants.LOG_INCORRECT_PASSWORD)
            raise InvalidCredentialsError('Email and password combination is incorrect')

        # user has correct password
        return user


class InvalidCredentialsError(CustomException):
    pass


class EmailAlreadyRegisteredError(CustomException):
    pass
