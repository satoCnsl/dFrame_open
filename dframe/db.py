# 2025/01/03
import dataset
#from mysql.connector 
#import pandas as pd

import click
import os
from pathlib import Path
import pymysql.cursors
from flask import session
from flask import  Blueprint
from flask import current_app, g
from flask import Flask, render_template, url_for, request, redirect
from flask.cli import with_appcontext
from . import constant
from . import commonTool


db_app = Blueprint('db', __name__)

def get_db():    
    if 'db' not in g:
        g.db = pymysql.connect(host=constant.DB_HOST, user=constant.DB_USER,port=constant.DB_PORT, \
                        passwd=constant.DB_PASS, db='dframe', charset=constant.DB_CHARSET, \
                        cursorclass=pymysql.cursors.DictCursor)
        if 'user' in g:      # to avoid issue putLog in commonTool when test mode
            commonTool.putLog('db', 'get_db' , "g.db!=None", session.get('socketDb'))
    return g.db
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(sqlfile):
    d = get_db()
    d.query(sqlfile)
    #commonTool.putLog('db', 'init_db' , sqlfile, session.get('socketDb'))

@click.command("init-db")
def init_db_command():
    click.echo('Initialized the database.')
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
    """Clear the existing data and create new tables."""
    #init_db('schema.sql')
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
