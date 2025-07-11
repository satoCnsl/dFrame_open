import pytest
from flask import current_app, g
from dframe import db
from dframe import formInfoGetter

def test_get_db(app):
    with app.app_context():
        response = db.get_db()
        assert response != None
        assert response == g.pop('db', None)


def test_close_db(app):
    with app.app_context():
        db.get_db()
        db.close_db()
        assert g.pop('db', None) == None


'''
@pytest.mark.parametrize(('sqlfile', 'table_name', 'num_of_record'),(
    ('data.sql','post',2),
))
def test_init_db(app, sqlfile, table_name, num_of_record):
    with app.app_context():
        response = db.init_db(sqlfile)
        assert len(response) == num_of_record
'''
