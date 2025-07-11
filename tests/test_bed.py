import pytest
from flask import g, session, request
from datetime import date,datetime 
from dframe import commonTool, formInfoGetter, constant 

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