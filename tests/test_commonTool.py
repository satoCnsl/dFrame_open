import pytest
from flask import g, session, request
from datetime import date,datetime 
from dframe import commonTool, formInfoGetter, constant 


def test_login(client, auth):
    assert client.get('/dframe/auth/login/').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/dframe/auth/login/'

    response = client.post('/dframe/auth/login/',data={'username':'testbed','password':'password', 'appSelNm':'testbed'})
    with client:
        client.get('/')
        assert session['user_id'] == 23
        assert g.user['name'] == 'testbed'
        assert session['socketDb'] == 'dframe_testbed'
        assert session['appName'] == 'testbed'


@pytest.mark.parametrize(('DFcpath', 'bulkSourceObjectID', 'result'),(
    ([1,2,3,4,5,6], [{'masterObjectID':1,'bulkSourceObjectID':1}], \
     ([{'masterObjectID':1,'bulkSourceObjectID':1}],'call dframe.getFormColumnsPivot("myDb",1,9)', \
      'call dframe.getFormPivotData("myDb",1,6,5)', 'call dframe.getFormPivotData("myDb",1,6,5)', \
      [],[], \
      'call dframe.getFormButton("myDb",1,9,2,4)','call dframe.getFormMenuBar("myDb",1,9,5)') \
    ),  
    ([1,2,3,40,5,6], [{'masterObjectID':1,'bulkSourceObjectID':0}], \
     ([{'masterObjectID':1,'bulkSourceObjectID':0}],'call dframe.getFormColumns("myDb",1,9,2,0)', \
      'call dframe.getFormData("myDb",1,9,2,3,0,0,6,0,40)', \
      'call dframe.getFormData("myDb",1,9,2,3,0,True,6,0,40)', \
      'call dframe.getFormLinkage("myDb",1)',[], \
      'call dframe.getFormButton("myDb",1,9,2,40)','call dframe.getFormMenuBar("myDb",1,9,5)') \
    ),  
    ([1,0,3,400,5,6], [{'masterObjectID':1,'bulkSourceObjectID':0}], \
     ([{'masterObjectID':1,'bulkSourceObjectID':0}],'call dframe.getFormColumns("myDb",1,9,0,5)', \
      'call dframe.getFormData("myDb",1,9,0,3,0,0,6,5,400)', \
      'call dframe.getFormData("myDb",1,9,0,3,0,True,6,5,400)', \
      'call dframe.getFormLinkage("myDb",1)',[], \
      'call dframe.getFormButton("myDb",1,9,0,400)','call dframe.getFormMenuBar("myDb",1,9,5)') \
    ),  
    ))  

def test_set_formparam(app, mocker, DFcpath, bulkSourceObjectID, result):
    with app.test_request_context():
        session['user_id'] =9
        session['socketDb'] = "myDb"
        mocker.patch.object(formInfoGetter, 'exec_sql', new = test_exec_sql.exec)
        mocker.patch.object(commonTool, 'set_fk_link', new = test_exec_sql.exec2)
        response = commonTool.set_formparam(DFcpath)
        assert response == result
        print(response)
        

class test_exec_sql():
    def exec(sql):
        if sql == 'call dframe.getFormPrpty("myDb",1,9,3,4)':
            sql = [{'masterObjectID':1,'bulkSourceObjectID':1}]
        elif sql == 'call dframe.getFormPrpty("myDb",1,9,3,40)':
            sql = [{'masterObjectID':1,'bulkSourceObjectID':0}]
        elif sql == 'call dframe.getFormPrpty("myDb",1,9,3,400)':
            sql = [{'masterObjectID':1,'bulkSourceObjectID':0}]
            
        return sql
    def exec2(data_key_set,formVal,formColumns):
        return  []


