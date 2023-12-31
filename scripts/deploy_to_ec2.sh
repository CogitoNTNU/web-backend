#!/bin/bash
# deploy_to_ec2.sh

# Navigate to your Django project directory
cd Backend/Cogito-Backend

# Pull the latest code
git pull origin main

# Install any new dependencies
pip install -r requirements.txt

# Make database migrations
python manage.py makemigrations

# Apply database migrations
python manage.py migrate

# Restart your Django application within a tmux session
TMUX_SESSION_NAME="django_app"

# Check if the tmux session exists
if tmux has-session -t $TMUX_SESSION_NAME 2>/dev/null; then
  # If it exists, kill the session
  tmux kill-session -t $TMUX_SESSION_NAME
fi

# Create a new tmux session and run your Django application
tmux new-session -d -s $TMUX_SESSION_NAME "python manage.py runserver 0.0.0.0:8000"

echo "Deployment completed."
