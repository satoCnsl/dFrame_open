
import pytest
from flask  import session
from datetime import datetime 
from dframe import db
from dframe import formInfoGetter
from dframe import constant

def init_db(app):
    with app.app_context():
        formInfoGetter.exec_sql('update dframe_testbed.__systemini set language="eng" where id=1',isResults = False, commitReq=True )

        db.get_db()      
        formInfoGetter.exec_sql('DROP TABLE IF EXISTS testbed.post2, testbed.post3, testbed.test', isResults = False) 
        formInfoGetter.exec_sql('USE dframe_testbed', isResults = False) 
        formInfoGetter.exec_sql('DELETE FROM dframe_testbed.__object', isResults = False) 
        formInfoGetter.exec_sql('DELETE FROM dframe_testbed.__list_view', isResults = False)       
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object           AUTO_INCREMENT =  100', isResults = False)        
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object_field     AUTO_INCREMENT = 1000', isResults = False)        
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object_field_rw  AUTO_INCREMENT = 1000', isResults = False)      
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__list_view        AUTO_INCREMENT = 100', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__list_view_filter AUTO_INCREMENT = 1000', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__list_view_field  AUTO_INCREMENT = 1000', isResults = False) 
    
@pytest.mark.parametrize(('sql', 'isResults', 'out', 'commitReq', 'logOff', 'result' ),(
    ('select "test" as value',                             True, None, False, False, [{'value': 'test'}]),
    ('select "test" as value',                             False,None, False, False,[]),
    ('select * from dframe.__account where id < 0',        True, None, False, False, []),
    ( '',                            True, '"test" as value', False, False, [{'value': 'test'}]),
    ('drop   table if exists testbed.test01',               False,None, True,  False, [{'NewID': 0}]),
    ('create table  testbed.test01 (id int auto_increment, fld text, primary key (id)) ', False,None, True,  False, [{'NewID': 0}]),
    ('insert into testbed.test01 (fld) value("TEST DATA1") ',  False,None, True,  False, [{'NewID': 1}]),
    ('drop   table if exists testbed.test01',               False,None, True,  False, [{'NewID': 0}]),
))

def test_exec_sql(app, sql, isResults, out, commitReq, logOff, result):
    with app.app_context():
        res = formInfoGetter.exec_sql(sql, isResults, out, commitReq, logOff) 
    assert res == result


@pytest.mark.parametrize(('kindOfInfo', 'cpath', 'sql_app','Results'),(
    ('sql_app', [0,0,0,0,0,0], 'select id,name,title,masterObjectID from dframe_testbed.__object_v where id=11',
    [{'id': 11, 'name':'__report', 'title': 'Desining Report'}]
    ),     
))

def test_get_form_info(app,kindOfInfo, cpath, sql_app, Results):  
    with app.app_context():
        result = formInfoGetter.get_form_info(kindOfInfo, cpath, sql_app = sql_app)
        assert result[0]['id']           == Results[0]['id']
        assert result[0]['name']         == Results[0]['name']
        assert result[0]['title']        == Results[0]['title']


@pytest.mark.parametrize(('kindOfInfo','DFcpath',  'isRawValue', 'Results'),(
    ('FormPrpty',   [2,0,21,0,8,0],  0, 'call dframe.getFormPrpty("dframe_testbed",2,99,21,0)'),
    ('FormColumns', [11,0,0,0,0,0],  0, 'call dframe.getFormColumns("dframe_testbed",11,99,0,0)'),  
    ('FormColumns', [11,0,0,0,8,0],  0, 'call dframe.getFormColumns("dframe_testbed",11,99,0,8)'),  
    ('FormData',    [11,0,0,0,8,0],  0, 'call dframe.getFormData("dframe_testbed",11,99,0,0,0,0,0,8,0)'), 
    ('FormData',    [11,-1,0,0,0,0], 0, 'call dframe.getFormData("dframe_testbed",11,99,-1,0,0,0,0,0,0)'), 
    ('FormData',    [2,0,21,2,0,0],  0, 'call dframe.getFormData("dframe_testbed",2,99,0,21,0,0,0,0,2)'),    
    ('FormButton',  [11,0,0,0,0,0],  0, 'call dframe.getFormButton("dframe_testbed",11,99,0,0)'), 
    ('FormButton',  [11,-1,0,0,0,0], 0, 'call dframe.getFormButton("dframe_testbed",11,99,-1,0)'), 
    ('FormButton',  [2,0,21,2,0,0],  0, 'call dframe.getFormButton("dframe_testbed",2,99,0,2)'),    
    ('FormColumnsPivot',[11,0,0,0,8,0],0, 'call dframe.getFormColumnsPivot("dframe_testbed",11,99)'),
    ('FormPivotData', [11,0,0,0,8,0],0, 'call dframe.getFormPivotData("dframe_testbed",11,0,8)'),
    ('FormMenuBar',[11,0,0,0,8,0],0, 'call dframe.getFormMenuBar("dframe_testbed",11,99,8)'),
))
def test_get_sql(app,kindOfInfo, DFcpath, isRawValue, Results):
    with app.test_request_context():
        session['user_id'] = 99
        session['socketDb'] = 'dframe_testbed'
        result = formInfoGetter.get_sql(kindOfInfo ,DFcpath, isRawValue=isRawValue)
        assert result == Results



