#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime


def datetime_to_timestamp(dt, epoch=datetime.datetime(1970,1,1)):
    td = dt - epoch
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6


def time_format(d, timezone=None):
    return d.strftime('%-H%p')


def is_tomorrow(d, timezone=None):
    return d.date() == (datetime.datetime.now() + datetime.timedelta(hours=24)).date()


def is_today(d, timezone=None):
    return d.date() == datetime.datetime.now().date()
