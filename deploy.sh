#!/usr/local/bin/bash

set -e
set -x

ssh root@95.217.223.96 'cd /opt/apps/cyanblue \
    && git pull \
    && source venv/bin/activate \
    && pip install -r requirements.txt \
    && python manage.py collectstatic --noinput \
    && python manage.py migrate'
