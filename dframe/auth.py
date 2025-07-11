# 2025/03/26   session['isLogActive']
# 2025/01/05
import functools
import logging

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from . import trailKeeper
from . import formInfoGetter
from . import commonTool


auth_app = Blueprint('auth', __name__)


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@auth_app.route('/dframe/auth/login/', methods=('GET', 'POST'))
def login():
    
    commonTool.putLog('au', 'login', request.method,)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        appNm   = request.form['appSelNm']
        session['socketDb'] = 'dframe_' + appNm
        session['appName'] = appNm
        commonTool.putLog('au', 'login', session.get('socketDb'), username)
        error = None
        rowDict = None
        #result = d.query(
        sql = 'SELECT id,password,isLogActive FROM dframe.__account WHERE name ="' + username + '"'
        result = formInfoGetter.exec_sql(sql)
        for row in result:
            rowDict = dict(row)    

        if rowDict is None:
            error = 'Incorrect username.'
            
        else:
            user = rowDict
        
            if not check_password_hash(user["password"], password):
                error = 'Incorrect password.'
                
            if error is None:
                session['user_id'] = user['id']
                session['isLogActive'] = user['isLogActive']
                commonTool.putLog('au', 'login.out', session['user_id'], session.get('socketDb'))
                return redirect(url_for('index.index'))
            
        commonTool.putLog('au', 'login.error', session.get('user_id'), session.get('socketDb'))
        flash(error)
    listAppNm = formInfoGetter.exec_sql('SELECT * FROM __application ')
    commonTool.putLog('au', 'login.out', listAppNm, session.get('user_id'))
    return render_template('auth/login.html', listAppNm = listAppNm)

@auth_app.before_app_request
def load_logged_in_user():
    # ログレベルを DEBUG に変更
    logging.basicConfig(filename='logfile/logger.log', level=logging.DEBUG)
    
    user_id = session.get("user_id")
    
    #--- for pytest test_navi.py     
    s = session.get('sizeOfFieldsOnPrevForm')
    if s is None:
        session['sizeOfFieldsOnPrevForm']=0
    #--- END     
   
    commonTool.putLog('au', 'load_logged_in_user', user_id, '')
    if user_id is None:
        g.user = None
        commonTool.putLog('au', 'load_logged_to_login', 'user_id is None', '')
    else:
        rowDict = None
        sql = 'SELECT name,password,isLogActive FROM dframe.__account WHERE id = ' + str(user_id) 
        result = formInfoGetter.exec_sql(sql)
        for row in result:
            rowDict = dict(row)    
        g.user = rowDict
        
        session['isLogActive'] = rowDict['isLogActive']
        commonTool.putLog('au', 'load_logged_in_user.out', session.get('socketDb'), '')
        

@auth_app.route('/logout')
def logout():
    commonTool.putLog('au', 'logout', g.user)
    trailKeeper.init_trail()
    session.clear()
    session.pop('user_id', None)
    g.user = None

    return redirect(url_for('index.index'))

