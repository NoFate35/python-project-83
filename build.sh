curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
export PATH="$HOME/.local/bin:$PATH"
apt install mlocate
updatedb
locate psql
make install && psql -a -d $DATABASE_URL -f database.sql
make start
