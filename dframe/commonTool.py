# 2025/05/20   compile_sql elif c['name'] not in ('id', 'dbName', 'dummy_field') and c['value'] not in (None, 'NULL') :
#                        --> elif c['name'] not in ('id', 'dbName', 'dummy_field') , password validators=nn :
#                           eliminate:isModigy, isRename
#              setAttribute:if c['derivedTerm'] > '':  # and c['isReadOnly'] == 1:  , if c['isReadOnly'] or c['derivedTerm'] > '': 
# 2025/04/02   length --> dataLength  updateFilter:if objectID < constant.OBJECT_ID_START_FOR_APPS: isSystemUse = 1
# 2025/01/15   2025/02/02 2025/02/04 dfV = formInfoGetter.exec_sql('SELECT IFNULL(defaultViewID,0) dv FROM ' + session.get('socketDb')
import math
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from flask_wtf import FlaskForm
from wtforms import  Form, StringField, PasswordField, SubmitField, DateField, DateTimeLocalField, BooleanField
from wtforms import EmailField, RadioField, SelectField, IntegerField, DecimalField, TextAreaField, SelectMultipleField, FieldList, FormField
from wtforms.validators import InputRequired
from wtforms import widgets 
from datetime import date,datetime 
from . import constant
from . import formInfoGetter
import logging
from flask import g

class sForm(Form):
    pass

class bForm(FlaskForm):
    search = FieldList(FormField(sForm))
    rows = FieldList(FormField(sForm))

class pForm(Form):
    search = FieldList(FormField(sForm))
    rows = FieldList(FormField(sForm))
    
def putLog(modulNm, defNm, desc, value = 'None'): 
    if 'user' in g:            # for pytest not to issue logging nor print
        if session.get('isLogActive'):
            logging.info( str(session.get("user_id")) + '**' + modulNm + '.' + defNm + '=' + '= %s value= %s' % (desc , value))
        else:
            print(str(session.get("user_id")) + '**' + modulNm + '.' + defNm + ':' + ': %s value %s' % (desc , value))

def set_formparam(data_key_set):
    
    formPrpty=    formInfoGetter.get_form_info('FormPrpty',data_key_set)
    if formPrpty[0]['masterObjectID'] > 0 and formPrpty[0]['bulkSourceObjectID'] > 0:
        formColumns = formInfoGetter.get_form_info('FormColumnsPivot',data_key_set)
        formData = formInfoGetter.get_form_info('FormPivotData',data_key_set)
        formVal  = formInfoGetter.get_form_info('FormPivotData',data_key_set)
        dd_link  = []
        fk_link  = []
    else:
        formColumns = formInfoGetter.get_form_info('FormColumns',data_key_set)
        formData=     formInfoGetter.get_form_info('FormData',data_key_set)      
        formVal  =    formInfoGetter.get_form_info('FormData',data_key_set, isRawValue=True)       
        dd_link=      formInfoGetter.get_form_info('FormLinkage',data_key_set)
        fk_link =     set_fk_link(data_key_set,formVal,formColumns)  
    formButton=   formInfoGetter.get_form_info('FormButton',data_key_set)  
    formMenuBar=  formInfoGetter.get_form_info('FormMenuBar',data_key_set)    
    #       0         1           2        3          4       5       6      7
    return formPrpty,formColumns,formData,formVal,dd_link,fk_link,formButton,formMenuBar


