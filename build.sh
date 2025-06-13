curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
apt update
apt install postgresql
make install && psql -a -d $DATABASE_URL -f database.sql
make start
