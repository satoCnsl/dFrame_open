import pytest
import json
from flask import template_rendered
from datetime import datetime 

from dframe import constant
from dframe import trailKeeper
from dframe import formInfoGetter
from dframe import commonTool


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


@pytest.mark.parametrize(('endpoint','actType', 'data_key_set', 'templateName'   , 'viewName', 'data','appName'   ),(
               ('/dframe/view/open/', 'A', [22,0,0,0,0,0], 'filterBuild.html', None,  None , 'View Editting'),
               ('/dframe/view/open/', 'E', [1,0,0,0,1,0],  'filterBuild.html', '設定',    None , 'View Editting'),

))
def test_viewForm(client, mocker, captured_templates, endpoint, actType, data_key_set, templateName, viewName, data, appName):
    with client:
        mocker.patch.object(trailKeeper, 'get_curr_path', return_value = data_key_set)
        mocker.patch.object(trailKeeper, 'del_viewID')
        client.post('/dframe/auth/login/',data={'username':'testbed','password':'password', 'appSelNm':'testbed'})
    
        response = client.get(endpoint + actType + '/')
            
        assert response.status_code==200
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == templateName
        assert context['appName'] == appName

        form = commonTool.sForm()
        assert form['viewName'].data == viewName
        if data:
            assert form['sf_999_fieldSel'].data == data


@pytest.mark.parametrize(('action_type', 'data_key_set_pre', 'data', 'result'),(
    ('b',  [1, 0, 0, 0, 0, 0], 
     {'viewName':'Test View' ,'filterName':'TEST','sf_0_objectFieldID': 2 ,'sf_0_fieldOperator': 'like','sf_0_value': 'post','sf_0_andOr': '', \
      'sf_1_objectFieldID': 1 ,'sf_1_fieldOperator': '>=','sf_0_value': 22,'sf_0_andOr': 'and'},
      [{'cnt':2, 'mod_at':datetime.now()}]
     ),
    ('d',  [1, 0, 0, 0, 100, 0],  
     {'viewName':'Test View' ,'filterName':'TEST','sf_0_objectFieldID': 2 ,'sf_0_fieldOperator': 'like','sf_0_value': 'post','sf_0_andOr': '', \
      'sf_1_objectFieldID': 1 ,'sf_1_fieldOperator': '>=','sf_0_value': 22,'sf_0_andOr': 'and'},
     []
     ),
))
def test_viewButton(app, client, action_type, data_key_set_pre, data, result ):
    
    def chk_line(app, objectID):
        with app.app_context():
            sql = 'select count(v.id) as cnt , max(v.modifiedAt) as mod_at \
                from dframe_testbed.__list_view_filter f join dframe_testbed.__list_view v \
                    on v.id = f.listviewID where v.objectID = ' + str(objectID) +  \
                        ' group by listViewID order by listViewID desc'
            cnt = formInfoGetter.exec_sql(sql)
            return cnt
    
    with app.app_context():
        formInfoGetter.exec_sql('DELETE FROM dframe_testbed.__list_view', isResults = False)    
        formInfoGetter.exec_sql('ALTER TABLE dframe_testbed.__list_view        AUTO_INCREMENT = 100', isResults = False)   

    with client:
        client.post('/dframe/auth/login/',data={'username':'testbed','password':'password', 'appSelNm':'testbed'})
    
        trailKeeper.push_trail(data_key_set_pre)

        client.get('dframe/view/open/A/')
        
        client.post('dframe/view/open/A',data=json.dumps(data))

        chk = chk_line(app, data_key_set_pre[constant.OBJECT_ID])         
        assert len(chk) == 0

        client.get('/dframe/view/btn/'+ action_type + '/', data=data)

        chk = chk_line(app, data_key_set_pre[constant.OBJECT_ID])

        if result != []:
            assert chk[0]['cnt'] == result[0]['cnt']
            assert chk[0]['mod_at'] < datetime.now()
            assert chk[0]['mod_at'].strftime('%Y/%m/%d %H:%M') == datetime.now().strftime('%Y/%m/%d %H:%M')
        else:
            assert chk == result