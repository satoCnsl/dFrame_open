# 2025/06/18 updaate_data_line: getFieldList(dbName --> socketDb,):
# 2025/05/29 if kindOfInfo  in ('FormData','FormDataAll', 'FormMenuBar', 'FormColumns') and cpath[constant.ENTITY_ID] != 0:
#            if sql_body[5] == '': sql_body[5] = session['socketDb']
# 2025/04/01 getObjFldVal elif where != None:
# 2025/03/25  get_table_name: (data_key_set, socket=False): ex. to update __object_security , do not attach _v
#                              getFormPivotData: offset
# 2025/02/24 exec_sql
# 2025/01/22 pivot: viewID  , getTableName
# DataSet Test
# getFormColumne/
#from tkinter import StringVar
from flask import session, jsonify, abort
import logging
import pymysql.cursors
from . import db 
from . import constant
from . import commonTool

from sqlalchemy import sql, values

def exec_sql(sql, isResults = True, out = None, commitReq=False, logOff=False ):
    if logOff == False:
        commonTool.putLog('ig', 'exec_sql' , sql + ', isResults=' + str(isResults) + ', out=' + str(out) + ', commit=' + str(commitReq))
        pass
    conn = db.get_db()
    try:        
        with conn.cursor() as d:
            results = []
            if isResults:
                if out != None:
                    sql = 'select ' + out
                    #results=d.query(sql) 
                rows = d.execute(sql)
                if rows == None:
                    return []
                
                results = d.fetchall()
            else:                
                #d.query(sql)  
                d.execute(sql)
            if commitReq:
                conn.commit()
                d.execute('select last_insert_id() as NewID')
                results = d.fetchall()
                logging.info('*IG*exec_sql.result %s', results)
    except:
        comment = '  exec_sql( ' + sql + ')'
        commonTool.putLog('ig', 'exec_sql.ERROR□□□□□□□□□□□□', comment)
        print('exec_sql.ERROR□□□□□□□□□□□□', comment)
        return jsonify({'message': comment})  
    finally:
        d.close()
        

    result = []
    i = 0
    for row in results:
        rowDict = dict(row)
        result.insert(i,rowDict)
        i += 1
    if len(result) > 0 and 'ERROR' in result[0]:
        comment = 'ERROR  exec_sql( ' + sql + ')' + rowDict
        abort(49, comment)
    
    return result


def get_table_name(data_key_set, isUpdate=False):
    commonTool.putLog('ig', 'get_table_name.data_key_set', data_key_set , isUpdate)
    dNm = session['socketDb']
    
    objID = data_key_set[constant.OBJECT_ID]
    sql = ''
    if data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING:  # to be eliminated: no cases happen 
        if objID == constant.OBJECT_ID_OF_OBJECT_FIELD :   # to be eliminated: no cases happen 
            if data_key_set[constant.MASTER_ENTITY_ID]>0:       # to be eliminated: no cases happen 
                sql = 'select distinct case when dbName = "socket" then "' + dNm + '" else dbName end dbName, o.name ' \
                    ' from ' + dNm + '.__object_v o where o.id =' + str(data_key_set[constant.MASTER_ENTITY_ID])
            elif data_key_set[constant.ENTITY_ID]>=constant.OBJECT_ID_START_FOR_APPS:
                sql = 'select distinct  dbName, name from ' + dNm + '.__object_v o where o.id =' \
                    + '(select objectID from ' + dNm + '.__object_field_v where id =' + str(data_key_set[constant.ENTITY_ID]) + ')'
                #return jsonify({'message': 'ERROR!!'})  
            else:
                sql = 'select "' + dNm + '" as dbName, "__object_field" as name'
        elif objID == constant.OBJECT_ID_OF_OBJECT :
            sql = 'select distinct o.dbName as dbName, o.name ' \
                + ' from ' + dNm + '.__object_v o  where o.id =' + str(data_key_set[constant.ENTITY_ID])
            
        else:
            sql = 'select case when dbName in ("socket", "socketObject") and "' + format(isUpdate) + '"="True" \
                then "' + dNm + '" else dbName end as dbName,' + \
                  ' case  when dbName = "socket" and "' + format(isUpdate) + '" ="False" then concat(name , "_v") else name end as name ' + \
                ' from ' + dNm + '.__object_v where id ='  + str(objID)
    else:
        sql = 'select case when dbName in ("socket", "socketObject") then "' + dNm + '" else dbName end as dbName, name '\
             ' from ' + dNm + '.__object_v where id ='  + str(objID)
    commonTool.putLog('ig', 'get_table_name.out', sql, '')
    result = exec_sql(sql)
    return result[0]

