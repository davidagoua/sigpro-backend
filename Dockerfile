
FROM python:3.12-bullseye

WORKDIR /app

ENV DJANGO_SETTINGS_MODULE="prsep.settings.prod"
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

#RUN python manage.py collectstatic --no-input
# RUN python manage.py migrate


EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000","--reload","-w 5","-k gevent", "prsep.wsgi:application"]
