#!/bin/bash


NAME='best_selling'
DJANGODIR=/var/www/best_selling
SOCKFILE=/var/www/best_selling/best_selling.sock
USER=mahdi
GROUP=mahdi
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=best_selling.settings
DJANGO_WSGI_MODULE=best_selling.wsgi

echo "Starting $NAME as `whoami`"

cd $DJANGODIR
source /var/www/best_selling/selling-venv/bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

exec /var/www/best_selling/selling-venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=-
