release: python manage.py migrate
web: daphne dcrypt22.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=dcrypt22.settings -v2
