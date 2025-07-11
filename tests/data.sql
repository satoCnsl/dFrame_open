drop database if exists testbed; 
create database testbed;
update dframe_testbed.__systemini set language="eng" where id=1;
   
DELETE FROM dframe_testbed.__object;
DELETE FROM dframe_testbed.__list_view; 
DELETE FROM dframe_testbed.__report;      
ALTER TABLE dframe_testbed.__object           AUTO_INCREMENT =  100;       
ALTER TABLE dframe_testbed.__object_field     AUTO_INCREMENT = 1000;       
ALTER TABLE dframe_testbed.__object_field_rw  AUTO_INCREMENT = 1000;     
ALTER TABLE dframe_testbed.__list_view        AUTO_INCREMENT = 100;  
ALTER TABLE dframe_testbed.__list_view_filter AUTO_INCREMENT = 1000;  
ALTER TABLE dframe_testbed.__list_view_field  AUTO_INCREMENT = 1000;  
ALTER TABLE dframe_testbed.__report           AUTO_INCREMENT = 100; 