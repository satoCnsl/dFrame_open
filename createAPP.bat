
mysql -uroot -pmypass -e "CREATE DATABASE %1 CHARACTER SET utf8mb4"
mysql -uroot -pmypass -e "CREATE DATABASE dframe_%1 CHARACTER SET utf8mb4"

mysql -uroot -pmypass --default-character-set=sjis dframe_%1 < SQL\dframe_socket.dump
mysql -uroot -pmypass -e "UPDATE dframe_%1.__systemini set appNm='%1'"
mysql -uroot -pmypass -e "INSERT INTO dframe.__application (name, title)value ('%1', '%2')"


flaskrun.bat