def set_fk_link(data_key_set,formVal,formColumns):
    if len(formVal) > 0 and len(formColumns) > 0:
        putLog('cm', 'set_fk_link.formVal:', formVal[0], '')
        putLog('cm', 'set_fk_link.formCol:', formColumns[0], '')
    #link information for list form
    fk_link = []       #[row1,...,rowN] rowN:{ col0(id), col1(name), ....]
    #ddObjID = formPrpty[0]['drillDownObjectID']
    #dFldNm = formPrpty[0]['drillDownFieldNm']
    for i in range(len(formVal)) :
        linkRow = {}
        df = 0      #default ViewID in __object.defaultViewID
        for c in formColumns :
            col = {}
            col['runningModeID'] = data_key_set[constant.RUNNING_MODE_ID]
            fNm = c['name']
            fobjID = c['foreignObjectID']
            if fNm == 'id':    
                # for drill down form ex. view summary form (like inventory) to another view for detail recieve/ship data         
                if fobjID > 0:         #  inventory only  temporaly solutiion!!
                    col['objectID']      = fobjID
                    col['entityID']      = 0
                    col['masterObjID']   = 0
                    col['viewID'] = 100000  + int(formVal[i]['id'])
                    col['caption'] = formInfoGetter.getFieldCaption(False, 'Detail')
                    col['offset'] = 0
                else:
                    # application :for detail single form (ex. to select a entity to display on a sigle form
                    #    ex. __post entity list to __post single data)
                    
                    dfV = []
                    if formVal[i]['id'] is not None:
                        dfV = formInfoGetter.exec_sql('SELECT IFNULL(defaultViewID,0) dv FROM ' + session.get('socketDb') + '.__object_v ' \
                                                ' WHERE id= ' + str(data_key_set[constant.OBJECT_ID]))
                    if len(dfV) > 0:
                        df = dfV[0]['dv']
                    # link to upper object when the data is a record-type-object 
                    #    (class diary -  infant class, baby class, saturdya claww)
                    recType = []
                    col['offset'] = 0
                    if data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT and \
                    data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_USER:
                        if formVal[i]["id"] > 0:
                            recType = formInfoGetter.exec_sql('call getRecTypeInfo(' + str(formVal[i]["id"]) + ', 0, 0)')
                            eid = 0
                    if recType == [] and data_key_set[constant.VIEW_ID] > 0:
                        recType = formInfoGetter.exec_sql('call getRecTypeInfo( 0,' + \
                                        str(data_key_set[constant.OBJECT_ID]) + ',' + str(data_key_set[constant.VIEW_ID ]) + ')')
                        eid = formVal[i]["id"]
                    
                    if len(recType)> 0 :
                        col['objectID'] = recType[0]['upperObjectID']
                        col['viewID']   = recType[0]['viewID']
                        col['entityID']  = eid
                        col['masterObjID']   = 0
                        col['caption'] = formInfoGetter.getFieldCaption(False, 'Open')

                    # setting portal: app object entity (single form: app object property ) 
                    #    ex. post object --> object single form for "post"
                    #   application portal for RECORD TYPE Object
                    #       put view_field on link data                 
                    
                    elif data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT and \
                    data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING and \
                    formVal[i]['runningType']==constant.RUNNING_TYPE_ID_FOR_USER or \
                    data_key_set[constant.OBJECT_ID] != constant.OBJECT_ID_OF_OBJECT :
                        col['objectID']  = data_key_set[constant.OBJECT_ID]
                        col['entityID']  = formVal[i]['id']
                        
                        if data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT:
                            col['caption'] = formInfoGetter.getFieldCaption(False, 'Setting')
                        else:
                            col['caption'] = formInfoGetter.getFieldCaption(False, 'Detail')
                        col['viewID'] = df

                    # setting portal: __account List, __role List
                    # application portal: app object List 
                    else:
                        col['objectID']  = formVal[i]['id']
                        col['entityID']  = 0
                        col['viewID'] = df
                        if formVal[i]['runningType']==constant.RUNNING_TYPE_ID_FOR_CUSTOMIZING:
                            col['caption'] = formInfoGetter.getFieldCaption(False, 'Customizing')
                        else:
                            col['caption'] = formInfoGetter.getFieldCaption(False, 'Open')
                col['masterObjID']   = 0
                putLog('cm', 'set_fk_link.1' , col, '')

            # to link to foreign object set  (foreingn object)
            #  ex. __post to __account   List to foreign object entity 
            elif fobjID != 0 and c['isMultiSelect'] == False : 
                col['objectID']      = fobjID
                col['entityID']      = formVal[i][fNm]
                col['masterObjID']   = 0
                col['viewID'] = df
                col['offset'] = 0
                putLog('cm', 'set_fk_link.4' , col, '')

            else:
                col['objectID']      = 0

            linkRow[fNm] = col
            
        putLog('cm', 'set_fk_link.out:', linkRow, '')
        fk_link.append(linkRow)
    return fk_link


