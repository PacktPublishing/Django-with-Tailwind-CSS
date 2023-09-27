#!/bin/sh

# reset the migrations
find . -path "*/migrations/*" -name "*.py" -not -path "*__init__*" -delete
find . -path "*/migrations/*.pyc" -delete

# remove the db
rm -f "db.sqlite3"

# run the migrations
python manage.py makemigrations
python manage.py migrate

# create the superuser
echo "from django.contrib.auth.models import User; User.objects.create_superuser('lukaszmakinia', '', 'somepassword')" | python manage.py shell

# prepare the dummy data
python manage.py generate_dummy_data