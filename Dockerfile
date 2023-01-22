FROM python:3.10.8-slim AS base

RUN apt-get update && apt-get install -y \
  xmlsec1

COPY . /app/
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN python3 manage.py migrate
RUN DJANGO_SUPERUSER_USERNAME=admin \
  DJANGO_SUPERUSER_EMAIL=admin@example.com \
  DJANGO_SUPERUSER_PASSWORD=password \
  python3 manage.py createsuperuser --noinput
RUN python3 manage.py collectstatic --noinput
CMD python3 manage.py runserver 0.0.0.0:8000
