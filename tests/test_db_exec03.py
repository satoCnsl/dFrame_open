import pytest
from dframe import formInfoGetter
from dframe import db

from flask import g, session

def init_db(app):
    with app.app_context():
        formInfoGetter.exec_sql('drop database if exists testbed', logOff=True)
        formInfoGetter.exec_sql('create database testbed', logOff=True)        
        formInfoGetter.exec_sql('USE dframe_testbed', isResults = False) 
        formInfoGetter.exec_sql('DELETE FROM dframe_testbed._object',     commitReq=True, isResults = False) 
        formInfoGetter.exec_sql('DELETE FROM dframe_testbed.__list_view', commitReq=True, isResults = False)   
        formInfoGetter.exec_sql('DELETE FROM dframe_testbed.__report',    commitReq=True, isResults = False)       
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object           AUTO_INCREMENT =  100', isResults = False)        
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object_field     AUTO_INCREMENT = 1000', isResults = False)        
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object_field_rw  AUTO_INCREMENT = 1000', isResults = False)      
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__list_view        AUTO_INCREMENT = 100', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__list_view_filter AUTO_INCREMENT = 1000', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__list_view_field  AUTO_INCREMENT = 1000', isResults = False)      
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__report           AUTO_INCREMENT = 100', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__report_scope     AUTO_INCREMENT = 1000', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__report_schema    AUTO_INCREMENT = 1000', isResults = False)    

def test_login(client, auth):
    assert client.get('/dframe/auth/login/').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/dframe/auth/login/'

    response = client.post('/dframe/auth/login/',data={'username':'testbed','password':'password', 'appSelNm':'testbed'})
    with client:
        client.get('/')
        assert session['user_id'] == 23
        assert g.user['name'] == 'testbed'