def get_table_field_name(data_key_set):
    dNm = session['socketDb']
    if data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT_FIELD:
        sql = 'select distinct name from ' + dNm + '.__object_field_v where id =' + str(data_key_set[constant.ENTITY_ID] )
        result = exec_sql(sql)
        return result[0]['name']
    
    else:
        return None

'''
def get_table_field_size(objectID):
    dNm = session['socketDb']
    sql = 'select distinct count(id) as size from ' + dNm + '.__object_field_v where objectID =' + str(objectID )
    result = exec_sql(sql)
    return result[0]['size']
'''

def get_form_info(kindOfInfo, cpath, sql_app='', isRawValue=0):
    
    sql =  get_sql(kindOfInfo, cpath, sql_app, isRawValue)
    result = exec_sql(sql)
    return result


def get_sql(kindOfInfo, cpath, sql_app='', isRawValue=0):
    sql = ''
    offset = cpath[constant.OFFSET_VALUE]
    if kindOfInfo != 'sql_app' :
        path = '"' + session['socketDb'] + '"'                              #app name
        path += ',' +  str(cpath[constant.OBJECT_ID])                       #objectID
        if kindOfInfo not in ('FormLinkage','FormPivotData'):
            path += ',' + str(session.get("user_id"))                       #accountID)                       #objectID
        if kindOfInfo in ('FormColumns','FormData','FormDataAll','FormButton'):
            path += ',' + str(cpath[constant.ENTITY_ID])                    #entityID    entityID=-1: request a new data
        if kindOfInfo  in ('FormPrpty','FormData','FormDataAll'):
            path += ',' + str(cpath[constant.MASTER_ENTITY_ID])             #masterEntityID
            if kindOfInfo != 'FormPrpty':
                if kindOfInfo == 'FormDataAll':                             #total size of Data
                    kindOfInfo = 'FormData'
                    path += ',1'                                            # to get whole data
                else:
                    path += ',0'
                path += ',' + str(isRawValue)                               # isRawValue
                path += ',' + str(offset)                                   # offset value
        if kindOfInfo == 'FormPivotData':            
                path += ',' + str(offset)                                   # offset value
        if kindOfInfo  in ('FormData','FormDataAll', 'FormColumns') and cpath[constant.ENTITY_ID] == 0 \
            or kindOfInfo  in ('FormPivotData','FormMenuBar' ) :
            path += ',' + str(cpath[constant.VIEW_ID])                      # viewID (reportID)
        
        if kindOfInfo  in ('FormData','FormDataAll', 'FormColumns') and cpath[constant.ENTITY_ID] != 0:
            path += ',' + str(0)                                            # viewID (reportID)
                
        if kindOfInfo in ('FormPrpty','FormData','FormDataAll','FormButton'):
            path += ',' + str(cpath[constant.RUNNING_MODE_ID])  
                
        sql = 'call dframe.get' +  kindOfInfo + '(' + path + ')'
    else:
        sql = sql_app
    commonTool.putLog('ig', 'get_sql.out',  cpath, sql)
    return sql
    
#to provide the combobox list Data
#slctStyle: "lookup"-combobox sourceName=list data to provied the selection list data, 
#           "view"- objectID = to provide the field name of the objectID Object
def getSelectList(srcObjID, object_id, view_id, categoryNm):
    commonTool.putLog('ig', 'getSelectList',  str(srcObjID) +',' + str(object_id) +',' + str(view_id) , categoryNm)
    
    sql = 'call dframe.getSelectList'
    sql += '("' + session.get('appName') + '",'  + str(srcObjID) + ',' + str(object_id) + ',' + str(session.get("user_id")) \
          + ',' +  str(view_id) + ',"' + categoryNm + '")'

    sList = exec_sql(sql)
    #if slctStyle == 'lookup':
    l =[]
    for row in sList:
        t = row['value'], row['title']
        l.append(t)
    commonTool.putLog('ig', 'getSelectList.out', l, t)
    return l


    
