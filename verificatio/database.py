# -*- coding: utf-8 -*-

import uuid
import sqlite3
import sqlalchemy as db
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from .conf import DATABASE_URL


def setup_db():
    engine = create_engine(DATABASE_URL)
    meta = MetaData()
    verificationTable = Table(
       'verification', meta,
       Column('domain', String, primary_key = True),
       Column('checktype', String, primary_key = True),
       Column('value', String),
    )
    meta.create_all(engine)


def generate(domain, check_type):
    current_code = retrieve(domain, check_type)
    if current_code is not None:
        return current_code
    uid = str(uuid.uuid4())
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    connection.execute('''
		INSERT INTO verification
		VALUES(?, ?, ?)''',
              (domain, check_type, uid))
    connection.close()
    return uid


def retrieve(domain, check_type):
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    c = connection.execute('''
			   SELECT value FROM verification
			   WHERE domain=? AND checktype=?''',
                   (domain, check_type))
    row = c.fetchone()
    if row is not None:
        return row[0]
    else:
        return None


def purge(domain, check_type):
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    connection.execute('''
    	DELETE FROM verification WHERE domain=? AND checktype=?''',
                   (domain, check_type))
    connection.close()
