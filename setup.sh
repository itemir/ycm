#!/bin/bash
sudo apt install build-essential python3-dev libpq-dev virtualenv -y
python=$(which python3)
virtualenv -p $python venv
source venv/bin/activate
pip install -r requirements.txt
