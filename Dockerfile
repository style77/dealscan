FROM python:3.11

ENV PIP_NO_CACHE_DIR off
ENV PIP_DISABLE_PIP_VERSION_CHECK on
ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev netcat-traditional \
    build-essential libpq-dev 

WORKDIR /usr/src/app

COPY poetry.lock pyproject.toml /usr/src/app/

RUN pip3 install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction \
    && rm -rf /root/.cache/pypoetry

COPY . /usr/src/app

RUN chmod +x /usr/src/app/crawler/jobs.sh

RUN python manage.py collectstatic --noinput

EXPOSE 8000