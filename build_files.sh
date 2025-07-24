#!/bin/bash

# Build the project
echo "Creating Build Directory..."

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Verify Django installation
echo "Verifying Django installation..."
python -c "import django; print('Django version:', django.get_version())"

echo "Make Migration..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "Collect Static..."
python manage.py collectstatic --noinput --clear