def set_url(DFcpath):
    # url path of the current form 
    urlPath = ''
    for p in DFcpath:
        urlPath += '/'
        if type(p) is int :
            urlPath += str( p ) 
        elif type(p) is str:
            urlPath += p 
        else:
            urlPath += "%27%27"
    return urlPath + '/'


def lap_field(dataType, value, isViaForm=True):
    fld = 'NULL'
    
    putLog('cm', 'lap_field', dataType + ':' + str(value) , isViaForm)
    if value == None or value == "":              
        if dataType in ('int','tinyint'):
            fld = '0'
        #else:
        #    fld = 'NULL'
    #elif value[0:9] == 'curdate()' \
    elif dataType in ('date', 'datetime') and isViaForm :  #2024/3/26 bForm date babyDailyRec_v.date
            fld = '"' + value  + '"' 
            if len(fld) == 0:
                fld = 'NULL'
    elif dataType in ('text'): 
        if value != None: 
            fld = '"' + value  + '"' 
        else:
            fld = 'NULL'  
    
    elif dataType in ('date') and isViaForm == False :
        fld = '"' + (datetime.strftime(value, "%Y/%m/%d"))  + '"'  
    elif dataType in ('datetime') and isViaForm == False :
        fld = '"' + (datetime.strftime(value, "%Y/%m/%d %H:%M:%S"))  + '"'       

    elif dataType in ('password'):
        fld = '"' + generate_password_hash(value) + '"'
    else:
        fld =  str(value)
        
    putLog('cm', 'lap_field.out', fld, '')
    return fld


# build a SQL phrase like ' field-name = data ' for update operation, 
#                         ' field-name1, field-name2... and field-data1, field-data2... for insert operation
# note: data to be presented as int, text, datetime etc
def build_update_field_terms(isUpdate, colNm, data, dtType):
    putLog('cm', 'build_update_field', isUpdate, colNm  + ':' + str(data) + ':' + dtType)
    if data == '"None"':
        data = "NULL" 
    if isUpdate == True:   # if update operation , formurate (col-name = input value)
        #body = colNm + '=' + lap_field(dtType, data, isViaForm=True) + ',' 
        body = colNm + '=' + str(data) + ',' 
        putLog('cm', 'build_update_field.update', body, '')
        return body, None
    # if create data, formurate field-name-string and input value string
    else: 
        if data != None:
            fld = colNm + ','      
            #data = lap_field(dtType,data, isViaForm=True)+ ','      # for date/datetime already to be of String Type      
            data = str(data) + ','
        else:
            fld = ''
            data = ''
        putLog('cm', 'build_update_field.notUpdate', data, '')
        return fld,data