@pytest.mark.parametrize(('srcObjID', 'object_id', 'view_id', 'categoryNm','Results'),(
    (0,  0, 0, "sex", [('',''),('0','Male'),('1','Female')]), 
    (16, 0, 0, '',  [(1, 'Administrator')]), 
    ( 2, 4, 0, '',  [('',''),('48','ID'),('49','Name'),('50','Email'),('51','Password')]),
    ( 1, 0, 0, '', [('',''),('4','User Account'),('6','Trigger')]),
    ( 1, 1, 0, '', [('',''),('4','User Account'),('6','Trigger')]),
    ( 1, 1, 1, '', [('',''),('id','□'),('name','Name(Table Name)'),('title','Title')])
)) 
def test_getSelectList(app, srcObjID, object_id, view_id, categoryNm, Results):  
    with app.test_request_context():
        formInfoGetter.exec_sql('update dframe_testbed.__systemini set language="eng" where id=1',isResults = False, commitReq=True )
        session['user_id'] = 1
        session['appName'] = 'testbed'
        result = formInfoGetter.getSelectList(srcObjID, object_id, view_id, categoryNm)
    
    i = 0
    for r in Results:
        assert result[i] == r
        i += 1


@pytest.mark.parametrize(('data_key_set', 'sql_body', 'tbl_name', 'Results'),(
    ( [1, -1, 0, 2, 0,0],
      ('name,title,runningType,descriptions', '"post2","BLOG2",0,"test2"',  '', '', '' ,'', '' , '"testbed"', '"post2"'),
      'post2' ,
      [ [{'id':100, 'name': 'post2', 'title': 'BLOG2', 'runningType': 0,'descriptions':'test2'},],
        [{'id':1200, 'objectID': 100, 'name': 'id', 'title':'□', 'dataType': 'int'},
         {'id':1201, 'objectID': 100, 'name': 'modifiedBy', 'title':'Modified By', 'dataType': 'int'},
         {'id':1202, 'objectID': 100, 'name': 'modifiedAt', 'title':'Modified At', 'dataType': 'datetime'},
         {'id':1203, 'objectID': 100, 'name': 'createdAt',  'title':'Created At',  'dataType': 'datetime'},],
        [{'id':300, 'objectID': 100, 'roleID': 1, 'isAccessible':1}],
        [{'id':400, 'objectFieldID': 1200, 'roleID': 1, 'fieldRwID': 2},
         {'id':401, 'objectFieldID': 1201, 'roleID': 1, 'fieldRwID': 1},
         {'id':402, 'objectFieldID': 1202, 'roleID': 1, 'fieldRwID': 1},
         {'id':403, 'objectFieldID': 1203, 'roleID': 1, 'fieldRwID': 1}],
        [{'TABLE_NAME':'post2'}] ]
    ),     
    
    ([2, -1, 0, 2, 0,0],
     ('objectID,name,title,dataType,dataLength,NumOfLines,width,defaultExpression,isNotNull,foreignObjectID, \
      isMultiSelect,isMasterObject,isBulkSearchField,seq',
      '100,"post_name","Post Name","text",10,1,10,"Hank Sato",0,0, 0,0,0,10', \
      'post_name',  '"text"', 0, 'testbed' ,'post2', '' , ''),
     'post2' ,
     [ [{'id':1204, 'objectID': 100, 'name': 'post_name',  'title':'Post Name',  'dataType': 'text'}],
       {'id':404, 'objectFieldID': 1204, 'roleID': 1, 'fieldRwID': 2},
       {'Field':'post_name', 'Type':'text', 'Null':'NO', 'Key':'', 'Default':None, 'Extra':''}  ]
    ),     
    
    ([100, -1, 0, 2, 0,0],
     ('post_name', '"Jim Beans"', '', '', '', 'testbed' ,'post2', '' , ''), 
     '',
     [{'id':1, 'post_name':'Jim Beans'}  ]
    ),     

))

