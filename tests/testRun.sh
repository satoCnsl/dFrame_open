 /bin/bash
cd /home/rocky/dframeBase/202507/testbed/tests/
mysql -uroot -pmypass dframe<_testbed  data.sql

pytest test_Caption_Eng.py
pytest test_auth.py
pytest test_commonTool.py
pytest test_db.py
pytest test_db_exec01.py
pytest test_db_exec02.py
pytest test_db_exec03.py
mysql -uroot -pmypass dframe<  data.sql
pytest test_formInfoGetter.py
read -p "Hit enter: "
mysql -uroot -pmypass dframe<  data.sql
pytest test_navi.py
pytest test_trailKeeper.py
read -p "Hit enter: "
mysql -uroot -pmypass dframe<  data.sql
pytest test_viewEdit.py