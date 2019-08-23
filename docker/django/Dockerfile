FROM revolutionsystems/python:3.7.4-wee-optimized-lto

WORKDIR /app

ENV PYTHONUNBUFFERED 1
RUN python3.7 -m pip install -U pip setuptools

COPY requirements /tmp/requirements
RUN python3.7 -m pip install -U --no-cache-dir \
    -r /tmp/requirements/development.txt \
    pylibmc==1.6.1

COPY docker/django/celery/beat_start.sh /start-celerybeat
RUN chmod +x /start-celerybeat

COPY docker/django/celery/flower_start.sh /start-flower
RUN chmod +x /start-flower

COPY docker/django/jupyter_entrypoint.sh /usr/local/bin/jupyter_entrypoint.sh
RUN chmod +x /usr/local/bin/jupyter_entrypoint.sh

COPY docker/django/django_entrypoint.sh /usr/local/bin/django_entrypoint.sh
RUN chmod +x /usr/local/bin/django_entrypoint.sh

ENTRYPOINT ["django_entrypoint.sh"]
