## <pre class="notranslate"><code>dFrame</code></pre>
  dFrame is an open source PaaS (Platform as a Service) solution. You can evaluate the prototype now.
  You can build up a business application without any code (No Code) or with small amount of SQL statements (Low Code). <br>
  It should be strongly mentioned that the source code (or system information) of your application is build on MySQL database as "data", that is, the ultimate target of dFrame is "auto porgraming" thru AI generator.
  For details visit web site <a href="http://home.s06.itscom.net/datacent/index_eng.html" >PaaS dFrame</a><br>
   <a href="https://youtu.be/lVeoRK1wMJ0" >YouTube dframe:Create an app with nocode(5min)</a><br>
## Reqirments
   Windows , Linux<br>
   flask/Python3<br>
   MySQL<br>

## Source Code
   Please download from the branch "master"

## Create dFrame Platform
   1.make the file folder for your PaaS Platform on your system(ex."dFrameSystem")<br>
   2.deploy download file of 'dframe'package to the above folder<br>

## Create database on MySQL
   1.create the following schema<br>
        dframe: 	dframe control information<br>
	testbed:	sample app for training tool for biginners as well as testbed for pytest<br>
	dframe_testbed:	control information for "testbed" app<br>
   2.down load mysql dump<br>
	mysql -uroot -pmypass dframe < ../sql/dframe.dump<br>
        mysql -uroot -pmypass dframe_testbed < ../sql/dframe_socket.dump<br>

## Instration:Layout
dFrameSystem<br>
　|---dframe/<br>
　|　　　|---__init__.py<br>
　|　　　|---auth.py<br>
　|　　　|---commonTool.py<br>
　|　　　|---constant.py<br>
　|　　　|---db.py<br>
　|　　　|---formInfoGetting.py<br>
　|　　　|---genPDF.py<br>
　|　　　|---index.py<br>
　|　　　|---navi.py<br>
　|　　　|---trailKeeper.py<br>
　|　　　|---viewEdit.py<br>
　|　　　|---static/<br>
　|　　　|---templates/<br>
　|　　　|　　　|---auth/<br>
　|　　　|　　　|　　　|---login.html<br>
　|　　　|　　　|---base.html<br>
　|　　　|　　　|---bForm.html<br>
　|　　　|　　　|---.....html<br>
　|　　　|---out_files/<br>
　|<br>
　|---sql<br>
　|　　　|---dframe_inv2_20250701.dump<br>
　|　　　|---dframe.dump<br>
　|　　　|---dframe_inv2_20250701.dump<br>
　|　　　|---dframe_socket.dump<br>
　|　　　|---nschool_20250701.dump<br>
　|　　　|---nschool_20250701.dump<br>
　|<br>
　|---logfile/<br>
　|　　　|---logger.log<br>
　|<br>
　|---tests/<br>
　|　　　|---__init__.py<br>
　|　　　|---.....py<br>
　|　　　|---testRun.bat<br>
　|　　　|---testRun.sh<br>
　|<br>
　|---venv/<br>
　|---flaskRun.bat<br>
　|---flaskrun.sh<br>
　|---createApp.bat<br>
　|---createapp.sh<br>

## Run testbed app on Setting mode
   1.cd dFrameSystem(your PaaS Platform)<br>
   2.sh flaskrun.sh(linux) or flaskRun.bat(widows)<br>
   3.reply to log form as "admin" as user name and "password" as password as well as choice "testbed" as app name selection menu.<br>
   
## Create tables(objects) on the testbed app
   1.set runnning mode thrugh hitting "Setting" link on the top menu bar on the form<br>
      (defalut running mode is "applicationt"<br>
   2.Hit "Add" button to create new table(object)<br>
   3.define table name on the table definition form then hit "Save" button<br>
   4.You will find your new table(object) name on the object list form<br>
   5.Hit "setting" link on your new table(object) on the object list form <br>
   6.define data fields for your new table(object)<br>
   for more detail, please vist YouTube (search "dframe")<br>

## Run testbed app on Application mode
   1.Hit "Application" link on the top menu bar on the form<br>
   2.You can see your object(s) list on the form<br>
   3.Hit "Open" link on the object(s) list<br>
   4.There is no data, "empty", on that object.<br>
   5.Hit "Add" button to create data of the object<br>
   6.Empty form of the object is set for your new data entry<br>

## Create your new application
   to create new applicaton,<br>
   1.create new schema on MySQL whose name is of mame of your new application (ex."newapp")<br>
   2.sh createapp.sh newapp NewAPP (or createAPP.bat newapp,NewApp)<br>
   　newapp:your object name(sample) NewAPP:title of your new application<br>
   3.reply to log form as "admin" as user name and "password" as password as well as choice "NewAPP" as app name selection menu.<br>
   4.define objects and their fields for NewAPP like as mentioned for testbed app<br>

## Sample applications:
   1.Nursly School Document Support System: dframe_nschool_20250701.dump, nschool_20250701.dump(Japanese version)<br>
   2.Inventory Information System: dframe_invt2_20250701.dump, invt2_20250701.dump(English version)<br>
   Those source code are available to download from the branch "master"

## If you have any questions or comments, please mail to dframe@u01.itscom.net .
