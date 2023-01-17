celery -A AutoCountApi.celery worker -l info #start celery


celery -A AutoCountApi.celery worker --loglevel=info -P eventlet # with eventlet
 