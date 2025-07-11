# 2024/11/14
from flask import Flask
from . import commonTool
from . import constant
from . import formInfoGetter


globals()['trail'] = []

def get_curr_path():
    commonTool.putLog('tk', 'get_curr_pass', globals()['trail'])
    if len(globals()['trail']) == 0:
        return []
    else:
        return globals()['trail'][-1]


def init_trail():
    globals()['trail'] = []
    commonTool.putLog('tk', 'init_trail', globals()['trail'])

def push_trail(cpath):
    commonTool.putLog('tk', 'push_trail_before:', cpath)
    if len(globals()['trail']) >0 :
        g = globals()['trail'][-1]
        if (cpath[constant.OBJECT_ID] != g[constant.OBJECT_ID] or # cpath[constant.ENTITY_ID ] != g[constant.ENTITY_ID ] or \
                cpath[constant.MASTER_ENTITY_ID ] != g[constant.MASTER_ENTITY_ID] or cpath[constant.VIEW_ID == 0]) :
            
            globals()['trail'].append(cpath)           # push the trail
    else:
        globals()['trail'].append(cpath)           # push the trail       
        
    commonTool.putLog('tk', 'push_trail_after', globals()['trail'])                                           
    return globals()['trail'][-1]

def pop_up_trail():
    commonTool.putLog('tk', 'pop_up_trail_before:', globals()['trail'])
    if len(globals()['trail']) > 1:
        del globals()['trail'][-1]
        commonTool.putLog('tk', 'pop_up_trail_after:', globals()['trail'])
        
    if len(globals()['trail']) >= 1:
        return globals()['trail'][-1]
    else:
        return [constant.OBJECT_ID_OF_APP ,0,0,0]
    

def get_master_object_id():
    if len(globals()['trail']) > 1:
        data_key_set_prev = globals()['trail'][-2]
        commonTool.putLog('tk', 'get_master_object_id.out', data_key_set_prev)
        return data_key_set_prev[2]
    else:
        return 0
    
    
def get_current_app_name():    
    p = globals()['trail'][-1]
    if p[constant.RUNNING_MODE_ID] == constant.RUNNING_MODE_ID_FOR_SETTING and p[constant.MASTER_ENTITY_ID] > 0:
        if p[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT:
            return formInfoGetter.get_app_name(abs(p[constant.ENTITY_ID]))
        elif p[constant.OBJECT_ID] == constant.OBJECT_ID_OF_OBJECT_FIELD:
            return formInfoGetter.get_app_name(p[constant.MASTER_ENTITY_ID])
    else:
        return formInfoGetter.get_app_name(p[constant.OBJECT_ID])
    
    
def del_viewID():
    p = globals()['trail'][-1]
    p[constant.VIEW_ID]   = 0

