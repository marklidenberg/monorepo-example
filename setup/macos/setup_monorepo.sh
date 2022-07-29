# - Go to repo root
cd ${0%/*} # go to file directory
cd ../.. # todo maybe: cd by pattern for bash?

# - Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# - Install Git LFS
brew install git-lfs

# - Install Poetry
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# - Install pre-commit
brew install pre-commit
pre-commit install

# -