@pytest.mark.parametrize(('data_key_set', 'formVal', 'formColumns', 'result'),(
    ([99,0,2,0,0,0],
     [{'id':1,'name':'some1', 'title':'Some One', 'link_fld':100},
      {'id':2,'name':'some2', 'title':'Some Two', 'link_fld':101}],
     [{'name':'id',           'isVisible':0,'foreignObjectID':0, 'isMultiSelect':0},
      {'name':'name',         'isVisible':1,'foreignObjectID':0, 'isMultiSelect':0},
      {'name':'title',        'isVisible':1,'foreignObjectID':0, 'isMultiSelect':0},
      {'name':'link_fld',     'isVisible':1,'foreignObjectID':21, 'isMultiSelect':0},],
     [{'id':       {'runningModeID':0, 'offset': 0,'objectID':99, 'entityID':1, 'caption':'Detail', 'viewID': 0, 'masterObjID':0},
       'name':     {'runningModeID':0, 'objectID':0}, 
       'title':    {'runningModeID':0, 'objectID':0},  
       'link_fld': {'runningModeID':0, 'objectID':21, 'offset':0, 'entityID':100, 'masterObjID':0, 'viewID': 0}},
       {'id':      {'runningModeID':0, 'offset': 0,'objectID':99, 'entityID':2, 'caption':'Detail', 'viewID': 0, 'masterObjID':0},
       'name':     {'runningModeID':0, 'objectID':0}, 
       'title':    {'runningModeID':0, 'objectID':0},  
       'link_fld': {'runningModeID':0, 'objectID':21, 'offset':0, 'entityID':101, 'masterObjID':0, 'viewID': 0}}]),
))


def test_set_fk_link(app, data_key_set, formVal, formColumns, result):   
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        response = commonTool.set_fk_link(
            data_key_set, formVal, formColumns)
    assert response == result


@pytest.mark.parametrize(('DFcpath', 'result'),(
    ([21,1,200,30,0,0],'/21/1/200/30/0/0/'),   
    ([21,1,200,'ABC','',0],'/21/1/200/ABC//0/'),   
))
def test_set_url(DFcpath, result):
    response = commonTool.set_url(DFcpath)
    assert response == result


@pytest.mark.parametrize(('dataType','value','isViaForm', 'result'),(
    ('text','sato@v08.itscom.net' , None, '"sato@v08.itscom.net"'),
    ('int', '12345' , None, '12345'),
    ('date',date(2022, 1, 2), False, '"2022/01/02"'),
    ('date','2022/01/02', True,  '"2022/01/02"'),
    ('datetime',datetime(2022, 1, 2, 1, 2, 3), False,'"2022/01/02 01:02:03"'),
    ('datetime','2022/01/02 01:02:03', True, '"2022/01/02 01:02:03"'),
    ('bbb', '12345' , None, '12345'),
))
def test_lap_field(app, dataType, value, isViaForm, result):
    with app.test_request_context():
        response = commonTool.lap_field( dataType, value, isViaForm)
    
    assert response == result


@pytest.mark.parametrize(('isUpdate', 'colNm', 'data', 'dtType', 'result'),(
    (True,  'col01',     'abcd',                'text',     ('col01=abcd,', None)),
    (False, 'col02',     'abcd',                'text',     ('col02,','abcd,')),
    (False, 'col03',     '',                    'text',     ('col03,',',')),
    (False, 'col04',      None,                 'text',     ('','')),
    (True,  'account_id', 1,                    'int',      ('account_id=1,', None)),
    (True,  'title',     'test title 03',       'text',     ('title=test title 03,', None)) ,
    (True,  'createdAt', datetime(2023, 4,20,11,22,33), 'datetime', ('createdAt=2023-04-20 11:22:33,', None)) ,
    (False, 'account_id', 1,                    'int',      ('account_id,', '1,')),
    (False, 'title',     'test title 03',       'text',     ('title,', 'test title 03,')) ,
    (False, 'createdAt', datetime(2023, 4,20,11,22,33), 'datetime', ('createdAt,', '2023-04-20 11:22:33,')), 
))
def test_build_update_field_terms(app, isUpdate, colNm, data, dtType, result):
    with app.test_request_context():
        response = commonTool.build_update_field_terms(isUpdate, colNm, data, dtType)
    
    assert response == result


