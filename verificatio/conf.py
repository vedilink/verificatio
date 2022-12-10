# -*- coding: utf-8 -*-

import os

CHECK_TYPES = ['CNAME', 'TXT', 'META', 'FILE']
SERVICE_PREFIX = os.environ.get('SERVICE_PREFIX', 'vedilink-site-verification')
CNAME_HOST = os.environ.get('CNAME_HOST', 'vedilink.com')
CNAME_PREFIX = os.environ.get('CNAME_PREFIX', 'dpv')
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///verificatio.db')
FAKE_USER_AGENT = os.environ.get('FAKE_USER_AGENT', 'Mozilla/5.0; Verificatio/1.0')