def ins_data_line( data_key_set, sql_body):
   # sql_body": 0:',fld,' 1:', val,' 2:', fld_name,' 3:', fld_dataType,' 4:', fld_isNotNull, 
   #          ' 5:', db_name,' 6:', tbl_name,' 7:', new_db_name, ' 8;',new_tbl_name)
   
    results = []
    commonTool.putLog('ig', 'ins_data_line', data_key_set, sql_body)
    # when "setting" mode , set a new object to data base schema
    if data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT and \
        data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING:
        sql = 'call setNewObj("' + session.get("appName") + '", "' + str(sql_body[0]) + '",\'' + str(sql_body[1]) + \
              '\','  +  str(sql_body[7]) + ',' + str(sql_body[8]) + ',' + str(session.get("user_id"))  +')'
        print(sql)
        commonTool.putLog('ig', 'ins_data_line.out', sql, '')
        print(sql)
        results = exec_sql(sql)
        return results[0]['NewID']

    # for object field modifing
    elif data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT_FIELD:
        if sql_body[4] == '':
            isNotNull = 0
        else:
            isNotNull = 1
        #sql = 'call setNewObjFld("' + session.get("socketDb") + '", "objectID,' + str(sql_body[0]) + '",\'' + str(object_id)  + ',' + str(sql_body[1]) +  \
        sql = 'call setNewObjFld("' + session.get("appName") + '",  "' + str(sql_body[0]) + '",\''  +  str(sql_body[1]) +  \
             '\',"'+ str(sql_body[5])  + '","' + str(sql_body[6]) + '","' + str(sql_body[2])  + '",' + str(sql_body[3]) + ',' + \
            str(isNotNull) + ',' + str(session.get("user_id"))  +')'
        results = exec_sql(sql)  
        return results[0]['NewID']
    else:        
        # to register the new data to user table(if user mode) or object table(if setting mode)
        commonTool.putLog('ig', 'ins_data_line.out.else', sql_body[0].rstrip(',') + ' : ' + sql_body[1].rstrip(',') + ' : ' +  sql_body[6], '')
        sql = 'INSERT INTO ' + str(sql_body[5]).replace('"','') + '.' + str(sql_body[6]).replace('"','')
        sql += ' (' + sql_body[0].rstrip(',') + ') VALUES (' + sql_body[1].rstrip(',') + ');'

        #d.query(sql)
        results  = exec_sql(sql, isResults=False, commitReq=True)
        sList = []
        i = 0
        
        for row in results:
            rowDict = dict(row)
            sList.insert(i,rowDict)
            i += 1
            
        commonTool.putLog('ig', 'ins_data_line.result', results, '')
        
        return results[0]['NewID']
    