def test_ins_data_line(app, data_key_set, sql_body, tbl_name, Results):
    with app.test_request_context():
        d = db.get_db()
        session['user_id'] = 1
        session['appName'] = 'testbed'
        if data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT:
            if data_key_set[constant.ENTITY_ID] == -1:
                formInfoGetter.exec_sql('DELETE FROM dframe_testbed.__object', isResults = False) 
                formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object          AUTO_INCREMENT =  100', isResults = False)  
                formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object_field    AUTO_INCREMENT =  1200', isResults = False)  
                formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object_security AUTO_INCREMENT =   300', isResults = False) 
                formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__object_field_rw AUTO_INCREMENT =   400', isResults = False)     
                formInfoGetter.exec_sql('DROP TABLE IF EXISTS testbed.' + tbl_name , isResults = False) 
       
        response = formInfoGetter.ins_data_line(data_key_set, sql_body)

        if data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT:
            __object_data = formInfoGetter.exec_sql('SELECT id, name, title, runningType, descriptions \
                                                  FROM dframe_testbed.__object  WHERE id = ' + str(response))
            __object_field_data = formInfoGetter.exec_sql('SELECT id, objectID, name, title, dataType \
                            FROM dframe_testbed.__object_field WHERE objectID=' + str(response) + ' ORDER BY id')
            __object_security_data = formInfoGetter.exec_sql('SELECT id, objectID, roleID, isAccessible \
                            FROM dframe_testbed.__object_security WHERE objectID=' + str(response) + ' ORDER BY id')
            __object_field_rw_data = formInfoGetter.exec_sql('SELECT id, objectFieldID, roleID, fieldRwID \
                            FROM dframe_testbed.__object_field_rw \
                            WHERE objectFieldID >=' +str(Results[1][0]['id']) + ' AND objectFieldID <=' + str(Results[1][3]['id']))
            created_table = formInfoGetter.exec_sql('SELECT TABLE_NAME FROM information_schema.tables \
                                    WHERE table_schema =' + sql_body[7]+ ' AND table_name = ' + sql_body[8] )
            created_fields = formInfoGetter.exec_sql('SHOW COLUMNS FROM testbed.' + tbl_name )
            assert __object_data           == Results[0]
            assert __object_field_data     == Results[1]
            assert __object_security_data  == Results[2]
            assert __object_field_rw_data  == Results[3]
            assert created_table           == Results[4]
            assert len(created_fields)     == len(__object_field_data)
        
        elif data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT_FIELD:
            __object_field_data = formInfoGetter.exec_sql('SELECT id, objectID, name, title, dataType \
                            FROM dframe_testbed.__object_field WHERE id = ' + str(response))
            __object_field_rw_data = formInfoGetter.exec_sql('SELECT id, objectFieldID, roleID, fieldRwID \
                            FROM dframe_testbed.__object_field_rw WHERE objectFieldID = ' + str(response))
            created_fields = formInfoGetter.exec_sql('SHOW COLUMNS FROM testbed.' + tbl_name )
            assert __object_field_data      == Results[0]
            assert __object_field_rw_data[0]  == Results[1]
            isFound = False
            for f in created_fields:
                if (f['Field'], f['Type'], f['Null'], f['Key']) == \
                    (Results[2]['Field'], Results[2]['Type'], Results[2]['Null'], Results[2]['Key']):
                    isFound = True
            assert isFound
                                         
        else:
            result = formInfoGetter.exec_sql('SELECT id,' + sql_body[0] + ' FROM ' + sql_body[5] + '.' + sql_body[6] + \
                             ' WHERE id =' + str(response))            
            assert result == Results
        

