# Sub Creator

A tool to auto generate, translate and embed subtitles for short movies.


## How to install

This is for Linux!

Install Python 3, Python Virtual Env(venv, this is found on your system repository) and Git,
then clone this repository and create a virtual environment inside it, now install dependencies
and starting using!

Here's a script for automating all I can without knowing what system you use:

```bash
mkdir -p ~/.local/bin
cd ~/.local
git clone --depth=1 https://github.com/dheison0/subcreator
cd subcreator
python -m venv env
source env/bin/activate
pip install -r requirements.txt

p=$HOME/.local/bin/subcreator
# Create a script to run subcreator without needing to activate venv manually every time
echo '#!/usr/bin/env bash' > "$p"
echo 'root="$HOME/.local/subcreator"' >> "$p"
echo 'source "$root/env/bin/activate"' >> "$p"
echo 'exec "$root/subcreator.py" "$@"' >> "$p"
chmod +x "$p"
```