FROM python:3.9

# - install poetry
ENV POETRY_HOME=/poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/poetry/bin:${PATH}"
# setup global python as default
RUN poetry config virtualenvs.create false

# - install basic dependencies. NOTE: requirements.txt fild is created manually. See update_requirements.sh script
COPY src/python/services/hello-world/requirements.txt .
RUN pip install -r requirements.txt

## - copy source
COPY ../../../. /app
WORKDIR /app/src/python/services/hello-world

## - install all left dependencies (editable installs, ...)
RUN poetry install
