#!/bin/sh

sudo apt-get upgrade && apt-get install -y python-pip
sudo pip install --upgrade google-cloud google-api-python-client google-auth-httplib2
sudo pip install --upgrade google-cloud
sudo pip install paramiko


echo "export GOOGLE_APPLICATION_CREDENTIALS=~/apikey.json" > ~/.bash_profile
bash

