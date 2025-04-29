curl -LsSf https://astral.sh/uv/install.sh | sh
exec bash
source $HOME/.local/bin/env (sh, bash, zsh)
uv add gunicorn
make install
