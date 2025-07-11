
cd %~dp0
rem pause
set flask_app=dframe
set flask_env=development
flask run
flask init-db