def updateFilter(DFcpath, viewNm, filterSpec, accountID):
    #prePath = trailKeeper.get_curr_path()
    #objectID = prePath[constant.OBJECT_ID] 
    #viewID   = prePath[constant.VIEW_ID]
    objectID = DFcpath[constant.OBJECT_ID] 
    viewID   = DFcpath[constant.VIEW_ID]
    putLog('cm', 'updateFilter', viewNm, filterSpec) 
    if viewID > 0:
        #update the __list_view table
        sql_body = [('name="' + viewNm + '",objectID=' + str(objectID)),'','','','',session['socketDb'],'__list_View']
        formInfoGetter.updt_data_line([constant.OBJECT_ID_OF_VIEW,viewID,0,0,0],sql_body)
        #delete the whole __list_view_field
        formInfoGetter.delete_data_line([constant.OBJECT_ID_OF_VIEW_FILTER,0,viewID,0,0,0])
    
    else:
        # insert list_view table
        fieldNm = 'name,objectID,isSystemUse,modifiedBy,modifiedAt'
        isSystemUse = 0
        if objectID < constant.OBJECT_ID_START_FOR_APPS:
            isSystemUse = 1
        dataValue = '"' + viewNm + '",' + str(objectID) + ',' + str(isSystemUse) + ',' + str(accountID)
        dataValue += ', CURRENT_TIMESTAMP'
        viewID = formInfoGetter.ins_data_line([constant.OBJECT_ID_OF_VIEW,0,0,0,0,0], \
                    [fieldNm, dataValue,None,None,None, session.get('socketDb'),constant.OBJECT_NAME_OF_VIEW])
        
    putLog('cm', 'updateFilter.viewID', viewID, viewNm)
    # insert list_view_filter table
    # ['_id', '_objectFieldID', '_fieldOperator', '_value', '_andOr']
    filterFieldNm = 'listViewID,objectFieldID,fieldOperator,value,andOr'
    
    #fieldDataType = ['','"','"','"']  #int or string
    fieldDataType = ['','','','']  #int or string
    # filterSpec: [[list_view_filter line_no],[id,objectFieldID,fieldOp,value,andOr]]
    for s in range(len(filterSpec)):
        if filterSpec[s][0] > str(0) :    
            dataValue = str(viewID) 
            for d in range(len(fieldDataType)):     
                    if filterSpec[s][d] != None and filterSpec[s][d] > '':
                        dataValue += ',' + fieldDataType[d] + filterSpec[s][d] + fieldDataType[d]
                    else:
                        dataValue += ',' + fieldDataType[d] + 'NULL'+ fieldDataType[d] 
            formInfoGetter.ins_data_line([constant.OBJECT_ID_OF_VIEW_FILTER ,0,0,0,0], \
                                        [filterFieldNm, dataValue,None,None,None, session.get('socketDb'),constant.OBJECT_NAME_OF_VIEW_FILTER])

    return viewID
 
def setViewCol(colList, viewID):
    dNm = session['socketDb']
    formInfoGetter.exec_sql('DELETE FROM ' + dNm + '.__list_view_field WHERE listViewID =' + str(viewID), isResults=False, commitReq=True) 
    fString = ''
    #filterID = 0
    for i in range(len(colList)):
        fString += colList[i] + ","
    if len(fString) > 0:    
        fieldNmSql = ' SELECT ' + str(viewID) + ',f.id FROM ' + dNm+ '.__object_field_v f '
        fieldNmSql += '  WHERE f.id IN (' + fString[:-1] + ')'
        formInfoGetter.exec_sql('INSERT INTO ' + dNm+ '.__list_view_field (listViewID,objectFieldID)' + fieldNmSql, \
                                isResults=False, commitReq=True)

def setPageButton(DFcpath, lineNumPerPage, len_pivotForm):
    volOfLines=0
    offsetValue = DFcpath[constant.OFFSET_VALUE]
    pageBtnOnOff = ['', '', '', '']     # html: 'disabled' vs ''
    pageOffset = [0,0,0,0]
    if len_pivotForm == 0:
        formData = formInfoGetter.get_form_info('FormDataAll', DFcpath,'', isRawValue=0) #offset=0: whole lines
        volOfLines = len(formData)
    else:
        volOfLines = len_pivotForm
    volOfPages = math.ceil(volOfLines / lineNumPerPage) 
    pageOffset = [0,                                     # top page
                max(0,offsetValue - lineNumPerPage),     # prev page
                min(offsetValue + lineNumPerPage,(volOfPages -1 ) * lineNumPerPage), # next page
                (volOfPages -1 ) * lineNumPerPage]       # last page
    if offsetValue < lineNumPerPage:
        pageBtnOnOff[0] = 'disabled'
        pageBtnOnOff[1] = 'disabled'
    if offsetValue >= (volOfPages-1) * lineNumPerPage:
        pageBtnOnOff[2] = 'disabled'
        pageBtnOnOff[3] = 'disabled'
        
    return [pageOffset, pageBtnOnOff]



