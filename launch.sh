#!/bin/sh
set -e

DB="db/db.sqlite3"
if [ ! -f "$DB" ]; then
    NEED_SUPER=true
    echo "Need to create superuser"
fi

python manage.py makemigrations lists
python manage.py migrate

if [ "$NEED_SUPER" == "true" ]; then
    echo "Creating superuser..."
    echo "from django.contrib.auth.models import User;import os; User.objects.create_superuser(os.environ.get('ADMIN_USERNAME'), os.environ.get('ADMIN_EMAIL'), os.environ.get('ADMIN_PASSWORD'))" | python manage.py shell
fi

echo "Running server..."
exec python manage.py runserver "$@"