@pytest.mark.parametrize(('data_key_set', 'setBody', 'Results'),(   
    ( [2, 1204, 0, 2, 0, 0], 
      ('objectID=100, name="name",title="Name",dataType="text(64)",modifiedBy=111,isNotNull=True','',  'post_name name', \
       'varchar(60)', '', 'testbed', 'post2', '""', '"p"', False, True),[
      {'id':1204, 'name': 'name', 'modifiedBy':111},
       ]),
    ( [100, 1, 0, 0, 0, 0], 
      ('name="Old Per",modifiedBy=123','',  '', '', '', 'testbed', 'post2', '""', '""', True, False),[
      {'id':1, 'name': 'Old Per', 'modifiedBy': 123},
       ]),       
    ( [1, 100, 0, 2, 0, 0], 
      ('name="post3",title="BLOG3",runningType=0,descriptions="BLOG POST3",modifiedBy=567','',  '', '', '', \
      'testbed', 'post2', '""', '"post3"', False, True),[
      {'id':100, 'name': 'post3', 'modifiedBy':567},
    ]),
))
def test_updt_data_line(app, data_key_set, setBody, Results): 
    with app.test_request_context():
        session['user_id'] = 88
        session['socketDb'] = 'dframe_testbed'
        resultPre = formInfoGetter.get_form_info('FormData',data_key_set)
        formInfoGetter.updt_data_line(data_key_set, setBody)
        result = formInfoGetter.get_form_info('FormData',data_key_set)
        print('resultPre:', resultPre)
        print('result:', result)
        assert result[0]['id']          == Results[0]['id']
        assert result[0]['name']        == Results[0]['name']
        assert result[0]['modifiedAt'].strftime('%Y/%m/%d %H:%M') == datetime.now().strftime('%Y/%m/%d %H:%M')



@pytest.mark.parametrize(('appID','Results'),(
    (1, 'Object'),
    (2, 'Object Field'),
    (100, 'BLOG3'),
))
def test_get_app_name(app, appID, Results):
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        response = formInfoGetter.get_app_name(appID)
        assert response == Results
        

@pytest.mark.parametrize(('tableNm', 'id', 'fldNm', 'where','Results'),(
    ('__object', 100, 'Title', None, 'BLOG3'),
    ('__object_field', 0, 'dataType', 'id=1204', 'text(64)'),
))
def test_getObjFldVal(app, tableNm, id, fldNm, where,Results):
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        response = formInfoGetter.getObjFldVal(tableNm, id, fldNm, where)
        assert response == Results


@pytest.mark.parametrize(('data_key_set', 'result'),(
    ([1, 16,  0, 2, 0, 0], [{'seq':1, 'id':1, 'name':'設定', 'isSystemUse':1},{'seq':2, 'id':2, 'name':'管理', 'isSystemUse':1}]),
    ([1, 16,  0, 0, 0, 0], [{'seq':999, 'id':3, 'name':'(すべて)', 'isSystemUse':0}]),
    ([2,  0, 16, 2, 0, 0], [{'seq':1, 'id':4, 'name':'_', 'isSystemUse':1}]),
    ([2,  0,  0, 0, 0, 0], []),
))
def test_getListViewName(app, data_key_set, result):
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        response = formInfoGetter.getListViewName(data_key_set)
        assert response ==  result
        


@pytest.mark.parametrize(('socketDb', 'user_id', 'objectID', 'viewID', 'Results'),(
    ('dframe', 1, 16, 0,
    [('151', '□'), ('152', '役割名称'),('153', '最終更新日時'), ('154', '作成日時')]),
    ('dframe_testbed', 1, 100, 0,
    [('1200', '□'), ('1204', 'Name'), ('1201', 'Modified By'),('1202', 'Modified At'), ('1203', 'Created At')]),
))
def test_getFieldList(app, socketDb, user_id, objectID, viewID, Results):
    with app.test_request_context():
        response = formInfoGetter.getFieldList(socketDb, user_id, objectID, viewID)
        assert response == Results





