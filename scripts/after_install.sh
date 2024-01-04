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

echo ">>> start app.py"
nohup python3 -u app.py >> "$log_file" 2>&1 &
echo ">>> app.py started."