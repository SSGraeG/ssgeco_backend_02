#!/bin/bash

var=$(ps -ef | grep 'python3 -u app.py' | grep -v 'grep')
pid=$(echo ${var} | cut -d " " -f2)
if [ -n "${pid}" ]
then
    kill -9 ${pid}
    echo "Process ${pid} is terminated."
else
    echo "Process is not running."
fi

# '/home/ubuntu/ssgbay' 디렉토리를 삭제하고 다시 만듭니다.
rm -rf /home/ubuntu/ssg_backend
mkdir /home/ubuntu/ssg_backend
