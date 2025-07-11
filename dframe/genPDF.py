# 2024/11/14
import pdfkit
import os
#import winreg
from datetime import datetime
# from xhtml2pdf import pisa
from flask import  Blueprint, session, send_file
#from fieldBuilder import updateData,saveFilter
import os
from . import formInfoGetter 
from . import trailKeeper
from . import commonTool
from . import constant
from . import navi

genPDF_app = Blueprint('genPDF', __name__)

#filter editing form: a view definition file is consisted by ond/or more 
#                   filter definition lines, those are combined by ana/or to each other
@genPDF_app.route('/dframe/print/<int:report_id>/<int:entity_id>/<string:scope>/' , methods=['GET','POST'])
def generate_pdf(report_id, entity_id, scope):
    dNm = session['socketDb']
    rpt = formInfoGetter.exec_sql('select * from ' + dNm + '.__report_v where id=' + str(report_id))
    objNm = rpt[0]['title']

    wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    #wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    # ファイルのパスを指定
    root = os.path.dirname(__file__)
    print('gp30: root:',root)
    temp_file = root + r'\templates\report.html'
    work_file = root + r'\templates\work.html'

    tdatetime = datetime.now()
    tstr = tdatetime.strftime('%Y%m%d%H%M%S')
    entityList = getEntityList(report_id, entity_id, scope)
    i = 0
    for row in entityList:
        i += 1
        output_file = root + r'\out_files\r-' + objNm + '-' + str(i) + '-'  +  tstr + '.pdf'
        print('gp49: outpurFile::::', output_file)
        e = row['id']
        # テンプレートを読む --- (*3)
        with open(temp_file, 'rt', encoding='utf-8') as fp:
            text = fp.read()
            #to get set of schemas each of which constitutes a table
            text = setFieldOnTemplate(text,report_id, e)
    
    
        # 一時ファイルを出力 --- (*5)
        with open(work_file, 'wt', encoding='utf-8') as fp:
            wf = fp.write(text)    
        print('gp54', 'pass AA',wf)

        
        resultFile = open(output_file, "w+b")
        
        #pisa.CreatePDF(src=work_file.encode('utf-8'), dest=resultFile, encoding='utf-8')
        resultFile.close()
        
        #pdfkit.from_file(html, "output.pdf", configuration=configure) 
        # 変換オプションなどを指定
        conf = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)            
        #conf = pdfkit.configuration(wkhtmltopdf=pisa)

        options = {'page-size': rpt[0]['pageSize'],'orientation':rpt[0]['orientation'], 'encoding': "UTF-8"}
        
        # HTML/CSSファイルをPDF出力 --- (*6)
        pdfkit.from_file(work_file, output_file, options=options, configuration=conf)
        print("gp71:', ok1")
    
    return send_file(output_file)

def setFieldOnTemplate(text, reportID , entity_id):
    dNm = session['socketDb']
    #to analyze the report schema
    sql = 'call dframe.getRprtSchema("' + dNm + '",' + str(reportID) + ')'
    fld = formInfoGetter.exec_sql(sql)
    title = fld[0]['title']
    text = text.replace('__title__', title)

    print('gp85:', reportID, fld[0])
    offset = 0
    t_depth = 0   # for nested table counter
    j = 0
    # to scan the schema table to costruct tables assembling the report
    for f in fld:
        print('**', f['id'], ' offset:', offset)
        #scope = "'dummy'"
        scope ="'0'"
        # to get the source data to construct a table
        if f['sourceData'] != 'None' and f['sourceData'] != 'offset':
            dt = formInfoGetter.exec_sql("call " + session['appName'] + "." + f['sourceData'] + "(" + str(entity_id) + "," + scope +")")
            offset = 0
        elif f['sourceData'] == 'offset':
            offset += 1
        else:
            offset = 0
        # to set data to each line in a table
        offset, tt = setTableTag(f, dt, offset, t_depth)

        text = text.replace('__sec' + str(j) + '__'  , tt)
        
        j += 1
        print('gP102:', j, ' : ' ,offset)
    
    if offset > 0:
        tt += '</tr></table>'
    
    while j <= 15:
        text = text.replace('__sec' + str(j) + '__'  , '')
        j += 1
    #print('***',j, ' txt:',text)
    return text

def setTableTag(field, dataset, offset, t_depth):
    f = field
    tt = ''
    print('pg121:',offset,' f:', f, ' d:', dataset, ) 
    
    w = f['width_1stCol'] + f['width_2ndCol'] + f['width_midCol']*(f['numOfCols']-4) + f['width_1stTailCol'] + f['width_2ndTailCol']
    fs = f['fontSize']
    fontSize = ''
    if fs != None:
        fontSize = 'font-size:' + str(fs) + 'px; ' 
    if f['type'] == 'table':
        tt = '<table width="' +str(w) + '%" border="' + str(f['border']) + '" style="border-collapse:collapse; vertical-align:middle;' + fontSize + '">'
        if f['sourceData'] != 'None':
            # is multiple data colums ?
            if len(dataset[0])> 1: 
                if f['numOfRows'] == 999:
                    num = len(dataset)
                else:
                    num = f['numOfRows']        
                print('gp136:',num ,len(dataset[0]))   
                print('5555',f['numOfCols'])
                for r in range(num):                # multi rows x multi columns -- data set [row][field] 
                    tt += '<tr>'                                              # single row 
                    for c in range(f['numOfCols']):            # dataset row ['fld'] =  colomun val 
                        print('661' + tt, dataset[r]['fld' + str(c+1)])
                        tt += setTDtag(f, dataset[r]['fld' + str(c+1)], c)  # build <td> .... </td>
                    tt +=  '</tr> '
                print('666' + tt)
            else:                                              # single row 
                for r in range(f['numOfCols']):                # dataset row ['fld'] =  colomun val 
                    tt += setTDtag(f, dataset[r + offset]['fld'] , r)  # build <td> .... </td>
                    print('gp145:',r, offset )
            offset += r
            tt += '</table>  '
            t_depth = 0
            print('777' + tt )
        else:
            t_depth += 1
            tt += '<tr>'
    elif f['type'] == 'td' and f['sourceData'] != None:       
        for r in range(f['numOfRows']):
            tt += setTDtag(f, dataset[r + offset]['fld'] , r)
        offset += r
    print('gp156:','offset:',offset, tt[:20] )    

    return offset, tt

def setTDtag(f, dataval, colNo ):         
    q = 'call getRprtWidthVal("'+ session['socketDb'] + '",'  + str(f['id']) + ',' + str(colNo + 1) + ')'
    w = formInfoGetter.exec_sql(q)
    #print('gp163:', dataval ,' width:', w[0]['width'],' id:', f['id'],' colNo:', colNo)
    if dataval == None:
        dataval = " "
    tt = '<td style = "text-align:' + f['align'] + '; vertical-align:' + f['v_align'] + '"  class="padding" width ="' +  \
         str(w[0]['width']) + '%" height="' + str(f['height']) + '">' + str(dataval) + '</td>'        
    sd = 0
    return tt

def getEntityList(report_id, entity_id, scope):
    if scope == 'id':
        return [{'id':entity_id}]
    else:
        dNm = session['socketDb']
        q = 'call dframe.getRprtEntity("' +  dNm + '",' + str(report_id) + ',' + str(entity_id)  + ',"' + scope + '")'
        print('gp177:', q)
        #e = formInfoGetter.exec_sql(q)  #2024/06/22
        e = formInfoGetter.exec_sql(q, isResults=True)  #2024/06/22
        return e

