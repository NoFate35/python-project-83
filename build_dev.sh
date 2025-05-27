result=$which bash
#!'$result'
if ['$result'='/data/data/com.termux/files/usr/bin/bash']

then
pg_ctl -D $PREFIX/var/lib/postgresql start
psql py_flaskdb < database.sql

else
sudo service postgresql start
psql py_flaskdb < database.sql
fi
