#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting build process..."

# Step 1: Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Step 2: Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations
python manage.py migrate

# Step 3: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Step 4: Other setup tasks (if needed)
# Example: Compile translation files
# echo "Compiling translations..."
# python manage.py compilemessages

echo "Build process complete!"