def compile_sql(data_key_set, form_column_with_value):
    putLog('cm', 'compile_sql', data_key_set)
    
    if data_key_set[constant.ENTITY_ID] > 0:
        is_update = True
    else:
        is_update = False

    fld = ''            # 0 when updating mode: (col01="val01",col02="val02",...)
                        #   when creating mode: (col01,col02...)
    val = ''            # 1 when creating mode: (val01,val02,...)
    fld_name = ''       # 2 when field_setting mode:  colxx(old field name to be modified) to new colxx(new field name)
    fld_dataType = ''   # 3 when field_setting mode:  data type ('int', 'text', 'datetime',...) 
    fld_isNotNull = ''  # 4 when field_setting mode:  not null attribute
    db_name = ''        # 5 when  field_setting/object_setting mode mode: database name
    tbl_name = ''       # 6 when  field_setting/object_setting mode mode: table name 
    new_db_name ='""'   # 7 when  field_setting/object_setting mode mode: database name (default:"")
    new_tbl_name = ''   # 8 when  field_setting/object_setting mode mode: table name
    isModify    = False # when field_setting mode: modify  "data type" "IS NOT NULL" option
    isRename    = False
    for c in form_column_with_value:
        putLog('cm', 'compile_sql.col:',  c['name'], c['value'])
        if c['value'] != None and (c['derivedTerm'] in ('', None) or c['cmbStrainObjNm'] > '' or c['foreignObjectID'] > 0):
            # to set "field name" list and "value" list to "fld" and "data" respectively 
            # for child entity to set foreign key value when on user running mode
            if c['isMasterObject'] == 1 and data_key_set[constant.MASTER_ENTITY_ID]>0 and is_update == False :
                fld += c['name'] + ','
                val += str(data_key_set[constant.MASTER_ENTITY_ID]) + ','
               
            # for ordinary field
            elif c['name'] not in ('id', 'dbName', 'dummy_field', 'modifiedAt', 'createdAt') :
                result = build_update_field_terms(is_update, c['name'], c['value'], c['dataType'])
                fld += result[0] 
                if is_update == False:
                    val +=  str(result[1]) 
                    
            # when setting mode, to alter the table schema as well as modifing __object_field table data
            if data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT_FIELD :
                if c['name'] in ('objectID', 'name','dataType', 'dataLength','isNotNull'):
                    if c['name'] == 'name' :
                        fld_name = c['value'].replace('"', '')
                        if is_update == True and c['value_old'] != c['value'].replace('"', ''):
                            isRename = True
                            fld_name = c['value_old'] + ' ' + c['value'].replace('"', '') + ' '
                    if c['name'] == 'dataType':
                        if c['value_old'] != c['value'].replace('"', ''):
                            isModify = True
                            fld_dataType = c['value']
                        else:
                            fld_dataType = c['value']
                    if c['name'] == 'dataLength' and fld_dataType.replace('"', '') in ('char', 'vachar', 'MBLO', 'text'):
                        fld_dataType = fld_dataType.replace('"', '') 
                        if int(c['value']) > 0:
                            fld_dataType += '(' + c['value'] + ')'
                        else:                            
                            fld_dataType += '(100)'
                        fld_dataType = '"' + fld_dataType + '"'
                    if c['name'] == 'isNotNull':
                        if str(c['value_old']) != c['value']:
                            isModify = True
                            if c['value'] == '1':
                                fld_isNotNull = ' NOT NULL '
                            else:
                                fld_isNotNull = ''

            elif (data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT and \
                data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING ):
                if c['name'] == 'name':
                    tbl_name     = c['value_old'] 
                    new_tbl_name = c['value']
                    if is_update == True and c['value_old'] != c['value'].replace('"', ''):
                        isRename = True
                elif c['name'] == 'dbName': #and is_update == False:
                    db_name     = c['value_old']
                    new_db_name = c['value'] 
                    
    if data_key_set[constant.OBJECT_ID] != constant.OBJECT_ID_OF_OBJECT:
            t        = formInfoGetter.get_table_name(data_key_set, (data_key_set[constant.ENTITY_ID] != 0))
            if t != None:
                tbl_name = t['name']                    
                db_name  = t['dbName']
    putLog('cm', 'compile_sql.out:', \
          ' 0:' + fld + ' 1:' + val + ' 2:' + fld_name +' 3:' + fld_dataType + ' 4:' + fld_isNotNull + \
          ' 5:' + db_name  + ' 6:' + tbl_name + ' 7:' + new_db_name + ' 8:' + new_tbl_name +  \
          ' 9:' + str(isModify) + ' 10:' + str(isRename), '') 
        
    fld =  fld.rstrip(',')
    val =  val.rstrip(',')
    #        0    1    2        2            4              5         6         7          8             
    return fld, val, fld_name, fld_dataType, fld_isNotNull, db_name, tbl_name, new_db_name, new_tbl_name, \
        isModify, isRename
    #     9          10  


