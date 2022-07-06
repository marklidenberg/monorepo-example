FROM python:3.9

# copy source
COPY . /app
WORKDIR /app

# install poetry
ENV POETRY_HOME=/poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/poetry/bin:${PATH}"

# install dependencies
RUN poetry install

# run app
ENTRYPOINT ["poetry"]
CMD ["run python hello_world/app.py"]
