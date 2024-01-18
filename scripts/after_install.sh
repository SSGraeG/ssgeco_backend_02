#!/bin/bash
LOGFILE=/home/ubuntu/gunicorn.log

cd /home/ubuntu/ssg_backend || exit

echo ">>> pip install"
pip install -r requirements.txt

echo ">>> remove template files "
rm -rf appspec.yml requirements.txt

echo ">>> change owner to ubuntu "
chown -R ubuntu /home/ubuntu/ssg_backend

sudo chown -R ubuntu:ubuntu /home/ubuntu/ssg_backend

echo ">>> start server ---------------------"
gunicorn --bind 0.0.0.0:5000 --timeout 90 "app:create_app()" >> "$LOGFILE" 2>&1 &