@pytest.mark.parametrize(('script', 'num_of_records'),(
   (' select portalViewID id from dframe_testbed.__systemini where id=1',0),
   (' call dframe.getFormPrpty("dframe_testbed",1,23,0,0)',0),
   (' call dframe.getFormColumns("dframe_testbed",1,23,0,0)',0),
   (' call dframe.getFormData("dframe_testbed",1,23,0,0,0,0,0,0,0)',0),
   (' call dframe.getFormData("dframe_testbed",1,23,0,0,0,True,0,0,0)',0),
   (' call dframe.getFormLinkage("dframe_testbed",1)',0),
   (' SELECT IFNULL(defaultViewID,0) dv FROM dframe_testbed.__object_v  WHERE id= 1',0),
   (' call getRecTypeInfo(100, 0, 0)',0),
   (' call getFieldCaption("dframe_testbed", False, "Open")',0),
   (' call getRecTypeInfo(101, 0, 0)',0),
   (' call dframe.getFormButton("dframe_testbed",1,23,0,0)',0),
   (' select seq, id, name, isSystemUse  from dframe_testbed.__list_view_v where objectID=1 and isSystemUse = 0 ORDER BY seq ',0),
   (' select IFNULL(dic.toString ,o.title) as Title from dframe_testbed.__object_v o  left join         ( select toString, ordinaryWord from dframe.__caption_dic cd inner join dframe_testbed.__systemini  si             on si.language = cd.language) dic          on o.title = dic.ordinaryWord where id = 1 limit 1',0),
   (' call dframe.getFormData("dframe_testbed",1,23,0,0,1,0,0,0,0)',0),
   (' call getFieldCaption("dframe_testbed", False, "Application")',0),
   (' call getFieldCaption("dframe_testbed", False, "Setting")',0),
   (' call getFieldCaption("dframe_testbed", False, "List_of")',0),
   (' call getFieldCaption("dframe_testbed", False, "Edit")',0),
   (' call getFieldCaption("dframe_testbed", False, "Add")',0),
   (' call dframe.getFormPrpty("dframe_testbed",1,23,0,2)',0),
   (' call dframe.getFormColumns("dframe_testbed",1,23,0,1)',0),
   (' call dframe.getFormData("dframe_testbed",1,23,0,0,0,0,0,1,2)',0),
   (' call dframe.getFormData("dframe_testbed",1,23,0,0,0,True,0,1,2)',0),
   (' call dframe.getFormLinkage("dframe_testbed",1)',0),
   (' call getRecTypeInfo( 0,1,1)',0),
   (' call dframe.getFormButton("dframe_testbed",1,23,0,2)',0),
   (' select seq, id, name, isSystemUse  from dframe_testbed.__list_view_v where objectID=1 and isSystemUse = 1 ORDER BY seq ',0),
   (' call dframe.getFormData("dframe_testbed",1,23,0,0,1,0,0,1,2)',0),
   (' call dframe.getFormColumns("dframe_testbed",1,23,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",1,23,0,0,0,0,0,2,2)',0),
   (' call dframe.getFormData("dframe_testbed",1,23,0,0,0,True,0,2,2)',0),
   (' call dframe.getFormLinkage("dframe_testbed",1)',0),
   (' call getRecTypeInfo( 0,1,2)',0),
   (' call getFieldCaption("dframe_testbed", False, "Customizing")',0),
   (' call dframe.getFormData("dframe_testbed",1,23,0,0,1,0,0,2,2)',0),
   (' INSERT INTO dframe_testbed.__report (name,title,objectID,recordTypeID,foreignKeyFieldID,scopeRelFieldID,pageSize,orientation,modifiedBy) VALUES ("List _MasterA","PDF for Master A",100,0,100,0,"A4","Portrait",23)',-1),
   (' select case when dbName in ("socket", "socketObject") and "True"="True"                 then "dframe_testbed" else dbName end as dbName, case  when dbName = "socket" and "True" ="False" then concat(name , "_v") else name end as name  from dframe_testbed.__object_v where id =15',0),
   (' select case when dbName in ("socket", "socketObject") and "True"="True"                 then "dframe_testbed" else dbName end as dbName, case  when dbName = "socket" and "True" ="False" then concat(name , "_v") else name end as name  from dframe_testbed.__object_v where id =14',0),
   (' INSERT INTO dframe_testbed.__report_scope (reportID,caption,scope,seq) VALUES (100,"List of MasterA","id",1)',0),
   
   (' INSERT INTO dframe_testbed.__report_schema (reportID,type,border,align,v_align,height,width_1stCol,width_2ndCol,width_midCol,width_1stTailCol,width_2ndTailCol,fontSize,sourceData,numOfRows,numOfCols,isHeaderReq,modifiedBy) VALUES (100,"table",1,"center","middle",10,20,20,20,20,20,10,"getMasterAhdr",1,4,0,23)',-1),
   (' INSERT INTO dframe_testbed.__report_schema (reportID,type,border,align,v_align,height,width_1stCol,width_2ndCol,width_midCol,width_1stTailCol,width_2ndTailCol,fontSize,sourceData,numOfRows,numOfCols,isHeaderReq,modifiedBy) VALUES (100,"table",1,"center","middle",10,20,20,20,20,20,10,"getMasterAdata",4,4,0,23)',-1),
  
   (' call dframe.getFormPrpty("dframe_testbed",11,23,0,0)',0),
   (' call dframe.getFormPrpty("dframe_testbed",11,23,0,2)',0),
   (' call dframe.getFormColumns("dframe_testbed",11,23,0,0)',0),
   (' call dframe.getFormData("dframe_testbed",11,23,0,0,0,0,0,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",11,23,0,0,0,True,0,0,2)',0),
   (' call dframe.getFormLinkage("dframe_testbed",11)',0),
   (' call dframe.getFormButton("dframe_testbed",11,23,0,2)',0),
   (' select 0 as seq, 0 as id, "" as name, 0 as isSystemUse  UNION select seq, id, name, isSystemUse  from dframe_testbed.__list_view_v where objectID=11 and isSystemUse = 1 ORDER BY seq ',0),
   (' select IFNULL(dic.toString ,o.title) as Title from dframe_testbed.__object_v o  left join         ( select toString, ordinaryWord from dframe.__caption_dic cd inner join dframe_testbed.__systemini  si             on si.language = cd.language) dic          on o.title = dic.ordinaryWord where id = 11 limit 1',0),
   (' call dframe.getFormData("dframe_testbed",11,23,0,0,1,0,0,0,2)',0),
   (' call dframe.getFormColumns("dframe_testbed",11,23,-1,0)',0),
   (' call dframe.getFormData("dframe_testbed",11,23,-1,0,0,0,0,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",11,23,-1,0,0,True,0,0,2)',0),
   (' SELECT IFNULL(defaultViewID,0) dv FROM dframe_testbed.__object_v  WHERE id= 11',0),
   (' call getFieldCaption("dframe_testbed", False, "Detail")',0),
   (' call dframe.getFormButton("dframe_testbed",11,23,-1,2)',0),
   (' call dframe.getSelectList("testbed",1,11,23,0,"")',0),
   (' call dframe.getSelectList("testbed",8,11,23,0,"")',0),
   (' call dframe.getFormData("dframe_testbed",11,23,-1,0,1,0,0,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",11,23,-1,0,0,1,0,0,2)',0),
   (' select case when dbName in ("socket", "socketObject") and "True"="True" then "dframe_testbed" else dbName end as dbName, case  when dbName = "socket" and "True" ="False" then concat(name , "_v") else name end as name  from dframe_testbed.__object_v where id =11',0),
  
   (' call dframe.getFormPrpty("dframe_testbed",14,23,0,0)',0),
   (' call dframe.getFormPrpty("dframe_testbed",14,23,0,2)',0),
   (' call dframe.getFormColumns("dframe_testbed",14,23,0,0)',0),
   (' call dframe.getFormData("dframe_testbed",14,23,0,0,0,0,0,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",14,23,0,0,0,True,0,0,2)',0),
   (' call dframe.getFormLinkage("dframe_testbed",14)',0),
   (' call dframe.getFormButton("dframe_testbed",14,23,0,2)',0),
   (' select 0 as seq, 0 as id, "" as name, 0 as isSystemUse  UNION select seq, id, name, isSystemUse  from dframe_testbed.__list_view_v where objectID=14 and isSystemUse = 1 ORDER BY seq ',0),
   (' select IFNULL(dic.toString ,o.title) as Title from dframe_testbed.__object_v o  left join         ( select toString, ordinaryWord from dframe.__caption_dic cd inner join dframe_testbed.__systemini  si             on si.language = cd.language) dic          on o.title = dic.ordinaryWord where id = 14 limit 1',0),
   (' call dframe.getFormData("dframe_testbed",14,23,0,0,1,0,0,0,2)',0),
   (' call dframe.getFormColumns("dframe_testbed",14,23,-1,0)',0),
   (' call dframe.getFormData("dframe_testbed",14,23,-1,0,0,0,0,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",14,23,-1,0,0,True,0,0,2)',0),
   (' SELECT IFNULL(defaultViewID,0) dv FROM dframe_testbed.__object_v  WHERE id= 14',0),
   (' call dframe.getFormButton("dframe_testbed",14,23,-1,2)',0),
   (' call dframe.getSelectList("testbed",11,14,23,0,"")',0),
   (' call dframe.getFormData("dframe_testbed",14,23,-1,0,1,0,0,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",14,23,-1,0,0,1,0,0,2)',0),
   (' call dframe.getFormPrpty("dframe_testbed",15,23,0,0)',0),
   (' call dframe.getFormPrpty("dframe_testbed",15,23,0,2)',0),
   (' call dframe.getFormColumns("dframe_testbed",15,23,0,0)',0),
   (' call dframe.getFormData("dframe_testbed",15,23,0,0,0,0,0,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",15,23,0,0,0,True,0,0,2)',0),
   (' call dframe.getFormLinkage("dframe_testbed",15)',0),
   (' call dframe.getFormButton("dframe_testbed",15,23,0,2)',0),
   (' select 0 as seq, 0 as id, "" as name, 0 as isSystemUse  UNION select seq, id, name, isSystemUse  from dframe_testbed.__list_view_v where objectID=15 and isSystemUse = 1 ORDER BY seq ',0),
   (' select IFNULL(dic.toString ,o.title) as Title from dframe_testbed.__object_v o  left join         ( select toString, ordinaryWord from dframe.__caption_dic cd inner join dframe_testbed.__systemini  si             on si.language = cd.language) dic          on o.title = dic.ordinaryWord where id = 15 limit 1',0),
   (' call dframe.getFormData("dframe_testbed",15,23,0,0,1,0,0,0,2)',0),
   (' call dframe.getFormColumns("dframe_testbed",15,23,-1,0)',0),
   (' call dframe.getFormData("dframe_testbed",15,23,-1,0,0,0,0,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",15,23,-1,0,0,True,0,0,2)',0),
   (' SELECT IFNULL(defaultViewID,0) dv FROM dframe_testbed.__object_v  WHERE id= 15',0),
   (' call dframe.getFormButton("dframe_testbed",15,23,-1,2)',0),
   (' call dframe.getSelectList("testbed",11,15,23,0,"")',0),
   (' call dframe.getSelectList("testbed",12,15,23,0,"yesNo")',0),
   (' call dframe.getFormData("dframe_testbed",15,23,-1,0,1,0,0,0,2)',0),
   (' call dframe.getFormData("dframe_testbed",15,23,-1,0,0,1,0,0,2)',0),
   (' select 0 as seq, 0 as id, "" as name, 0 as isSystemUse  UNION select seq, id, name, isSystemUse  from dframe_testbed.__list_view_v where objectID=100 and isSystemUse = 0 ORDER BY seq ',0),
   (' select IFNULL(dic.toString ,o.title) as Title from dframe_testbed.__object_v o  left join         ( select toString, ordinaryWord from dframe.__caption_dic cd inner join dframe_testbed.__systemini  si             on si.language = cd.language) dic          on o.title = dic.ordinaryWord where id = 100 limit 1',0),
  
   (' select * from dframe_testbed.__report_v where id=101',0),
   (' call dframe.getRprtSchema("dframe_testbed",101)',0),
   (' call getRprtWidthVal("dframe_testbed",1002,1)',0),
   (' call getRprtWidthVal("dframe_testbed",1002,2)',0),
   (' call getRprtWidthVal("dframe_testbed",1002,3)',0),
   (' call getRprtWidthVal("dframe_testbed",1002,4)',0),
   (' call getRprtWidthVal("dframe_testbed",1003,1)',0),
   (' call getRprtWidthVal("dframe_testbed",1003,2)',0),
   (' call getRprtWidthVal("dframe_testbed",1003,3)',0),
   (' call getRprtWidthVal("dframe_testbed",1003,4)',0),

))
def test_obj021(app, client, script, num_of_records):
    
    client.post('/dframe/auth/login/', data={'username':'testbed','password':'password', 'appSelNm':'testbed'})
        
    with app.app_context():
        result = formInfoGetter.exec_sql(script, isResults=True, commitReq=True, logOff=True)
    assert len(result) >= num_of_records