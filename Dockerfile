FROM python:3.12.7-alpine

ENV POETRY_VERSION=1.7.1

WORKDIR /opt/src/

RUN apk update
RUN pip install --upgrade pip

COPY poetry.lock pyproject.toml ./

RUN yes | pip install --no-cache-dir "poetry==$POETRY_VERSION" && \
	poetry config virtualenvs.create false && \
	poetry install --only main --no-interaction --no-ansi

COPY src .

CMD ["python", "main.py"]
