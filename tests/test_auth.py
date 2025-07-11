import pytest,sys
from flask import g, session

def test_login(client, auth):
    assert client.get('/dframe/auth/login/').status_code == 200
    response = auth.login()

    assert response.headers['Location'] == 'http://localhost/dframe/auth/login/'
    response = client.post('/dframe/auth/login/',data={'username':'testbed','password':'password', 'appSelNm':'testbed'})
    with client:
        client.get('/')
        assert session['user_id'] == 23
        assert g.user['name'] == 'testbed'


def test_load_logged_in_user(client, auth):
    with client:
        auth.login()
        assert g.user['name'] == 'testbed'


def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        client.get('/logout')
        assert 'user_id' not in session
