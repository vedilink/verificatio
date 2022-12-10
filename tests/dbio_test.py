# -*- coding: utf-8 -*-

import unittest
from verificatio.database import setup_db, generate, retrieve, purge


TEST_DOMAIN = "google.com"


def test_dbio_generate():
    setup_db()
    assert generate(TEST_DOMAIN, 'TXT') != None
    assert generate(TEST_DOMAIN, 'TXT') != generate(
        TEST_DOMAIN, 'CNAME')
    assert generate(TEST_DOMAIN, 'TXT') == generate(
        TEST_DOMAIN, 'TXT')

def test_dbio_retrieve():
    setup_db()
    code = generate(TEST_DOMAIN, 'FILE')
    assert retrieve(TEST_DOMAIN, 'FILE') == code
    assert retrieve(TEST_DOMAIN, 'META') == None

def test_dbio_purge():
    setup_db()
    file = generate(TEST_DOMAIN, 'FILE')
    cname = generate(TEST_DOMAIN, 'CNAME')
    purge(TEST_DOMAIN, 'FILE')
    new_file = generate(TEST_DOMAIN, 'FILE')
    new_cname = generate(TEST_DOMAIN, 'CNAME')
    assert file != new_file
    assert cname == new_cname