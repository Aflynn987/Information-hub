#!/usr/bin/env bash
sudo apt update
# activate venv
source venv/bin/activate
# change directory into folder where application is downloaded
cd Information-hub/
# Create a venv and activate it
source venv/bin/activate
# Manually install Django
# Start the server
python3 manage.py runserver 0:3000