:'
#!/bin/bash
sudo service postgresql start
psql -a -d $DATABASE_URL flaskdb
psql py_flaskdb < database.sql
'

#!/data/data/com.termux/files/usr/bin/bash
pg_ctl -D $PREFIX/var/lib/postgresql start
psql py_flaskdb < database.sql

