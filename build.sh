#!/usr/bin/env bash

# Apply database migrations
echo "Applying database migrations"

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

# Create superuser
python manage.py createsu
