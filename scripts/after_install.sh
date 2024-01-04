#!/bin/bash
cd /home/ubuntu/ssg_backend

log_file="/home/ubuntu/ssg_backend/app_log.txt"

touch "$log_file"

echo ">>> pip install"
pip install -r requirements.txt

echo ">>> remove template files "
rm -rf appspec.yml requirements.txt

echo ">>> change owner to ubuntu "
chown -R ubuntu /home/ubuntu/ssg_backend

sudo chown -R ubuntu:ubuntu /home/ubuntu/ssg_backend

echo ">>> start server ---------------------"
gunicorn --bind 0.0.0.0:5000 --timeout 90 app:app > /dev/null 2> /home/ubuntu/gunicorn.log </dev/null &