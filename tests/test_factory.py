
from dframe import create_app
from dframe import formInfoGetter


def test_config(app):
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing