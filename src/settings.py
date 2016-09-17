#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import constants


def development():
    if os.environ['SERVER_SOFTWARE'].find('Development') == 0:
        return True
    else:
        return False


SITE_NAME = 'Boilerplate'


CLOUDSTORAGE_BUCKET = 'boilerplate'


DEFAULT_USER_STATUS = constants.USER_STATUS_ACTIVE
DEFAULT_USER_ROLE = constants.USER_ROLE_PUBLIC


SESSION_TOKEN_LENGTH = 256


ALLOW_MULTIPLE_USER_LOGINS = False



DEFAULT_PAGE_FOR_LOGGED_IN_USER = constants.ROUTE_FRONT