@pytest.mark.parametrize(('DFcpath', 'viewNm', 'filterSpec', 'accountID'),(
        ([9,0,   0,0,0,0], 'test01',[['200','"like"','"test"','"or"'],['201','"Notlike"','"prod"','NULL']], 1),                             
        ([9,0,1000,0,0,0], 'test02',[['200','"like"','"abcd"','"or"'],['201','"="',      '8',     None ]], 1),
        ([9,0,1000,0,0,0], 'test03',[['200','"like"','"abcd"','"or"'],['201','"="',     '28',   '"and"'], \
                                 ['202','"!="','99',None]], 1),
        ([9,0,1000,0,0,0], 'test04',[['203','"="','88',None]], 1),
))
def test_updateFilter(app, DFcpath, viewNm, filterSpec, accountID):
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        response_viewID = commonTool.updateFilter(DFcpath, viewNm, filterSpec, accountID)
        response_viewName = formInfoGetter.exec_sql('select name from ' + session['socketDb'] + \
                                                    '.__list_view where id = ' + str(response_viewID))
        filterID = formInfoGetter.exec_sql('select id from  ' + session['socketDb'] + \
                                                    '.__list_view_filter where listViewID=' + str(response_viewID))
        response_viewFieldOpr = formInfoGetter.getObjFldVal('__list_view_filter',filterID[-1]['id'],'fieldOperator')
        response_viewFieldVal = formInfoGetter.getObjFldVal('__list_view_filter',filterID[-1]['id'],'value')
    if DFcpath[constant.VIEW_ID] > 0:
        assert response_viewID == DFcpath[constant.VIEW_ID]
    else:        
        assert response_viewID > 0
    assert response_viewName[0]['name'] == viewNm
    assert response_viewFieldOpr == filterSpec[-1][1].replace('"', '')
    assert response_viewFieldVal == filterSpec[-1][2].replace('"', '')


@pytest.mark.parametrize(('colList', 'viewID', 'result'),(  
    (['1', '2', '3'], 1000, [{'id':2000, 'listViewID':1000, 'objectFieldID':1},{'id':2001, 'listViewID':1000, 'objectFieldID':2},\
                             {'id':2002, 'listViewID':1000, 'objectFieldID':3}]),  
))
def test_setViewCol(app, colList, viewID, result):
    with app.test_request_context():
        session['socketDb'] = 'dframe_testbed'
        formInfoGetter.exec_sql('DELETE FROM dframe_testbed.__list_view', isResults = False)   
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__list_view AUTO_INCREMENT = 1000', isResults = False) 
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__list_view_field AUTO_INCREMENT = 2000', isResults = False) 
        formInfoGetter.exec_sql("INSERT INTO dframe_testbed.__list_view (name, objectID ) values ('test', 1)", isResults = False)
        commonTool.setViewCol(colList, viewID)
        vfID = formInfoGetter.exec_sql('select id, listViewID, objectFieldID from dframe_testbed.__list_view_field where listViewID=' + str(viewID))
    assert vfID == result


@pytest.mark.parametrize(('DFcpath', 'dataSize', 'lineNumPerPage', 'len_pivotForm', 'result'),(
        ([12,0,0,2,0,0 ], 140, 200, 0, [[0,  0,  0,  0],  ['disabled','disabled','disabled','disabled']]),
        ([12,0,0,2,0,0 ], 140,  10, 0, [[0,  0, 10,130],  ['disabled','disabled','',        ''        ]]),
        ([12,0,0,2,0,10], 140,  10, 0, [[0,  0, 20,130],  ['',        '',        '',        ''        ]]),
        ([12,0,0,2,0,130],140, 10, 0, [[0,120,130,130],  ['',        '',        'disabled','disabled']]),
))
def test_setPageButton(app, mocker, DFcpath, dataSize, lineNumPerPage, len_pivotForm, result):
    with app.test_request_context():
        formData = []
        for i in range(dataSize):
            formData.append(i)

        mocker.patch.object(formInfoGetter, 'get_form_info', return_value=formData)
        response = commonTool.setPageButton(DFcpath, lineNumPerPage, len_pivotForm) 
    assert response == result


