import pytest
from dframe import formInfoGetter
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


def test_createDb(app):
    with app.app_context():
        formInfoGetter.exec_sql('drop database if exists testbed', logOff=True)
        formInfoGetter.exec_sql('create database testbed', logOff=True)        
        formInfoGetter.exec_sql('USE dframe_testbed', isResults = False) 
        formInfoGetter.exec_sql('DELETE FROM __object', isResults = False) 
        formInfoGetter.exec_sql('DELETE FROM __list_view', isResults = False)       
        formInfoGetter.exec_sql('DELETE FROM __report', isResults = False)       
        formInfoGetter.exec_sql('ALTER TABLE __object           AUTO_INCREMENT =  100', isResults = False)        
        formInfoGetter.exec_sql('ALTER TABLE __object_field     AUTO_INCREMENT = 1000', isResults = False)        
        formInfoGetter.exec_sql('ALTER TABLE __object_field_rw  AUTO_INCREMENT = 1000', isResults = False)      
        formInfoGetter.exec_sql('ALTER TABLE __list_view        AUTO_INCREMENT = 100', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE __list_view_filter AUTO_INCREMENT = 1000', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE __list_view_field  AUTO_INCREMENT = 1000', isResults = False)        
        formInfoGetter.exec_sql('ALTER TABLE __report           AUTO_INCREMENT = 100', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE __report_scope     AUTO_INCREMENT = 100', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE __report_schema    AUTO_INCREMENT = 100', isResults = False)   


@pytest.mark.parametrize(('script', 'num_of_records'),(
   ('SELECT name,password,isLogActive FROM dframe.__account WHERE id = 23',0),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
   ('select portalViewID id from dframe_testbed.__systemini where id=1',0),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
   ('call dframe.getFormPrpty("dframe_testbed",1,23,0,0)',0),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
   ('call dframe.getFormColumns("dframe_testbed",1,23,0,0)',0),                         
))
def test_obj011(app, client, script, num_of_records):
    
    client.post('/dframe/auth/login/', data={'username':'testbed','password':'password', 'appSelNm':'testbed'})
        
    with app.app_context():
        result = formInfoGetter.exec_sql(script, logOff=True)
    assert len(result) >= num_of_records
                                                                      