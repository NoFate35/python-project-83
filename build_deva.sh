#!/data/data/com.termux/files/usr/bin/bash
git pull
pg_ctl -D $PREFIX/var/lib/postgresql start
psql py_flaskdb < database.sql