@pytest.mark.parametrize(('data_key_set', 'form_column_with_value', 
                          'result_fld', 'result_val','result_fld_name', 'result_dataType','result_isNotNull',
                           'result_db_name', 'result_tbl_name', 'result_new_db_name', 'result_new_tbl_name', 'result_isModify', 'result_isRename' ),(
    
    ([1,-1,0,2,0],
     [
     {'name':'id',           'isVisible':1, 'dataType':'int', 'isMasterObject':0, 'value':100,       'value_old':None ,'isReadOnly':True ,
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},
     {'name':'col_name',     'isVisible':1, 'dataType':'text','isMasterObject':0, 'value':'testTbl1','value_old':'' ,'isReadOnly':True ,
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},
     {'name':'dbName',       'isVisible':1, 'dataType':'text','isMasterObject':0, 'value':'testbed','value_old':'' ,'isReadOnly':True ,
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},
     {'name':'runningType',  'isVisible':1, 'dataType':'int', 'isMasterObject':0, 'value':0,        'value_old':None ,'isReadOnly':True ,
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},
     {'name':'descriptions', 'isVisible':1, 'dataType':'text','isMasterObject':0, 'value':None,     'value_old':None ,'isReadOnly':True ,
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},
     ],
      'col_name,runningType', 'testTbl1,0', '', '', '', '', '', 'testbed', '',False,False
     ),
    ([1,99,0,2,0],
     [
     {'name':'id',           'isVisible':1, 'dataType':'int', 'isMasterObject':0, 'value':100,          'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},
     {'name':'name',         'isVisible':1, 'dataType':'text','isMasterObject':0, 'value':'"testTbl2"', 'value_old':'"old_testTbl1"','isReadOnly':True,
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0  },
     {'name':'dbName',       'isVisible':1, 'dataType':'text','isMasterObject':0, 'value':'testbed', 'value_old':'' ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},
     {'name':'runningType',  'isVisible':1, 'dataType':'int', 'isMasterObject':0, 'value':0,           'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},
     {'name':'descriptions', 'isVisible':1, 'dataType':'text','isMasterObject':0, 'value':'"testDescript2"','value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},
     ],
      'name="testTbl2",runningType=0,descriptions="testDescript2"', '','','','','','"old_testTbl1"', 'testbed', '"testTbl2"',False,True 
     ),    
    ([2,-1,88,2,0],
     [
     {'name':'id',        'isVisible':1, 'dataType':'int',      'isMasterObject':0, 'value':99,       'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'objectID',  'isVisible':1, 'dataType':'int',      'isMasterObject':1, 'value':88,       'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'name',      'isVisible':1, 'dataType':'text',     'isMasterObject':0, 'value':'"field2"', 'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'dataType',  'isVisible':1, 'dataType':'text',     'isMasterObject':0, 'value':'text',    'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0  },
     {'name':'isNotNull', 'isVisible':1, 'dataType':'boolean',  'isMasterObject':0, 'value':1,        'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     ],
      'objectID,name,dataType,isNotNull', '88,"field2",text,1','field2','text','','', 'testTbl2', '""', '', True, False      
     ),  
    ([2, 88,0,2,0],
     [
     {'name':'id',        'isVisible':1, 'dataType':'int',      'isMasterObject':0, 'value':99,       'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'objectID',  'isVisible':1, 'dataType':'int',      'isMasterObject':1, 'value':88,       'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'name',      'isVisible':1, 'dataType':'int',     'isMasterObject':0, 'value':'"field1"', 'value_old':'name' ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'dataType',  'isVisible':1, 'dataType':'text',     'isMasterObject':0, 'value':'int',    'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0  },
     {'name':'isNotNull', 'isVisible':1, 'dataType':'boolean',  'isMasterObject':0, 'value':1,        'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     ],
      'objectID=88,name="field1",dataType=int,isNotNull=1','','name field1 ','int','','', '', '""', '', True, True
     ),     
    ([88,-1,0,0,0],
     [
     {'name':'id',        'isVisible':1, 'dataType':'int',      'isMasterObject':0, 'value':99,                   'value_old':None,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 }, 
     {'name':'accountID', 'isVisible':1, 'dataType':'int',      'isMasterObject':1, 'value':88,                   'value_old':None ,'isReadOnly':True,  
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'title',     'isVisible':1, 'dataType':'text',     'isMasterObject':0, 'value':'"title1"',             'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 }, 
     {'name':'body',      'isVisible':1, 'dataType':'text',     'isMasterObject':0, 'value':'"body1"',              'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'createdAt', 'isVisible':1, 'dataType':'datetime', 'isMasterObject':0, 'value':'"2023-11-11 01:02:03"', 'value_old':None ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 }, 
     ],
      'accountID,title,body', '88,"title1","body1"','','','','dframe', '', '""', '', False, False 
     ),      
    ([88,99,0,0,0],
     [
     {'name':'id',        'isVisible':1, 'dataType':'int',      'isMasterObject':0, 'value':99,                   'value_old':99 ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'accountID', 'isVisible':1, 'dataType':'int',      'isMasterObject':1, 'value':77,                   'value_old':88 ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'title',     'isVisible':1, 'dataType':'text',     'isMasterObject':0, 'value':'"title2"',             'value_old':'title1' ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'body',      'isVisible':1, 'dataType':'text',     'isMasterObject':0, 'value':'"body2"',              'value_old':'body1' ,'isReadOnly':True, 
             'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0 },
     {'name':'createdAt', 'isVisible':1, 'dataType':'datetime', 'isMasterObject':0, 'value':'"2023-11-12 21:22:23"', 
      'value_old':'"2023-11-12 01:02:03"','isReadOnly':True, 'derivedTerm': '', 'cmbstrainObjNm': '', 'foreignObjectID':0},  ],

      'accountID=77,title="title2",body="body2"', '','','','','dframe', '', '""', '', False, False
     ),   
))

def test_compile_sql(app, mocker, data_key_set, form_column_with_value, result_fld, result_val,result_fld_name,result_dataType,result_isNotNull,
                     result_db_name, result_tbl_name, result_new_db_name, result_new_tbl_name, result_isModify, result_isRename ):
    with app.app_context():
        mocker.patch.object(formInfoGetter, 'get_table_name', return_value={'name':result_tbl_name, 'dbName':result_db_name} )
        response = commonTool.compile_sql(data_key_set, form_column_with_value)
        assert response[0] == result_fld
        assert response[1] == result_val
        assert response[2] == result_fld_name
        assert response[3] == result_dataType
        assert response[4] == result_isNotNull
        assert response[5] == result_db_name
        assert response[6] == result_tbl_name
        assert response[7] == result_new_db_name
        assert response[8] == result_new_tbl_name
        assert response[9] == result_isModify
        assert response[10] == result_isRename


@pytest.mark.parametrize(('formName', 'formColmns', 'formData', 'objectID', 'formVal', 'valueSet'),(
    ('sForm', [{'objectID':99,'name':'some3Search', 'title':'SOME3', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
               'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'1st Row', \
               'isBulkSearchField':1, 'description':'SOME3 SEARCH' },
               {'objectID':99,'name':'some3Data', 'title':'SOME3DATA', 'dataType':'text', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
               'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'1st Row', \
               'isBulkSearchField':0, 'description':'SOME3 DATA' }], 
              [{'some3Search':900, 'some3Data':'AAA'}], 99, \
              [{'some3Search':910, 'some3Data':'DDD'}], None),
    ('bForm', [{'objectID':99,'name':'some3Search', 'title':'SOME3', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
               'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'1st Row', \
               'isBulkSearchField':1, 'description':'SOME3 SEARCH' },
               {'objectID':99,'name':'some3Data', 'title':'SOME3DATA', 'dataType':'text', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
               'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'1st Row', \
               'isBulkSearchField':0, 'description':'SOME3 DATA' }], 
              [{'some3Search':900, 'some3Data':'AAA'},{'some3Search':901, 'some3Data':'BBB'},{'some3Search':902, 'some3Data':'CCC'}], 99, \
              [{'some3Search':910, 'some3Data':'DDD'},{'some3Search':911, 'some3Data':'EEE'},{'some3Search':912, 'some3Data':'FFF'}], None),
))

def test_setForm(app, mocker, formName, formColmns, formData, objectID, formVal, valueSet): 
    with app.test_request_context():
        #mocker.patch.object(commonTool, 'cleanup_form', return_value = None)
        #form = commonTool.setForm(formName, formColmns, formData, objectID, formVal, valueSet)
        if formName in ('sForm'):
            form = commonTool.setForm(formName, formColmns, formData, objectID, formVal, valueSet)
            i = 0
            for field in form:
                assert field.name           == 'sf_0_' + formColmns[i]['name']
                assert field.data           == formVal[0][formColmns[i]['name']]
                assert field.description[1] == formColmns[i]['description'] 
                i += 1
        
        elif formName in ('__cForm'):
            i = 0
            if len(formData) == 0:
                mocker.patch.object(commonTool, 'cleanup_form', return_value = None)
                form = commonTool.setForm(formName, formColmns, formData, objectID, formVal, valueSet)
                for field in form():
                    assert field.name           == 'sf_0_' + formColmns[i]['name']
                    assert field.data           == formVal[0][formColmns[i]['name']]
                    assert field.description[1] == formColmns[i]['description'] 
            else:
                
                mocker.patch.object(commonTool, 'cleanup_form', return_value = None)
                form = commonTool.setForm(formName, formColmns, formData, objectID, formVal, valueSet)
                i = 0
                for row in form.rows:
                    j = 0
                    for field in row:
                        assert field.name           == 'rows-' + str(i) + '-sf_' + str(j) + '_' + formColmns[j]['name']
                        assert field.data._value           == formVal[i][formColmns[j]['name']]
                        assert field.description[1] == formColmns[j]['description'] 
                        j += 1
                    i += 1

                    
        elif formName in ('bForm'):                
            mocker.patch.object(commonTool, 'cleanup_form', return_value = None)
            form = commonTool.setForm(formName, formColmns, formData, objectID, formVal, valueSet)
            r = 0
            c = len(formColmns)
            for row in form.rows:
                f = 0
                for field in row:
                    assert field.name           == 'rows-' + str(r) + '-sf_' + str(f//c) + '_' + formColmns[f%c]['name']

                    f += 1
                r += 1
        


@pytest.mark.parametrize(('formName', 'formColmns', 'formData', 'objectID', 'formVal', 'valueSet', 'result'),( 
    ('filterBuild', [ 
                     {'name':'id', 'title':'□', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                     {'name':'listViewID', 'title':'List ViewID', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                     {'name':'objectFieldID', 'title':'Field Name', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                     {'name':'fieldOperator', 'title':'Field Operator', 'dataType':'text', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                     {'name':'value', 'title':'Value', 'dataType':'text', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                     {'name':'andOr', 'title':'And/Or', 'dataType':'text', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                    ], 
                    [{'id':None, 'listViewID':100, 'objectFieldID':200, 'fieldOperator':'=', 'value':'ABC', 'andOr':'and' }, \
                     {'id':None, 'listViewID':100, 'objectFieldID':201, 'fieldOperator':'>', 'value':'123', 'andOr': None }  \
                    ], 
                    99, 
                    [{'id':None, 'listViewID':100, 'objectFieldID':200, 'fieldOperator':'=', 'value':'ABC', 'andOr':'and' }, \
                     {'id':None, 'listViewID':100, 'objectFieldID':201, 'fieldOperator':'>', 'value':'123', 'andOr': None }  \
                    ], 
                    'View Name:VIEW1' , None
    ), 
    ('filterBuildSub', [ 
                     {'name':'id', 'title':'□', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                     {'name':'listViewID', 'title':'List ViewID', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                     {'name':'objectFieldID', 'title':'Field Name', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                     {'name':'seq', 'title':'Seqence', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
                      'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':0, 'isMasterObject':0,'isReadOnly':True, 'position':'', \
                      'description': ''}, 
                    ], 
                    [{'id':None, 'listViewID':100, 'objectFieldID':300, 'seq':1 }, \
                     {'id':None, 'listViewID':100, 'objectFieldID':301, 'seq':2 }  \
                    ], 
                    99, 
                    [{'id':None, 'listViewID':100, 'objectFieldID':300, 'seq':1 }, \
                     {'id':None, 'listViewID':100, 'objectFieldID':301, 'seq':2 }  \
                    ], 
                    'View Name:VIEW1',  \
                    ["{'id': None, 'listViewID': 100, 'objectFieldID': 300, 'seq': 1}", "{'id': None, 'listViewID': 100, 'objectFieldID': 301, 'seq': 2}"]),
))


def test_set_ViewForm(app, formName, formColmns, formData, objectID, formVal, valueSet, result):  
    with app.app_context():

        form = commonTool.setViewForm(formName, formColmns, formData, objectID, formVal, valueSet)

        if formName =='filterBuild':            
            for r in range(constant.VIEW_FILTER_LINES_LEN):
                if r == 0:
                    i = 0
                    for field in form():
                        if i == 0:
                            assert field.name           == 'viewName'
                            assert field.data           == valueSet
                        elif i > 0 and i < len(formColmns):
                            assert field.name            == 'sf_' + str(r) + '_' + formColmns[i - 1]['name']
                            assert field.data            == formVal[r][formColmns[i - 1]['name']]
                        i += 1
                elif r >0 :
                    i = 1
                    for field in form():
                        if i < len(formColmns) and field.name == 'sf_' + str(r) + '_' + formColmns[i - 1]['name']:
                            if r < len(formVal) + 1:
                                assert field.data       == formVal[0][formColmns[i - 1]['name']]
                            else:
                                assert field.data       == None
                        i += 1
        elif formName =='filterBuildSub':
            for field in form():
                if field.name == 'sf_999_fieldSel':
                    assert field.type == 'SelectMultipleField'
                    assert field.data == result
            

@pytest.mark.parametrize(('form', 'formColmns', 'objectID', 'default', 'result'),(
    (commonTool.bForm,
     [{'name':'id',       'title':'test_int',   'dataType':'int',      'cmbStrainObjNm': 'sex', 'foreignObjectID':0 ,
       'isBulkSearchField':1, 'isReadOnly':1, 'isVisible':0}],
      900, 1,
     (['bf_id',[('', ''), ('0', 'Male'), ('1', 'Female')]])   
     ),   
    (commonTool.pForm,
     [{'name':'id',       'title':'test_int',   'dataType':'int',      'cmbStrainObjNm': '', 'foreignObjectID':0,
       'isBulkSearchField':0, 'isReadOnly':0, 'isVisible':1},
      {'name':'appNm', 'title':'APP Name', 'dataType':'text', 'cmbStrainObjNm': '', 'foreignObjectID':11,
       'isBulkSearchField':1, 'isReadOnly':1, 'isVisible':0}],
       4, 'someApp',
     (['cf_appNm',[('','')]])   
    ),   
))

def test_setSearchField(client, form, formColmns, objectID, default, result):   
    with client:
        client.post('/dframe/auth/login/',data={'username':'testbed','password':'password', 'appSelNm':'testbed'})
        
        response = commonTool.setSearchField(form, formColmns, objectID, default)
        i = 0
        for field in response():
            if field.name           in ('rows', 'csrf_token', 'search'): 
                i += 1
            elif field.name ==  result[0]:
                assert field.choices == result[1]
                assert field.default  == default
                i += 100
            else:
                i += 1000
        assert i <= 103
        

@pytest.mark.parametrize(('form', 'r', 'formColmns',  'r_data', 'objectID', 'v_data', 'field_key'),(
    (commonTool.sForm, 88,
     [{'objectID':99,'name':'some3Search', 'title':'SOME3', 'dataType':'int', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
       'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'1st Row', \
       'isBulkSearchField':1, 'description':'SOME3 SEARCH' },
      {'objectID':99,'name':'some3Data', 'title':'SOME3DATA', 'dataType':'text', 'numOfLines':1, 'cmbStrainObjNm': '', 'foreignObjectID':0 , 'width':'10px',  \
       'height':None, 'isMultiSelect':0, 'derivedTerm':'', 'isVisible':1, 'isMasterObject':0,'isReadOnly':True, 'position':'1st Row', \
       'isBulkSearchField':0, 'description':'SOME3 DATA' }], 
      {'some3Search':900, 'some3Data':'AAA'}, 99,  {'some3Search':910, 'some3Data':'DDD'},'sf_88_'),
))

def test_setAttribute(client, form, r, formColmns, r_data, objectID, v_data, field_key):   
    with client:
        client.post('/dframe/auth/login/',data={'username':'testbed','password':'password', 'appSelNm':'testbed'})
        commonTool.cleanup_form(form)
        response = commonTool.setAttribute(form, r, formColmns, r_data, objectID, v_data)
        i = 0
        for field in response():
            if field.name   != 'csrf_token': 
                assert field.name ==  field_key + formColmns[i]['name']
                assert field.data == v_data[formColmns[i]['name']]
                assert field.description[1]  == formColmns[i]['description']
            i += 1