def setForm(formName, formColmns, formData, objectID, formVal = None, valueSet = None):
    putLog('cm', 'setForm', formName, '')
    
    if formName in (constant.SINGLE_FORM_NAME):        
        form = sForm   
        cleanup_form(form)
        setAttribute(form, 0, formColmns, formData[0], objectID, formVal[0], valueSet)
        return form()
    
    elif formName in (constant.COMP_FORM_NAME) :
        #form = sForm
        if len(formData) == 0:   # to set the search Field ? 
            form = bForm
            cleanup_form(form)
            setSearchField(form, formColmns, objectID)
            return form()
        else:                         
            form = sForm   
            cleanup_form(form)
            form = setAttribute(form, 0, formColmns, formData[0], objectID, formVal[0], valueSet)
            bulkForm = bForm()   #bForm()   2025/05/21
            bulkForm.rows.append_entry(form())   
            return bulkForm

    #if formName in (constant.BULK_FORM_NAME, constant.VIEW_EDIT_FORM_NAME ) and classNm == None:
    elif formName in (constant.BULK_FORM_NAME): 
        cleanup_form(bForm)
        setSearchField(bForm, formColmns, objectID)
        bulkForm = bForm() 
        form = sForm        

        # set data fields on single form as well as single data line on bulk form
        numOfLines = len(formData)
        #if formName == constant.VIEW_EDIT_FORM_NAME:
        #    numOfLines =  max(numOfLines, constant.VIEW_FILTER_LINES_LEN)

        for r in range(numOfLines):        
            cleanup_form(form)
            r_data = []
            v_data = []
            if r < len(formData):
                r_data = formData[r]
                if formVal != None:
                    v_data = formVal[r]
            else:
                r_data = None
                v_data = None
            form = setAttribute(form, r, formColmns, r_data, objectID, v_data, valueSet)
            bulkForm.rows.append_entry(form()) 
        return bulkForm



def setViewForm(formName, formColmns, formData, objectID, formVal, valueSet=None):
    form = sForm      
    if formName == constant.VIEW_EDIT_FORM_NAME:
        cleanup_form(form)
        key = 'viewName'
        setattr(sForm, key, StringField(id='viewName',label='View Name:', default=valueSet, validators=[InputRequired("")] ))    
        
        itelNo = constant.VIEW_FILTER_LINES_LEN
        for r in range(itelNo):        
            if r < len(formData):
                form = setAttribute(form, r, formColmns, formData[r], objectID, formVal[r])
            else:
                form = setAttribute(form, r, formColmns, None, objectID, None)

    elif formName == constant.VIEW_EDIT_SUBFORM_NAME:
        #form = setAttribute(form, 999, formColmns, None, objectID, formVal, valueSet)
        setattr(form, 'sf_999_fieldSel', SelectMultipleField('Field Selection',choices=valueSet, 
                         coerce=str,option_widget=widgets.CheckboxInput(),default=formVal, validate_choice=True))
                
    return form

