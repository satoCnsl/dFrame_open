# 2025/06/19  #formInfoGetter.deleteData --> delete_data_line([constant.OBJECT_ID_OF_VIEW, viewID, 0, 0, 0,0])
# 2025/01/20  02/02 
import math
from tokenize import String
from flask import  Blueprint, session
from flask import Flask,  render_template, url_for, request, redirect
from wtforms import SelectMultipleField
#from fieldBuilder import updateData,saveFilter
from . import formInfoGetter 
from . import trailKeeper
from . import commonTool
from . import constant
from . import navi

viewEdit_app = Blueprint('select', __name__)


#origin: list1.html
#filter editing form: a view definition file is consisted by ond/or more 
#                   filter definition lines, those are combined by ana/or to each other
@viewEdit_app.route('/dframe/view/open/<string:actType>/' , methods=['GET','POST'])
def viewForm(actType):
    commonTool.putLog('ve', 'viewFom', actType)
    runningModeID = 0
    accountID = session.get("user_id")
    socketDb = session.get("socketDb")
    if actType == 'A':      # Add a view declaration
        trailKeeper.del_viewID()
        viewName = None
    viewID = trailKeeper.get_curr_path()[constant.VIEW_ID]
    if viewID == 0 and trailKeeper.get_curr_path()[constant.OBJECT_ID] == constant.OBJECT_ID_OF_VIEW_FIELD:
        viewID = trailKeeper.get_curr_path()[constant.MASTER_ENTITY_ID]
    if actType == 'E':    # Edit the view declaration
        viewName = formInfoGetter.getObjFldVal('__list_view_v', viewID, 'name')
        
    objectID = trailKeeper.get_curr_path()[constant.OBJECT_ID]

    DFcpath = [constant.OBJECT_ID_OF_VIEW_FILTER, 0, viewID, runningModeID, 0, 0]

    trailKeeper.push_trail(DFcpath)
   
    # BUILD FORM
    formParam = commonTool.set_formparam(DFcpath)  # DFcpath
    #       0         1        2        3      4       5       6           7
    #  formPrpty,formColumns,formData,formVal,dd_link,fk_link,formButton,formMenuBar
    btnList = []
    for b in formParam[6]:     # formButton           2025/01/20
        btnList.append(b['actionType'])
    
    #bForm = commonTool.setForm(constant.VIEW_EDIT_FORM_NAME,formColmns, formData, objectID, formVal, valueSet=None) formParam[1], formParam[2], objectID, formVal = formParam[5], valueSet=viewName)
    # set SelectMultiplField on Colum Selection section
    commonTool.setViewForm(constant.VIEW_EDIT_FORM_NAME, formParam[1], formParam[2], objectID, formParam[3], valueSet=viewName)
    
    DFcpathSel = [constant.OBJECT_ID_OF_VIEW_FIELD, 0, viewID, runningModeID, 0, 0]
    formParamSel = commonTool.set_formparam(DFcpathSel) 
    fieldList = formInfoGetter.getFieldList(socketDb, accountID, objectID, 0)
    fieldListDef = formInfoGetter.getObjFldVal('__list_view_field_v', 0, 'objectFieldID', where='listViewID=' + str(viewID))   
    
    commonTool.setViewForm(constant.VIEW_EDIT_SUBFORM_NAME, formParamSel[1], [], objectID, fieldListDef, valueSet=fieldList)  

    commonTool.putLog('ve', 'viewForm.render', formParam[1]) 

    return render_template(
        'filterBuild.html',
        form = commonTool.sForm(),
        formType = 'view',
        #viewName = viewName,
        formCaption = [formInfoGetter.getFieldCaption(False, 'Application'),formInfoGetter.getFieldCaption(False, 'Setting')],
        fieldCaption = formInfoGetter.getFieldCaption(True, ''),
        formPrpty  = formParam[0],      # for base.html
        formButton = formParam[6],      # for base.html
        appName =  trailKeeper.get_current_app_name(),     # for base.html
        message=''
    )


