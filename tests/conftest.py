import os
import tempfile

import pytest
from flask  import session

from dframe import create_app
from dframe import db, formInfoGetter

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    data_sql = f.read().decode('utf8')


@pytest.fixture(scope='module')
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope='module')
def client(app):
    print('conf34: passed')
    return app.test_client()


@pytest.fixture
def runner(app):
    print('conf40: passed')
    return app.test_cli_runner()

class indexActions(object):
    def __init__(self, client):
        self.client = client

    def index(self):
        print('conf48: passed')
        return self._client.post('/')

    def index(self):
        print('conf52: passed')
        return self._client.post('/dframe/navi/i/0/' + str(1) + '/""/0/0')

@pytest.fixture
def indexRun(client):
    print('conf57: passed')
    return indexActions(client)

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/dframe/auth/login',
            data={'username': username, 'password': password, 'appSelNm':'testbed'}
        )

    def logout(self):
        return self._client.get('/auth/logout/')


@pytest.fixture
def auth(client):
    return AuthActions(client)