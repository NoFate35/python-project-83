#!/usr/bin/bash
sudo service postgresql start
psql py_flaskdb < database.sql