def updt_data_line(data_key_set, sql_body):
    # 0:fld, 1:val,2:fld_name 3:fld_dataType, 4:fld_isNotNull, 5: db_name,
    # 6:tbl_name, 7:new_db_name, 8;new_tbl_name, 9:isModify,10:isRename
    commonTool.putLog('ig', 'updt_data_line', data_key_set, sql_body)
    fld = ''
    d = get_table_name(data_key_set)
    print(d)
    dbNm = d['dbName']   
    tblNm = d['name']    
    
    # when updating mode: (col01="val01",col02="val02",...)
    fld = sql_body[0]
    if data_key_set[constant.RUNNING_MODE_ID] != constant.RUNNING_MODE_ID_FOR_SETTING or \
       data_key_set[constant.OBJECT_ID] not in (constant.OBJECT_ID_OF_OBJECT, constant.OBJECT_ID_OF_OBJECT_FIELD ):
        sql = 'UPDATE ' + sql_body[5] + '.' + sql_body[6] + ' SET ' + fld + \
             ' WHERE id =' + str(data_key_set[constant.ENTITY_ID])
        exec_sql(sql, isResults=False, commitReq=True)
    
    else:
        if data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT:
            dbOld = session.get("appName")
            if sql_body[5] != '':
                dbOld = sql_body[5]

            if sql_body[7]!='""':
                dbNm = sql_body[7].replace('"','')
            if sql_body[9] or sql_body[10]:
                sql = 'UPDATE dframe_' + dbNm + '.__object' + ' SET ' + fld + \
                ' WHERE id =' + str(data_key_set[constant.ENTITY_ID])
                exec_sql(sql, isResults=False, commitReq=True)
            if sql_body[10]:
                sql = 'RENAME TABLE ' + dbOld + '.'+ sql_body[6] + \
                    ' TO ' + dbNm + '.' + sql_body[8].replace('"','')
                exec_sql(sql, isResults=False, commitReq=True) 
            
        if data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT_FIELD:
            sql = 'UPDATE dframe_' + sql_body[5] + '.__object_field' + ' SET ' + fld + \
                ' WHERE id =' + str(data_key_set[constant.ENTITY_ID])
            exec_sql(sql, isResults=False, commitReq=True)

            if sql_body[9] == True :     # isNotNull Data Type
                sql = 'ALTER TABLE ' + dbNm + '.'+ tblNm +' MODIFY ' 
                sql += sql_body[2].replace('"','') + ' ' + sql_body[3].replace('"','') + ' ' + sql_body[4].replace('"','') 
                exec_sql(sql, isResults=False, commitReq=True)             
            print(111,dbNm, tblNm, sql_body[2] + ' ' + sql_body[3].replace('"',''))
            if sql_body[2] > '':
                sql = 'ALTER TABLE ' + dbNm + '.'+ tblNm + ' CHANGE COLUMN ' + \
                        sql_body[2] + ' ' + sql_body[3].replace('"','')
                exec_sql(sql, isResults=False, commitReq=True) 


def delete_data_line(data_key_set):
    dfNm = session['socketDb']
    entity_id =        data_key_set[constant.ENTITY_ID]
    master_entity_id = data_key_set[constant.MASTER_ENTITY_ID]
    tNm =  get_table_name(data_key_set)['name']
    dNm =  get_table_name(data_key_set)['dbName']
    
    commonTool.putLog('ig', 'delte_data', data_key_set , dfNm)
    # if on "setting" mode , delete its field from data base schema
    if data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING:   

        if data_key_set[constant.OBJECT_ID]  == constant.OBJECT_ID_OF_OBJECT_FIELD:   
            fNm =  get_table_field_name(data_key_set)

            sql = 'show columns from ' + dNm + '.' + tNm + ' where Field="' + fNm + '"'
            #results = d.query(sql)
            results = exec_sql(sql)
            
            if len(results) > 0:
                sql = 'ALTER TABLE ' + dNm + '.' + tNm + ' DROP COLUMN ' + fNm
                exec_sql(sql, isResults=False, commitReq=True) 

            sql = 'DELETE FROM ' + dfNm + '.__object_field WHERE id = ' + str(data_key_set[constant.ENTITY_ID])
            exec_sql(sql, isResults=False, commitReq=True)
                
        elif data_key_set[constant.OBJECT_ID]  == constant.OBJECT_ID_OF_OBJECT:
            sql = 'DROP TABLE ' + dNm + '.' + tNm 
            exec_sql(sql, isResults=False, commitReq=True)

            sql = 'DELETE FROM ' + dfNm + '.__object WHERE id = ' + str(data_key_set[constant.ENTITY_ID])
            exec_sql(sql, isResults=False, commitReq=True)
        elif entity_id > 0:
            sql = 'DELETE FROM ' + dNm + '.' + tNm + ' WHERE id =' + str(entity_id)
            exec_sql(sql, isResults=False, commitReq=True)

    elif data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_VIEW_FILTER:
        #sql = 'DELETE FROM __list_view where id = ' + str(master_entity_id)
        #d.query(sql)
        sql = 'DELETE FROM ' + dNm + '.__list_view_filter where listViewID = ' + str(master_entity_id)
        exec_sql(sql, isResults=False, commitReq=True)
    elif entity_id > 0:
        sql = 'DELETE FROM ' + dNm + '.' + tNm + ' WHERE id =' + str(entity_id)
        exec_sql(sql, isResults=False, commitReq=True)
    

