#!/bin/bash
LOGFILE=/home/ubuntu/gunicorn.log
ACCESS_LOGFILE=/home/ubuntu/access.log  # 추가된 부분
ERROR_LOGFILE=/home/ubuntu/error.log    # 추가된 부분

cd /home/ubuntu/ssg_backend || exit

echo ">>> pip install"
pip install -r requirements.txt

echo ">>> remove template files"
rm -rf appspec.yml requirements.txt

echo ">>> change owner to ubuntu"
chown -R ubuntu /home/ubuntu/ssg_backend

sudo chown -R ubuntu:ubuntu /home/ubuntu/ssg_backend

echo ">>> start server ---------------------"
gunicorn --bind 0.0.0.0:5000 --timeout 90 "app:create_app()" \
    --access-logfile "$ACCESS_LOGFILE" \
    --error-logfile "$ERROR_LOGFILE" \
    --log-level debug \
    >> "$LOGFILE" 2>&1 &  # 기존의 로그 파일에도 로그를 출력하도록 수정