def setSearchField(form, formColmns, objectID, default = None):    
    putLog('cm', 'setSearchField', formColmns[0])
    cleanup_form(form)   
    for c in formColmns:
        if c['isBulkSearchField']==1 and c['isReadOnly']==1 and c['isVisible'] == 0 :
            
            name,        Title,       dataType,   cmbStrainObjNm  ,    foObjID = \
            c['name'] ,c['title'], c['dataType'], c['cmbStrainObjNm'], c['foreignObjectID']

            if form == bForm:
                key = 'bf_' + name
            else:
                key = 'cf_' + name

            selList = []
            if len(cmbStrainObjNm) > 0:       
                selList = formInfoGetter.getSelectList(constant.OBJECT_ID_OF_BASE_VALUE,objectID,0,cmbStrainObjNm)
                
            elif foObjID > 0:
                sDb = session.get('socketDb')
                selList = formInfoGetter.getSelectList(foObjID,objectID,0,'')
                
            
            if dataType in ("text", "int", "boolean"):
                if len(selList) > 0 :
                    setattr(form, key, SelectField(Title,choices=selList, default = default))
            
            elif dataType == "date":
                    #setattr(form, key, DateField(Title,format='%Y-%m-%d', default=date.today()))
                    setattr(form, key, DateField(Title,format='%Y-%m-%d', default=default))
            elif dataType == "datetime":                 
                    #setattr(form, key, DateTimeLocalField(Title,format='%H:%M',default=default ))                 
                    setattr(form, key, DateTimeLocalField(Title,format='%Y-%m-%dT%H:%M',default=default ))
                    
            putLog('cm', 'setSearchField.col', c['name'] + key)
            putLog('cm', 'setSearchField.selList', selList)
    return form    


