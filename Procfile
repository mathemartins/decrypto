release: python manage.py migrate
web: daphne decrypto.asgi:application --port $PORT --bind 0.0.0.0 -v2
celery: celery -A decrypto worker --pool=solo -L  info
celerybeat: celery -A decrypto beat -L INFO
celeryworker: celery -A decrypto worker & celery -A decrypto beat -L INFO & wait -n