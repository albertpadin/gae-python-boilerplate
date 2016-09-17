#!/usr/bin/env python
# -*- coding: utf-8 -*-
from handlers import base


class AdminUtilitiesHandler(base.BaseHandler):
    def get(self):
        self.tv['alert'] = 'Admin utilities'
        self.render()