def setAttribute(form, r, formColmns, r_data, objectID, v_data, valueSet = None):   
    putLog('cm', 'setAttribute.start', formColmns[0]) 
    putLog('cm', 'setAttribute.data', r_data)
    for c in formColmns:
        if c['isVisible'] :
            name,        Title,       dataType,      numOfLines,     cmbStrainObjNm  ,    foObjID, \
            width,       height,      isMultiSelect = \
            c['name']  ,c['title'],  c['dataType'], c['numOfLines'], c['cmbStrainObjNm'], c['foreignObjectID'], \
            c['width'] ,c['height'], c['isMultiSelect']
            
            key =  'sf_' + str(r) + '_' + name
            rd = {}
            nn = []
            
            if c['isReadOnly'] or (c['derivedTerm'] > '' and cmbStrainObjNm in ('', None) and foObjID == 0):
                rd['disabled'] = ''
            elif c['isNotNull'] :
                nn = [InputRequired("")]
            
            if numOfLines >1:
                rd['class'] = 'form-control'
                rd['rows']  = numOfLines
                rd['cols']  = constant.TEXT_AREA_WIDTH
                rd['style']  =  "width:" + width + "; height:" + height + "; text-align:left"
            
            elif dataType in ('text', 'char', 'varchar'):
                rd['style']  =  "width:" + width +  "; text-align:left"
            elif dataType in ('int', 'decimal', 'double'):
                rd['style']  =  "width:" + width +  "; text-align:right"
            else:    
                rd['style']  =  "width:" + width +  "; text-align:center"
                
            if r_data != None:
                if c['derivedTerm'] > '' and cmbStrainObjNm in ('', None) and foObjID in ('', None):  # and c['isReadOnly'] == 1 :
                    value = r_data[name] 
                else:
                    value = v_data[name]
            else:
                value = ''

            description = [c['position'],c['description']]

            #if slctStyle == 'lookup':        
            if len(cmbStrainObjNm) > 0:   
                #selList = formInfoGetter.getSelectList('lookup',dbName,cmbObjID,objectID,0,cmbStrainObjNm)
                selList = formInfoGetter.getSelectList(constant.OBJECT_ID_OF_BASE_VALUE,objectID,0,cmbStrainObjNm)
                putLog('cm', 'setAttribute.selList:', selList)
            #elif slctStyle == 'searchButton':
            elif foObjID > 0:
                selList = formInfoGetter.getSelectList(foObjID,objectID,0,'')
                
            if dataType in ["text", "int", "float", "double"] or len(cmbStrainObjNm) > 0 \
                or dataType.startswith(("char", "varchar", "BLOB") ):
                if (len(cmbStrainObjNm) > 0 or foObjID > 0) and isMultiSelect == False:
                    if c['isReadOnly'] == 0:
                        setattr(form, key, SelectField(Title,choices=selList,default=value,description=description,  validators=nn))
                    else:
                        setattr(form, key, StringField(id=name,label=Title, default=value, description=description, render_kw=rd, validators=nn ))
                elif (len(cmbStrainObjNm) > 0 or foObjID > 0) and isMultiSelect and c['isReadOnly'] == 0:            
                    dftList = []
                    if value != None:
                        dftList = value.split(",")
                    setattr(form, key, SelectMultipleField(Title,choices=selList,coerce=str,option_widget=None,default=dftList, \
                                                           description=description, validators=nn ))
                elif numOfLines > 1:
                    setattr(form, key, TextAreaField(Title,default=value,render_kw=rd,description=description,  validators=nn ))
                elif dataType == "int" and c['isReadOnly'] == 0:
                    setattr(form, key, IntegerField(Title,default=value,description=description, render_kw=rd, validators=nn ))
                else:
                    setattr(form, key, StringField(id=name,label=Title, default=value, description=description, render_kw=rd, validators=nn ))
            elif dataType in ( "tinyint", "boolean"):
                setattr(form, key, BooleanField(Title,default=value,description=description,  validators=nn))
                
            elif dataType in ("decimal","decimal(10,1)","decimal(10,2)","decimal(10,3)"):
                if value == '':
                    value = 0
            
                if dataType == "decimal":
                    plc = 0
                elif dataType == "decimal(10,1)":
                    plc = 1
                elif dataType == "decimal(10,2)":
                    plc = 2
                else:
                    plc = 3
                setattr(form, key, DecimalField(Title,default=value,places = plc,description=description, render_kw=rd, validators=nn ))
            elif dataType == "date":
                setattr(form, key, DateField(Title,default=value,format='%Y-%m-%d',description=description, render_kw=rd, validators=nn ))
            elif dataType == "datetime":
                setattr(form, key, DateTimeLocalField(Title,default=value,format='%Y-%m-%dT%H:%M',description=description, render_kw=rd, validators=nn ))
                #setattr(form, key, DateTimeInput(Title,default=value,format='%Y-%m-%d %H:%M:%S',description=description, render_kw=rd, validators=nn ))
            elif dataType == "password":
                setattr(form, key, PasswordField(Title,default=value,description=description,  validators=nn))
            elif dataType == "email":
                setattr(form, key, EmailField(Title,default=value,description=description, render_kw=rd, validators=nn ))
            
            putLog('cm', 'setAttribute.col:', Title + key + dataType)
            putLog('cm', 'setAttribute.val:', value)
    return form    
  

def cleanup_form(form):
    for f in form():
        
        if f.name != 'csrf_token':
            if ('sf_' in f.name) or ('cf_' in f.name) or (f.name == 'viewName'):
                exec("del sForm." + f.name)
            elif 'bf_' in f.name:
                exec("del bForm." + f.name)
