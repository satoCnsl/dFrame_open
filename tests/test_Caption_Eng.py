from unittest import result
from urllib import response
from flask_wtf import FlaskForm
import pytest
from flask import g, session
from datetime import date,datetime
from dframe import commonTool, formInfoGetter 



@pytest.mark.parametrize(('sourceObject_id', 'object_id', 'view_id', 'categoryNm','Results'),(
                         
    (12, 0, 0,'sex',[('',''),('0', '男性'),('1', '女性')]), 
    (16, 0, 0,'',[(1, '管理者'), (2, 'Member'), (3, 'Visitor'), (4, 'Director'), (5, 'Staff'), (6, '(not used1)'), (7, '(not used2)')]), 
    ( 2, 21, 0, '',[('', ''),('169', '□')]), 
))
def test_getSelectList(app, sourceObject_id, object_id, view_id, categoryNm,Results):  
    with app.test_request_context():
        formInfoGetter.exec_sql('update dframe_testbed.__systemini set language="jpn" where id=1')
        session['user_id'] = 1 
        session['appName'] = 'testbed'
        result = formInfoGetter.getSelectList(sourceObject_id, object_id, view_id, categoryNm)
    
    for i in range(len(Results)):
        assert result[i] == Results[i]


@pytest.mark.parametrize(('dbName', 'user_id', 'objectID','viewID','Results'),(
    ('dframe', 1, 12, 0,
      [('109', '□'), ('110', 'カテゴリー'), ('111', 'タイトル'), ('112', '値'),  \
       ('113', '順番'), ('114', '最終更新日時'), ('115', '作成日時')]) ,
))
def test_getFieldList(app, dbName, user_id, objectID, viewID, Results):
    with app.app_context():
        response = formInfoGetter.getFieldList(dbName, user_id, objectID, viewID)
        assert response == Results
    with app.test_request_context():
        formInfoGetter.exec_sql('update dframe_testbed.__systemini set language="eng" where id=1')
