#!/usr/bin/env bash
sudo apt update && sudo apt install -y python3-pip && sudo pip3 install --upgrade pip
# Install virtual env to localize dependencies
sudo pip3 install virtualenv
# change directory into folder where application is downloaded
cd Information-hub/
# Create a venv and activate it
virtualenv venv
source venv/bin/activate
# Manually install Django
# Install requirements
pip install -r requirements.txt
pip install Django
pip install django-bootstrap3
# Start the server
python3 manage.py runserver 0:3000