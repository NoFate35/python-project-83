intdir=$(which bash)
if echo $intdir == "/data/data/com.termux/files/usr/bin/bash"

then
#!/data/data/com.termux/files/usr/bin/bash
pg_ctl -D $PREFIX/var/lib/postgresql start
psql py_flaskdb < database.sql

else
#!/bin/bash
sudo service postgresql start
psql -a -d $DATABASE_URL py_flaskdb
psql py_flaskdb < database.sql

fi
