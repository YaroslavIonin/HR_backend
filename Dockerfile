FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /code

EXPOSE 8000

COPY requirements.txt .

RUN python -m pip install -r requirements.txt


CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