#origin: filterBuider.html
#filter declaration data registration: to database
#filterSpec:[[filterItem0],...,[filterItem4]]
#filterItem:[objectFieldID, fieldOperator, value, andOr]
@viewEdit_app.route('/dframe/view/btn/<string:actType>/' , methods=['GET','POST'])
def viewButton(actType):

    accountID = session.get("user_id")
    formName = constant.VIEW_EDIT_FORM_NAME
    form = commonTool.sForm()
    viewName = request.form.get('viewName')

    data_key_set = trailKeeper.get_curr_path()
    DFcpath = trailKeeper.pop_up_trail()
    
    commonTool.putLog('ve', 'viewButton', actType + ':' + viewName)
    
    if viewName != None:
        viewID =  0
    elif DFcpath[constant.OBJECT_ID] == constant.OBJECT_ID_OF_VIEW_FILTER:
        viewID = DFcpath[constant.MASTER_ENTITY_ID]
        viewName = formInfoGetter.getObjFldVal('__list_view_v', viewID, 'name') 
    else:
        viewID = DFcpath[constant.VIEW_ID]  # get the viewID on list1.html 
        viewName = formInfoGetter.getObjFldVal('__list_view_v', viewID, 'name') 
    
    #  save Filter Data then Back to the list form?
    if actType == 'b' :    # backward form
        
        form_column = formInfoGetter.get_form_info('FormColumns', data_key_set)
        filterSpec = []     #each Detail Line on  Filter Editing Form

        i = 0
        for itelNo in range(constant.VIEW_FILTER_LINES_LEN):
            filterItem = []     #Whole Filter Editing Lines
            for c in form_column:  
                if c['isVisible'] == 1 and c['name'] != 'id':
                # to get the id value  
                    key = 'sf_' + str(i) + '_' + c['name']
                    value = request.form.get(key)
                    dType = None
                    # value field get data type of the value on the value field
                    #if c['name'] == 'objectFieldID' and value > str(0):
                    if c['name'] == 'objectFieldID' and value != None and len(value) > 0:
                        dType = formInfoGetter.getObjFldVal('__object_field', 0, 'dataType', ' id=' + str(value))
                    if c['name'] == 'value' and dType != None:                        
                        value = commonTool.lap_field(dType, value, isViaForm = True)
                    else:
                    #if c['name'] in ('fieldOperator', 'andOr'):             # 20250202
                        value = commonTool.lap_field(c['dataType'], value, isViaForm = True)
                    
                    if value != None or c['name'] == 'andOr':
                        filterItem.append(value)
                    else:
                        if c['name'] != 'andOr':
                            i = 999
                        break
            i += 1
            if i == 999:
                break
            if filterItem[0] > '':
                filterSpec.append(filterItem)

        if len(filterSpec) > 0:
            filterSpec[-1][3] = ''    #delete "andOr" onto the last filter data line
            # to update Filter Data updateFilter(object_id, viewName, filterSpec, accountID)
            v_set = commonTool.updateFilter(DFcpath, viewName, filterSpec, accountID)

            # update __list_view_field data
            #colList = request.form.getlist(constant.VIEW_EDIT_SUBFORM_NAME + "00000")
            colList = request.form.getlist("sf_999_fieldSel")
            commonTool.setViewCol(colList,v_set)

        # view_field on Column Selection
        key = formName + '{:04}'.format(itelNo * constant.MAX_LEN_OF_FIELDS) + str(i)

    # was Cacel button pressed?
    #elif actType == 'c':   # cancel 
    #    DFcpath = []     

    # was Delete button pressed?
    elif actType == 'd':
        viewID = DFcpath[constant.VIEW_ID]
        formInfoGetter.delete_data_line([constant.OBJECT_ID_OF_VIEW, viewID, 0, 0, 0,0])

    render = navi.renderTemplate(DFcpath, viewID)    
    return render.render()


