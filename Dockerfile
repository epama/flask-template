FROM python:3.8-alpine as build-stage

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

RUN apk --update add curl postgresql-dev build-base && \
    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN /root/.poetry/bin/poetry export -f requirements.txt > requirements.txt

RUN pip install --user -r requirements.txt

FROM python:3.8-alpine AS final

RUN apk --update add py-gunicorn libpq

COPY --from=build-stage /root/.local /root/.local

WORKDIR /app
RUN mkdir /app/google_apikey

COPY . /app

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

CMD gunicorn --bind 0.0.0.0:8000 wsgi:app