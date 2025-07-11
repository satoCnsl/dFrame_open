import pytest
from flask  import session
from dframe import trailKeeper


@pytest.mark.parametrize(('cpath', 'result'),(
    ([0,1,2,3,4,5],       [0,1,2,3,4,5]),
    ([5,6,7,8,9,10],      [5,6,7,8,9,10]), 
    ([11,12,13,12,15,16], [11,12,13,12,15,16]), 
))
def test_get_curr_path(app, cpath, result): 
    with app.app_context():
        trailKeeper.push_trail(cpath)
        response =trailKeeper.get_curr_path()
        assert response == result

def test_init_trail(app):
    with app.app_context():
        trailKeeper.push_trail([1,2,3,4,5,6])
        trailKeeper.init_trail()
        response = trailKeeper.get_curr_path()
        assert response == []

def test_push_trail(app): 
    with app.app_context():
        trailKeeper.push_trail([1,1,1,1,1,1])
        assert trailKeeper.get_curr_path() == [1,1,1,1,1,1]


def test_pop_up_trail(app): 
    with app.app_context():
        trailKeeper.push_trail([8,0,0,0,0,0]) 
        trailKeeper.push_trail([9,0,0,0,0,0])
        response1 = trailKeeper.pop_up_trail()
        assert response1 == [8,0,0,0,0,0]


@pytest.mark.parametrize(('master_object_id'),(
    (99),
))
def test_get_master_object_id(app, master_object_id): 
    with app.app_context():
        trailKeeper.push_trail([18,0,99,0,0]) 
        trailKeeper.push_trail([19,0,0,0,0])
        response = trailKeeper.get_master_object_id()

        assert response == master_object_id


@pytest.mark.parametrize(('data_key_set','app_name'),(
    ([1, 0, 0, 0, 0, 0],  'Object'),
    ([1, 0, 0, 2, 1, 0],  'Object'),
    ([12,0,0,0,0,0],      'Base Values'),
))
def test_get_current_app_name(app, data_key_set, app_name): 
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        trailKeeper.push_trail(data_key_set) 
        response = trailKeeper.get_current_app_name()
        assert response == app_name