@pytest.mark.parametrize(('isSystemUse', 'fieldName', 'result', 'language'),(
    (0,     'Blog',        'Blog',        'eng'),
    (False, 'Name',        '名前',        'jpn'),
    (True,  'Customizing', 'ｶｽﾀﾏｲｽﾞ',        'jpn'),
    (True,  'Setting',     'Setting',     'eng'),
))
def test_getFieldCaption(app, isSystemUse, fieldName, result, language):    
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        formInfoGetter.exec_sql('update dframe_testbed.__systemini set language="' + language + '" where id=1',isResults = False, commitReq=True )
        if isSystemUse :
            response = formInfoGetter.getFieldCaption(isSystemUse, '')      
            assert response[fieldName] == result
        else:
            response = formInfoGetter.getFieldCaption(isSystemUse, fieldName)
            assert response == result
            

@pytest.mark.parametrize(('msg_id', 'language', 'result'),(
    (1, 'jpn',        'URL, アプリケーション名、画面の構成、画面の表示言語などを設定します。'),
    (1, 'eng',        'URL, アプリケーション名、画面の構成、画面の表示言語などを設定します。'),
))
def test_getDicDescription(app, msg_id, language, result):    
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        formInfoGetter.exec_sql('update dframe_testbed.__systemini set language="' + language + '" where id=1',isResults = False, commitReq=True )
        response = formInfoGetter.getDicDescription(msg_id)
        assert response == result


@pytest.mark.parametrize(('data_key_set', 'isUpdate', 'result'),(
    ([2,  0, 16, 2, 0, 0], False, {'dbName':'dframe', 'name':'__role'}),
    ([2,  0,  0, 2, 0, 0], False, {'dbName':'dframe_testbed', 'name':'__object_field'}),
    ([1, 16,  0, 2, 0, 0], False, {'dbName':'dframe', 'name':'__role'}),
    ([16,16,  0, 2, 0, 0], False, {'dbName':'dframe', 'name':'__role'}),
    ([16,16,  0, 0, 0, 0], False, {'dbName':'dframe', 'name':'__role'}),
    ([2,1204,  0, 2, 0, 0], False, {'dbName':'testbed', 'name':'post3'}),
))


def test_get_table_name(app, data_key_set, isUpdate, result):
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        response = formInfoGetter.get_table_name(data_key_set, isUpdate)
        assert response ==  result


@pytest.mark.parametrize(('data_key_set', 'result'),(
    ([2,  1, 0,  2, 0, 0], 'id'),
    ([16,  1, 0,  2, 0, 0], None),
    ([2, 1204, 0,  2, 0, 0], 'name'),
))

def test_get_table_field_name(app, data_key_set, result):
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        response = formInfoGetter.get_table_field_name(data_key_set)
        print(response)
        assert response ==  result



@pytest.mark.parametrize(('data_key_set', 'reference'),(
    ([100,1,0,0,0,0], {'cnt':'select count(id) c from testbed.post3 where id=1',
                       'col':None, 'tbl':None}),
    ([2,1204,0,2,0,0], {'cnt':'select count(id) c from dframe_testbed.__object_field where id=1204', 
                       'col':'show columns from testbed.post3 where field="name"', 'tbl':None} ),
    ([1,100,0,2,0,0], {'cnt':'select count(id) c from dframe_testbed.__object where id=100', 'col':None,
                       'tbl':'select count(*) c from information_schema.tables \
                        where table_schema="testbed" and table_name="post3"'} ),
))
def test_delete_data_line(app, data_key_set, reference):
  with app.test_request_context():
      session['socketDb'] = 'dframe_testbed'
      cnt_p = formInfoGetter.exec_sql(reference['cnt'])
      assert cnt_p[0]['c'] == 1
      if reference['col'] != None:
        col_p = formInfoGetter.exec_sql(reference['col'])
        assert len(col_p) == 1
      if reference['tbl'] != None:
        tbl_p = formInfoGetter.exec_sql(reference['tbl'])
        assert tbl_p[0]['c'] == 1
      
      formInfoGetter.delete_data_line(data_key_set)        

      cnt = formInfoGetter.exec_sql(reference['cnt'])
      assert cnt[0]['c'] == 0
      if reference['col'] != None:
        col = formInfoGetter.exec_sql(reference['col'])
        assert len(col) == 0
      if reference['tbl'] != None:
        tbl = formInfoGetter.exec_sql(reference['tbl'])
        assert tbl[0]['c'] == 0