def get_app_name(app_id):
    if app_id > 0:
        dNm = session['socketDb']
        
        # "app" is not supported on the preliminary version 
        sql = 'select IFNULL(dic.toString ,o.title) as Title from ' + dNm + '.__object_v o  left join \
        ( select toString, ordinaryWord from dframe.__caption_dic cd inner join ' + dNm + '.__systemini  si \
            on si.language = cd.language) dic \
         on o.title = dic.ordinaryWord where id = ' + str(app_id) + ' limit 1'
        #result = d.query(sql)
        result = exec_sql(sql)
        rowDict = []
        name = []
        for row in result:
            rowDict = dict(row) 
            name.insert(0,rowDict['Title']) 
        return name[0]


def getObjFldVal(tableNm, id, fldNm, where = None):
    dNm = session['socketDb']
    sql = 'select ' + fldNm + ' as name from ' + dNm + '.'   
    if id > 0:
        sql += tableNm + ' where id =' + str(id) 
    elif where != None:
        sql += tableNm + ' where ' + where

    #results=d.query(sql)
    results = exec_sql(sql)
    selList = []
    i = 0
    for row in results:
        #rowDict = dict(row)
        #selList.insert(i,rowDict['name'])
        selList.append(dict(row)['name'])
        i += 1
    if len(selList) == 1:
        return selList[0]
    elif len(selList) > 1:
        return selList
    else:
        return ''
    

def getListViewName(data_key_set):
    dNm = session['socketDb']
    objectID = data_key_set[constant.OBJECT_ID]
    sql0 = 'select 0 as seq, 0 as id, "" as name, 0 as isSystemUse '
    sql1 = 'select seq, id, name, isSystemUse  from ' + dNm + '.__list_view_v where objectID=' + str(objectID)

    if objectID in [constant.OBJECT_ID_OF_OBJECT, constant.OBJECT_ID_OF_OBJECT_FIELD]:  
        sql = sql1
    else:
        sql = sql0 + ' UNION ' + sql1 

    if data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING :        
        sql += ' and isSystemUse = 1 ORDER BY seq '
    else:
        sql += ' and isSystemUse = 0 ORDER BY seq '

    #results=d.query(sql)
    results = exec_sql(sql)
    selList = []

    i = 0
    for row in results:
        rowDict = dict(row)
        selList.insert(i,rowDict)
        i += 1

    commonTool.putLog('ig', 'getListViewName.resutl', selList, data_key_set)
      
    return selList


def getFieldList(socketDb, user_id, objectID, viewID):
    #results:[[id:val1, caption:cap1], [id:val2, caption:cap2], .... ,[]
    sql = 'call getFieldList("' + socketDb +  '" ,' + str(user_id) + ','+ str(objectID) + ','+ str(viewID) +')'
    results= exec_sql(sql)
    fld_id = []

    i = 0
    for row in results:
        rowDict = dict(row)
        fld_id.insert(i,rowDict)
        i += 1

    l =[]
    for row in fld_id:
        t = str(row['id']), row['title']
        l.append(t)
        
    commonTool.putLog('ig', 'getFiledList.resutl', l, objectID)
    return l



'''
def deleteData(dataTableNm, id):
    
    sql = 'DELETE FROM '
    sql += dataTableNm + ' WHERE id =' + str(id)
    exec_sql(sql, isResults=False, commitReq=True)
def chk_exe_trigger(type, object_id):
    dNm = session['socketDb']
    q = 'select sqls from ' + dNm + '.__trigger_v where objectID =' + str(object_id) + ' and type = "' + type + '"'
    #trgr = exec_sql(q)
    trgr = exec_sql(sql)
    
    if len(trgr) > 0:
        #execDb(trgr[0]['sqls'])
        exec_sql(sql, isResults=False)
        return 'done'
    return 'pass'
'''

def getFieldCaption(isSystemUse, fieldName = ''):
    dNm = session['socketDb']
    q = 'call getFieldCaption("' + dNm + '", '+ str(isSystemUse) + ', "' + fieldName + '")'
    d = exec_sql(q)
    
    if isSystemUse:
        return d[0]
    else:
        return d[0][fieldName]
    

def getDicDescription( msg_id):
    q = 'call getDicDescription(' + str(msg_id) + ')'
    d = exec_sql(q)
    return d[0]['description']

