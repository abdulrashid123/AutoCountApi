celery -A AutoCountApi.celery worker -l info #start celery


 celery -A myapp.celeryapp worker --loglevel=info -P eventlet # with eventlet
 