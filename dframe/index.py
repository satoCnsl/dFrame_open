# 2025/01/04

from flask import  Blueprint
from flask import  redirect
from flask import session
from flask import render_template
import logging
import os
from pathlib import Path
from . import trailKeeper
from . import constant
from . import formInfoGetter
from . import commonTool

index_app = Blueprint('index', __name__)

@index_app.route('/')
def index():
    # ログレベルを DEBUG に変更
    logging.basicConfig(filename='logfile/logger.log', level=logging.DEBUG)

    trailKeeper.init_trail()
    session['searchVal']    = []                      # for data packet for searchForm.html [objectFieldID, value]
    session['appViewID']    = constant.VIEW_ID_OF_APP_PORTAL
    session['menu_bar']     = []
    if session.get('socketDb') is None or session.get('user_id') is None:
        listAppNm = formInfoGetter.exec_sql('SELECT * FROM __application ')
        commonTool.putLog('au', 'login.out', listAppNm, '')
        return render_template('auth/login.html', listAppNm = listAppNm)
    
    else:
        v = formInfoGetter.exec_sql('select portalViewID id from ' + session.get('socketDb') + '.__systemini where id=1' ,isResults=True)
        if v[0]['id'] != None:
            session['appViewID'] = v[0]['id']
        
        commonTool.putLog('ix', 'index', session.get('appViewID'), session['socketDb'])
        objectID       = constant.OBJECT_ID_OF_APP      # Portal Object for APP
        entityID       = 0                   # list form or create-data(new data entry)
        masterObjectID = 0
        runningModeID  = 0 
        #viewID         = constant.VIEW_ID_OF_APP_PORTAL
        offsetValue    = 0
        DFcpath = [objectID, entityID, masterObjectID, runningModeID, session['appViewID'], offsetValue]
        DFcpath = trailKeeper.push_trail(DFcpath)
        path = '/dframe/navi/form/' +       \
                str(objectID)       + '/' + \
                str(entityID)       + '/' + \
                str(masterObjectID) + '/' + \
                str(runningModeID)  + '/' + \
                str(session['appViewID']) + '/' + \
                str(offsetValue)  
    
    return redirect(path)

