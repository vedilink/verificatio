# -*- coding: utf-8 -*-

import os

CHECK_TYPES = ['CNAME', 'TXT', 'META', 'FILE']
SERVICE_PREFIX = os.environ.get('PREFIX', 'vedilink-site-verification')
CNAME_VALUE = os.environ.get('CNAME_VALUE', 'domainverify.vedilink.com')
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///verificatio.db')
FAKE_USER_AGENT = os.environ.get('FAKE_USER_AGENT', 'Mozilla/5.0; Verificatio/1.0')
