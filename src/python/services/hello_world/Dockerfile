FROM python:3.9

# install poetry
ENV POETRY_HOME=/poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/poetry/bin:${PATH}"

# copy source
COPY ../../../. /lessmore
WORKDIR /lessmore/src/python/services/hello_world

# install dependencies
 RUN poetry install