intdir=/data/data/com.termux/files/usr/bin/bash
ttt=/data/data/com.termux/files/usr/bin/bash
if ["$intdir"="$ttt"]

then
#!/data/data/com.termux/files/usr/bin/bash
pg_ctl -D $PREFIX/var/lib/postgresql start
psql py_flaskdb < database.sql

else
#!/usr/bin/bash
sudo service postgresql start
psql py_flaskdb < database.sql

fi
