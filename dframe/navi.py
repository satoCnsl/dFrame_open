
# 2025/06/19    render:  #selVal  =  formInfoGetter.getMultiSelctValues(formParam[1], formParam[3]), --> delete
# 2025/03/25    navi_button: if bulk_id > 0 ()  length --> dataLength
#                            add "or (c['isReadOnly']==1 and c['isNotNull']==1)""
# 2025/02/24    trigger after save   
# 2025/01/24    isViaForm=True)

from urllib.parse import urlparse
from flask import Blueprint, session, render_template, request,flash # ,Flask, url_for,  redirect

from . import formInfoGetter
from . import commonTool
from . import trailKeeper
from . import constant

navi_app = Blueprint('navi', __name__)

class renderTemplate:
    def __init__(self, d=[], v=0, e=[]):
        self.data_key_set = d
        self.viewID       = v
        self.errData      = e

    def render(self):
        object_id, entity_id, view_id = self.data_key_set[constant.OBJECT_ID],self.data_key_set[constant.ENTITY_ID],self.data_key_set[constant.VIEW_ID]
        
        urlPath = 'dframe/navi/form' + commonTool.set_url(self.data_key_set)
        
        formParam = commonTool.set_formparam(self.data_key_set)
        #formParam: 0:formPrpty 1:formColumns 2:formData 3:formVal 4:dd_link 5:fk_link 6:formButton 7:formMenuBar
        session['menu_bar'] = [{}]
        if self.data_key_set[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT and self.data_key_set[constant.ENTITY_ID] == 0:
            session['menu_bar'] = formParam[7]
        form_msg = None
        if self.errData == []:
            formData = formParam[2]
        else:
            formData = self.errData[1]
            form_msg = formInfoGetter.getDicDescription(self.errData[2])

        offset_list = []
        #if view_id > constant.BULK_VIEWID_BASE_VALUE and self.data_key_set[constant.OFFSET_VALUE] > 0:
        if view_id > constant.BULK_VIEWID_BASE_VALUE and len(formParam[1]) > constant.BULK_FORM_ITEMS_MAX_LEN:
            sql = 'call getOffsetList(' + str(object_id) + ',' + str(view_id) + ')' 
            offset_list = formInfoGetter.exec_sql(sql)
            
        runningMode = []
        if self.data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING:
            runningMode.append('(OBJECT SETTING)')
        else:
            runningMode.append('')
        if self.data_key_set[constant.ENTITY_ID] == -1:
            runningMode.append('enter a new data')
        elif self.data_key_set[constant.ENTITY_ID] > 0:
            runningMode.append('ID:' + str(formData[0]['id']))
        else:
            runningMode.append('')
        runningMode.append(self.data_key_set[constant.RUNNING_MODE_ID])
        
        listViewName = formInfoGetter.getListViewName(self.data_key_set)
        
        #targetFormTitle = formInfoGetter.getFormTitle(object_id,'')  # for Name on the Object Setting Form
        appName = trailKeeper.get_current_app_name()
        
        templateNm = ''
        len_pivotForm = 0    # 0: not pivot Form
        form = commonTool.sForm()
        if object_id == constant.OBJECT_ID_OF_LOGIN:
            templateNm = constant.LOGIN_FORM_NAME
        elif object_id == 200:        
            templateNm = 'homePage'      # to deploy the Single form  
        elif entity_id > 0 or entity_id < 0 :   # entity_id = -1 : to enter a new data entity  
            templateNm = constant.SINGLE_FORM_NAME      # to deploy the Single form
        elif formParam[0][0]['bulkSourceObjectID'] > 0:
            if formParam[0][0]['masterObjectID'] > 0:
                len_pivotForm = len(formParam[2]) + 1  # 0 means non-pivot
                templateNm = constant.BULK_FORM_NAME
            elif len(formParam[1]) > constant.BULK_FORM_ITEMS_MAX_LEN:
                templateNm = constant.COMP_FORM_NAME
            else:
                templateNm = constant.BULK_FORM_NAME
        else:
            templateNm = constant.LIST_FORM_NAME       # to deploy the List form

        if templateNm != constant.LIST_FORM_NAME:            
            #form = commonTool.setForm(templateNm, formParam[1], formData, self.data_key_set[constant.OBJECT_ID], formVal = formParam[3])            
            form = commonTool.setForm(templateNm, formParam[1], formData, self.data_key_set[constant.OBJECT_ID], formVal = formParam[3]) 
       
        #if templateNm != constant.LIST_FORM_NAME and len(formParam[1]) > constant.BULK_FORM_ITEMS_MAX_LEN:  # for cForm
        if templateNm == constant.COMP_FORM_NAME:
            maxLineNumInPage = 1
        else:       
            maxLineNumInPage = formParam[0][0]['maxLinesInPage']  # for lForm
        pagenation =  commonTool.setPageButton(self.data_key_set,maxLineNumInPage, len_pivotForm)
        
        commonTool.putLog('nv', 'render', templateNm)
        return render_template(
            templateNm + '.html',

            #for invt2 APP
            #web_product_v = web_product_v,
            #web_col = web_col,
            #for base.html
            formType    =      'navi',
            campusSize  =      {'width':constant.CAMPUS_WIDTH,'hight': constant.CAMPUS_HIGHT},
            urlPath =          urlPath,
            menu_bar    =      session['menu_bar'],
            formCaption =      [formInfoGetter.getFieldCaption(False, 'Application'),formInfoGetter.getFieldCaption(False, 'Setting')],
            formButton=        formParam[6],
            pageOffset =       pagenation[0],
            pageBtnOnOff =     pagenation[1],
            pageButton   =     ['t', 'p', 'n', 'l'],    # pageTop, pagePrev, pageNext, pageLast
            pageBtnCap   =     ['Top', 'Prev', 'Next', 'Last'],

            #for both sForm.html and list1.html
            runningMode =      runningMode,
            formPrpty=         formParam[0],

            #for sForm.html
            form        =      form,    #commonTool.sForm(),  # for sForm.html only   to set the new instance of sForm class
                                        #commonTool,bForm(),    for cForm to reserve search fields in bForm
            entity_id =        entity_id,           # for sFrom.html to open Search Window 
            dd_link=           formParam[4],        # drill down linkage for sForm.html only
            form_msg =         form_msg,

            #for list1.html
            formCaptionL1 =    [formInfoGetter.getFieldCaption(False, 'List_of'),formInfoGetter.getFieldCaption(False, 'Edit'), \
                                formInfoGetter.getFieldCaption(False, 'Add')], 
            formColumns =      formParam[1],
            formData =         formParam[2],
            #fldList =          formParam[4],	    # for list1.html only	
            fk_link =          formParam[5],        # foreign key linkage for list1.html only
            listViewName=      listViewName,        # for list1 form only
            view_id=            view_id,            # for list1 form only
            appName=           appName,             # form base.html        

            #for cForm.html
            offset_list  = offset_list,
                
        )

@navi_app.route('/dframe/navi/application/', methods=['GET', 'POST'])
def application():
    viewID = session['appViewID']
    data_key_set = [constant.OBJECT_ID_OF_APP, 0, 0, constant.RUNNING_MODE_ID_FOR_USER, viewID, 0]
    trailKeeper.init_trail()
    trailKeeper.push_trail(data_key_set)   
    rt = renderTemplate(data_key_set, v = 0)
    
    return rt.render()


@navi_app.route('/dframe/navi/setting/', methods=['GET', 'POST'])
def setting():
    data_key_set = [constant.OBJECT_ID_OF_OBJECT, 0, 0, constant.RUNNING_MODE_ID_FOR_SETTING,constant.VIEW_ID_OF_SETTING_PORTAL, 0]
    trailKeeper.init_trail()
    trailKeeper.push_trail(data_key_set)   
    rt = renderTemplate(data_key_set, v = 0)
    
    return rt.render()


@navi_app.route('/dframe/navi/form/<int:object_id>/<int:entity_id>/<int:master_object_id>/<int:running_mode_id>/<int:view_id>/<int:offset>/', methods=['GET','POST'])
# to xmit to the form having "object_id" , "entity_id"(if specified) and "masterObjecID"(if specifie)
def setup_form(object_id, entity_id, master_object_id, running_mode_id, view_id, offset):
    viewID = view_id
    commonTool.putLog('nv', 'setup_form objID:', str(object_id) + ' entityID:' + str(entity_id) + ' viewID:' + str(view_id))
    if view_id == 0:
        if entity_id == 0 :
            viewSelID = request.form.get('viewSelID')  # to get selected viewID in List Form
            if viewSelID :           # No, 
                viewID = int(viewSelID)
            else:
                fp = formInfoGetter.get_form_info('FormPrpty', [object_id, 0, 0, 0, 0, 0])
                if fp[0]['bulkSourceObjectID'] > 0:
                    viewID = constant.BULK_VIEWID_BASE_VALUE
        
        elif entity_id > 0:
            recType = formInfoGetter.exec_sql('call getRecTypeInfo(' + str(object_id) + ', 0, 0)')
            if len(recType) > 0:
                viewID = recType[0]['viewID']  
    elif view_id == constant.BULK_VIEWID_BASE_VALUE:
        #fldSize = formInfoGetter.get_table_field_size(object_id)
        # if fldSize > constant.BULK_FORM_ITEMS_MAX_LEN and offset == 0 :
        #    offset = 1            # for the fisrt data  i.e. offset=0 --> whole data 
        
        searchField = formInfoGetter.exec_sql('call getSearchField("' + session['socketDb']  + '",' +str(object_id) + ')')
        viewID = view_id
        pos = 0
        key = ''
        
        for f in searchField:
            key = 'bf_' + f['name']
            #value = form[key].data
            value = request.form.get(key)  # value : None Type
            
            commonTool.putLog('nv', 'setup_form.searchField', f['name'] + str(value) + ' len:' + str(f['dataLength']) + f['dataType'])
            #value =  request.form.get('sf_0_' + f['name'])
            
            if value == None or value == '':
                #tk.Tk().withdraw()
                #messagebox.showinfo("Please set Search Fiels: " + f['name'])
                #viewID = 0
                pos += f['dataLength']
            else:
                if f['name'] == 'date':
                    v_diff = formInfoGetter.exec_sql('select datediff(curdate(), "' + value + '") AS datediff ', isResults=True)
                    value  = v_diff[0]['datediff'] + 31
                viewID += (int(value) )*(10**pos)
                #elif f['name'] == 'dateDiff':
                #    viewID += 100000 + int(value)*(10**pos)
                pos += f['dataLength']
    
    data_key_set = [object_id, entity_id, master_object_id, running_mode_id, viewID, offset]
      
    
    offset = request.args.get('offset')        # to get selected pagenation value in List Form
    if offset is not None:         # No, transit to another form
        data_key_set[constant.OFFSET_VALUE] = int(offset)
    
    commonTool.putLog('nv', 'setup_form.out:', data_key_set)
    commonTool.putLog('nv', 'setup_form.out.viewID:', view_id)
    trailKeeper.push_trail(data_key_set)   
    #renderTemplate(formType, data_key_set, offsetValue, viewID)
    rt = renderTemplate(data_key_set, v=viewID)
    
    return rt.render()


@navi_app.route('/dframe/navi/btn/<string:action_type>/', methods=['GET', 'POST'])
def navi_button(action_type):
    
    commonTool.putLog('nv', 'navi_button', action_type)
    p = trailKeeper.get_curr_path()
    data_key_set = [p[0],p[1],p[2],p[3],p[4],p[5]]      # to create new data instance
    # save the current data then Back to the previous form ?
    # b:Save bn:Save&Add n:Add c:cancel d:Delete
    if action_type in (constant.BUTTON_ACT_SAVE,constant.BUTTON_ACT_SAVE_ADD,constant.BUTTON_ACT_ADD):    # backward form or save and add
        if action_type in (constant.BUTTON_ACT_SAVE,constant.BUTTON_ACT_SAVE_ADD):
            form_Prpty = formInfoGetter.get_form_info('FormPrpty', data_key_set, '', 0)
            
            #data_key_set = trailKeeper.get_curr_path()
            #form_column: gets to be accompanied by its form-value
            bulk_id = form_Prpty[0]['bulkSourceObjectID']
            itel_pivot = 1
            if form_Prpty[0]['masterObjectID'] > 0 and form_Prpty[0]['bulkSourceObjectID'] > 0:
                form_data = formInfoGetter.get_form_info('FormPivotData', data_key_set)
                if len(form_data) > 0:
                    itel_pivot = form_data[0]['CNT']
            else:
                form_data   = formInfoGetter.get_form_info('FormData',    data_key_set, '', 1)
            form_column = formInfoGetter.get_form_info('FormColumns', data_key_set, '', 0)
            master_entity_id = trailKeeper.get_master_object_id()

            for r in range(len(form_data)):
                s = ''
                for i in range(itel_pivot):
                    isModified = False
                    if itel_pivot > 1:
                        s = str(i +1)                    
                    for c in form_column: 
                        c['value'] = None
                        c['value_old'] = str(form_data[r][c['name'] + s])
                        if bulk_id > 0 \
                            and (   (   c['name'] == 'id'  \
                                        or c['isBulkSearchField']==1 and (c['isVisible']==1 or c['foreignObjectID']==0) \
                                    ) \
                                    or c['value_old'] == c['derivedTerm'] and c['isVisible'] == 0 \
                            #    ) \
                            or (c['isVisible'] == 1 and c['isReadOnly'] == 1 and c['isNotNull'] == 1)
                            ):                                              #2025/03/18
                            if c['name'] == 'id':
                                data_key_set[constant.OBJECT_ID] = bulk_id   # to set original object id for bulk "view"object
                                bID = form_data[r]['id' + s]
                                if bID == 0 or bID == None:
                                    data_key_set[constant.ENTITY_ID] = -1    # to insert a new data
                                else:
                                    data_key_set[constant.ENTITY_ID] = bID   # to update data
                            
                            #if c['dataType'] in ('date', 'datetime'):
                            #    c['value'] = commonTool.lap_field(c['dataType'], form_data[r][c['name']],isViaForm=False)
                            #else:
                            #    c['value'] = form_data[r][c['name']]
                            c['value'] = commonTool.lap_field(c['dataType'], c['value_old'],isViaForm=True)


                        elif c['name'] == 'modifiedBy':
                            c['value'] = session.get("user_id")
                        elif c['isVisible']==1 and c['isReadOnly']==0:
                            # to get the id value 
                            if s != '':
                                key =   'sf_' + str(r) + '_' + c['name']  + s
                            else:
                                key =   'sf_' + str(r) + '_' + c['name']
                            value = request.form.get(key)
                            #c['value_old'] = form_data[r][c['name'] + s]
                            if c['isMultiSelect'] == 1:
                                colList = request.form.getlist(key)
                                ms = ''
                                for i in range(len(colList)):     
                                    ms += colList[i].lstrip().rstrip() + ","
                                value = ms
                                if len(colList) == 0:
                                    value = c['value_old']

                            elif value in ("", 'NULL'):
                                value = None
                            
                            value = commonTool.lap_field(c['dataType'],value,isViaForm=True)
                            c['value'] = str(value)
                            if len(c['cmbStrainObjNm']) > 0 or c['foreignObjectID'] > 0 :
                                if  c['isReadOnly'] == False and c['value'] != c['value_old'] :
                                    isModified = True
                                elif c['isReadOnly']:      # 2024-05-12
                                    c['value'] = c['value_old']
                                # 
                                #    for i in range(len(colList)):
                                #        fString += "'" + colList[i] + "',"
                            elif c['name'] != 'id' and value !=None:  #and \
                                #(c['isReadOnly']== 0 and (len(c['foreignKeyFldNm']) == 0 and \
                                #c['isMasterObject'] != 1 or master_entity_id == 0)):
                                if c['dataType'] in ['int','decimal','float','boolean','double','tinyint'] \
                                    and (value == 'NULL' or value == None or value == ''):
                                    c['value'] = 0
                                if c['dataType'] == 'boolean':
                                    if value == 'y':
                                        c['value'] = 1
                                    else:
                                        c['value'] = 0
                                if c['isReadOnly'] :
                                    c['value'] = c['value_old']
                                if c['value']  != c['value_old']:
                                    isModified = True
                            elif c['name'] == 'appID' and data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING:
                                c['value'] = constant.ID_OF_APP_FOR_SETTING
                            elif c['isMasterObject'] == 1 and master_entity_id > 0:
                                c['value'] = master_entity_id
                        elif  ((c['isVisible']==0 and c['isReadOnly']==0) or (c['isReadOnly']==1 and c['isNotNull']==1)) \
                               and c['value_old'] != None :
                            c['value'] = commonTool.lap_field(c['dataType'], c['value_old'],isViaForm=True)
                        commonTool.putLog('nv.button', 'name', c['name'] , str(c['value']) + ' isModified? ' + str(isModified))

                    if data_key_set[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING:
                        cv = check_vals(data_key_set[constant.OBJECT_ID], form_column)
                        if cv[0] == 'failed':
                            render = renderTemplate(data_key_set, 0, e = cv)    
                            return render.render()
                            
                    if isModified:

                        sql_body = commonTool.compile_sql(data_key_set, form_column)
                        if len(sql_body[0]) > 0:

                            # is to update data?
                            if data_key_set[constant.ENTITY_ID] > 0 :
                                formInfoGetter.updt_data_line(data_key_set, sql_body)
                                newID = data_key_set[constant.ENTITY_ID]
                            # to create data
                            else:
                                newID = formInfoGetter.ins_data_line(data_key_set,sql_body)    
            #after insert or update execute trigger defigned on __object table
            if form_Prpty[0]['triggerNm'] is not None:
                dbNm = ''
                if data_key_set[constant.OBJECT_ID] >= constant.OBJECT_ID_START_FOR_APPS:
                    dbNm =  session['appName'] + '.'
                formInfoGetter.exec_sql('call ' + dbNm + form_Prpty[0]['triggerNm'],isResults = False, out = None, commitReq=True)            
            
            if action_type == constant.BUTTON_ACT_SAVE:
                data_key_set = []
                    
        #  New record button pressed?
        if action_type in (constant.BUTTON_ACT_ADD,constant.BUTTON_ACT_SAVE_ADD):# make new record
            #data_key_set = trailKeeper.get_curr_path()
            # when single form, they have same object_id
            
            # add new entry to the object
            if data_key_set == [constant.OBJECT_ID_OF_OBJECT,0,0,constant.RUNNING_MODE_ID_FOR_SETTING,constant.VIEW_ID_OF_SETTING_PORTAL,0] :   
                data_key_set[constant.ENTITY_ID] = constant.ENTITY_ID_FOR_NEW_ONE          # entity_id
                data_key_set[constant.VIEW_ID] = 0    # VIEW_ID:display all fields when setting mode
            else:
                data_key_set[constant.ENTITY_ID] = constant.ENTITY_ID_FOR_NEW_ONE          # entity_id                
                
            trailKeeper.push_trail(data_key_set)                    # push current list form object_id to trail

    # was delte button pressed?
    elif action_type in (constant.BUTTON_ACT_DELETE):
        formInfoGetter.delete_data_line(data_key_set)
        data_key_set = []

    # was Cacel button pressed?
    elif action_type in (constant.BUTTON_ACT_CANCEL):   # cancel 
        data_key_set = []     

    # SWITCHER
    if data_key_set == []:
        data_key_set = trailKeeper.pop_up_trail()
    render = renderTemplate(data_key_set, 0)
    
    return render.render()


def check_vals(objectID, formColumns):
    if objectID == constant.OBJECT_ID_OF_OBJECT:
        return 'pass'

    elif objectID == constant.OBJECT_ID_OF_OBJECT_FIELD:
        v_o = '0'
        v_n = ''
        v_d = ''
        v_c = ''
        for c in formColumns:   
            if c['name']   == 'foreignObjectID':
                v_o = c['value']
            elif c['name'] == 'foreignKeyFldNm':
                v_n = c['value']
            elif c['name'] == 'derivedTerm':
                v_d = c['value']
            elif c['name'] == 'cmbStrainObjNm':
                v_c = c['value']
        if v_o == '0' and v_n == 'NULL':  # and v_d == 'NULL':
            return 'pass'
        elif v_o not in ('0','NULL') and v_n != 'NULL' and v_d != 'NULL':
            return 'pass'
        elif v_c != 'NULL' and v_o == '0' and v_n == 'NULL' and v_d == 'NULL':
            return 'pass'
        else:    
            if v_o != '0':
                msg = constant.FOREIGN_OBJ_REF_ERR
            elif v_c != 'NULL':
                msg = constant.CMB_STRAIN_OBJ_NM_ERR
            else:
                msg = None
            return ['failed', msg]
    return 'pass'
    








