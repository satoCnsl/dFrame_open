import pytest
from flask import request
from flask import template_rendered, session
from flask import current_app, session
#from flask_testing import TestCase, LiveServerTestCase

from dframe import auth
from dframe import trailKeeper
from dframe import formInfoGetter
from dframe import constant
from dframe import navi


@pytest.fixture    
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


def test_setting(app, client, captured_templates):
    with app.test_request_context():
        formInfoGetter.exec_sql('update dframe_testbed.__systemini set language="eng" where id=1')
    with client:
        client.post('/dframe/auth/login/', data={'username': 'admin', 'password': 'password', 'appSelNm':'testbed'})
       
        response = client.post('/dframe/navi/setting/')
        
        assert response.status_code==200
        template, context = captured_templates[0]
        assert template.name == 'list1.html'
        assert context['appName'] == 'Object'
    
def test_application(client, captured_templates):
    with client:
        client.get('/')
        client.post('/dframe/auth/login/', data={'username': 'admin', 'password': 'password', 'appSelNm':'testbed'})
       
        response = client.get('/dframe/navi/application/')
        
        assert response.status_code==200
        template, context = captured_templates[0]
        assert template.name == 'list1.html'
        assert context['appName'] == 'Object'
       
@pytest.mark.parametrize(('endpoint','templateName'),(
    ('/dframe/navi/form/13/0/0/0/0/0/', 'list1.html'),
    ('/dframe/navi/form/13/1/0/0/0/0/', 'sForm.html'),
    ('/dframe/navi/form/1/0/0/0/1/0/', 'list1.html'),
))
def test_setup_form(app, client, captured_templates, endpoint, templateName):
    with app.test_request_context():
        formInfoGetter.exec_sql('update dframe_testbed.__systemini set language="eng" where id=1',isResults = False, commitReq=True )

    with client:
        client.post('/dframe/auth/login/', data={'username': 'admin', 'password': 'password', 'appSelNm':'testbed'})
        response = client.get(endpoint)
        
        assert response.status_code==200
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == templateName
      
      
@pytest.mark.parametrize(('action_type', 'data_key_set','data_key_set_pre',  
                          'templateName', 'urlPath', 'data', 'dataLen', 'colLen'),(
    ('b',  [13, 1, 0, 2, 0, 0], [13, 0, 0, 2, 0, 0], 'sForm.html', 'dframe/navi/form/13/1/0/2/0/0/', 
     {'appNm':'testbed1','maxLinesInPage':11, 'language':'jpn'}, 1, 9),
    ('bn',  [13, 1, 0, 2, 0, 0], [13, 0, 0, 2, 0, 0], 'sForm.html', 'dframe/navi/form/13/1/0/2/0/0/', 
     {'appNm':'testbed2','maxLinesInPage':12, 'language':'jpn'}, 1, 9),
    ('bn',  [13, -1, 0, 2, 0, 0], [13, -1, 0, 2, 0, 0], 'sForm.html', 'dframe/navi/form/13/-1/0/2/0/0/', 
     {'appNm':'testbed3','maxLinesInPage':13, 'language':'jpn'}, 1, 9),
    ('c',  [13, -1, 0, 2, 0, 0], [13, 0, 0, 2, 0, 0], 'list1.html', 'dframe/navi/form/13/0/0/2/0/0/', 
     {'appNm':'testbed3','maxLinesInPage':13, 'language':'jpn'}, 1, 9),
    ('c',  [100, -1, 0, 0, 0, 0], [13, 0, 0, 2, 0, 0], 'list1.html', 'dframe/navi/form/13/0/0/2/0/0/', 
     {'appNm':'testbed3','maxLinesInPage':13, 'language':'jpn'}, 1, 9),
    ('d',  [100,  -1, 0, 0, 0, 0], [13, 0, 0, 0, 0, 0], 'list1.html', 'dframe/navi/form/13/0/0/0/0/0/', 
     {'modifiedBy':'123',}, 1, 9),
))
def test_navi_button(mocker, client, captured_templates, action_type, data_key_set, data_key_set_pre,
                     templateName, urlPath, data, dataLen, colLen ):

    with client:
        mocker.patch.object(trailKeeper,    'get_curr_path',        return_value=data_key_set)
        mocker.patch.object(trailKeeper,    'pop_up_trail',         return_value=data_key_set_pre)
        mocker.patch.object(trailKeeper,    'get_current_app_name', return_value='testbed')
        mocker.patch.object(formInfoGetter, 'updt_data_line',      return_value=None)
        mocker.patch.object(formInfoGetter, 'ins_data_line',       return_value=None)
        mocker.patch.object(formInfoGetter, 'delete_data_line',    return_value=None)
        mocker.patch.object(auth,           'load_logged_in_user', return_value=None)

        client.get('/')
        client.post('/dframe/auth/login/', data={'username': 'admin', 'password': 'password', 'appSelNm':'testbed'})
        
        client.get(urlPath)

        endpoint = '/dframe/navi/btn/'+ action_type + '/' 
        response = client.post(endpoint, data=data)
    
        assert request.form.get(next(iter(data)))        == data[next(iter(data))]        
        assert response.status_code             ==200
        template, context                       = captured_templates[0]
        assert template.name                    == templateName
        assert context['urlPath']               == urlPath
        assert len(context['formData'])         == dataLen
        assert len(context['formColumns'])      == colLen
        if templateName == 'sForm.html':
            assert context['entity_id']         == data_key_set[constant.ENTITY_ID]
    
        

@pytest.mark.parametrize(('objectID','formColumns', 'result'),(
        (1, [], 'pass'),
        (2, [{'name':'foreignObjectID', 'value':'0'},{'name':'foreignKeyFldNm', 'value':'NULL'}], 'pass'),
        (2, [{'name':'foreignObjectID', 'value':'9'},{'name':'foreignKeyFldNm', 'value':'SomeKey'},
                                                     {'name':'derivedTerm', 'value':'SomeTerm'}], 'pass'),
        (2, [{'name':'foreignObjectID', 'value':'0'},{'name':'foreignKeyFldNm', 'value':'NULL'},
             {'name':'derivedTerm', 'value':'NULL'}, {'name':'cmbStrainObjNm', 'value':'Some'}], 'pass'),
        (2, [{'name':'foreignObjectID', 'value':'NULL'},{'name':'foreignKeyFldNm', 'value':'NULL'},
                                                     {'name':'derivedTerm', 'value':'SomeTerm'}], ['failed', 10]),
        (2, [{'name':'foreignObjectID', 'value':'0'},{'name':'foreignKeyFldNm', 'value':'some'},
                                                     {'name':'cmbStrainObjNm',  'value':'Some'}], ['failed', 11]),
))
def test_check_vals(objectID, formColumns, result):
    assert navi.check_vals(objectID, formColumns) == result