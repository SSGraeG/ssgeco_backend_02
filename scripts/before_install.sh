#!/bin/bash

# 이전에 실행된 gunicorn 프로세스를 중지합니다.
GUNICORN_PID=$(pgrep -f 'gunicorn --bind 0.0.0.0:5000')
if [ ! -z "$GUNICORN_PID" ]; then
    echo "Gunicorn 프로세스 종료: PID $GUNICORN_PID"
    kill $GUNICORN_PID
else
    echo "실행 중인 Gunicorn 프로세스가 없습니다."
fi

# 로그 파일과 프로젝트 디렉터리를 초기화합니다.
rm -rf /home/ubuntu/gunicorn.log
rm -rf /home/ubuntu/ssg_backend
mkdir /home/ubuntu/ssg_backend

cd /home/ubuntu/ssg_backend