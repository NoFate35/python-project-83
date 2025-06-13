curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
locate psql
make install && psql -a -d $DATABASE_URL -f database.sql
make start
