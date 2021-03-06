#!/usr/local/bin/bash

set -e
set -x

# push origin
git push origin master

# push github
git push github master

# make sure tests pass
python manage.py test

# pull and reload on server
ssh root@95.217.223.96 'cd /opt/apps/cyanblue \
    && git pull \
    && source venv/bin/activate \
    && pip install -r requirements.txt \
    && python manage.py collectstatic --noinput \
    && python manage.py migrate \
    && touch /etc/uwsgi/vassals/cyanblue.ini'
