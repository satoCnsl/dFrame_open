# 2024/11/14
"""
The flask application package.
"""
import os
from datetime import timedelta
from flask import Flask
from flask import session


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='66c5b3e0541065728d4edc77cf5e6a9504faf9b3cb77d2d4150fa98b7395a072',
    #    DATABASE=os.path.join(app.instance_path, 'dframe.sqlite'),
    )
    
    #session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=420)
    #session.modified = True

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
        
    from . import auth
    app.register_blueprint(auth.auth_app)

    from . import index
    app.register_blueprint(index.index_app)

    from . import navi
    app.register_blueprint(navi.navi_app)

    #from . import search
    #app.register_blueprint(search.search_app)
    
    from . import viewEdit
    app.register_blueprint(viewEdit.viewEdit_app)
    
    from . import genPDF
    app.register_blueprint(genPDF.genPDF_app)
 


    return app