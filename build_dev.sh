#!/usr/bin/bash
git pull
sudo service postgresql start
psql py_flaskdb < database.sql
uv add ruff --dev
