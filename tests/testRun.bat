
mysql -h localhost -u root -pmypass dframe<  data.sql

pytest test_Caption_Eng.py
pytest test_auth.py
pytest test_commonTool.py
pytest test_db.py

pytest test_db_exec01.py

pytest test_db_exec02.py

pytest test_db_exec03.py

mysql -h localhost -u root -pmypass dframe<  data.sql
pytest test_formInfoGetter.py

pause
mysql -h localhost -u root -pmypass dframe<  data.sql

pytest test_navi.py

pytest test_trailKeeper.py
pause
mysql -h localhost -u root -pmypass dframe<  data.sql
pytest test_viewEdit.py

