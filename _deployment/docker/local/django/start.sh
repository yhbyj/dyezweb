#!/bin/sh

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
gunicorn dyezweb.wsgi:application -w 4 -k gthread -b 0.0.0.0:8000 --chdir=/app