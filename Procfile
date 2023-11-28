release: python manage.py migrate
web: daphne django_projects.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=django_projects.settings -v2
