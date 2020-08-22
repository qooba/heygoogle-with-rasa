#!/bin/bash

#docker network create -d bridge gitlab

PROJECT_NAME='heygoogle'
MINIO_ACCESS_KEY='AKIAIOSFODNN7EXAMPLE'
MINIO_SECRET_KEY='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'

docker run -d --rm -p 80:80 -p 8022:22 -p 443:443 --name gitlab --network gitlab \
  --hostname gitlab \
  -v $(pwd)/gitlab/config:/etc/gitlab:Z \
  -v $(pwd)/gitlab/logs:/var/log/gitlab:Z \
  -v $(pwd)/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest

#docker run --rm --network gitlab -v /srv/gitlab-runner/config:/etc/gitlab-runner gitlab/gitlab-runner register \
#  --non-interactive \
#  --docker-network-mode gitlab \
#  --executor "docker" \
#  --docker-image ubuntu:latest \
#  --url "http://gitlab/" \
#  --registration-token "TWJABbyzkVWVAbJc9bSx" \
#  --description "docker-runner" \
#  --tag-list "docker,aws" \
#  --run-untagged="true" \
#  --locked="false" \
#  --access-level="not_protected"

docker run -d --rm --name gitlab-runner --network gitlab \
     -v /srv/gitlab-runner/config:/etc/gitlab-runner \
     -v /var/run/docker.sock:/var/run/docker.sock \
     gitlab/gitlab-runner:latest

docker run -d --rm -p 9000:9000 --network gitlab --name minio \
  -e "MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY" \
  -e "MINIO_SECRET_KEY=$MINIO_SECRET_KEY" \
  -v $(pwd)/minio/data:/data \
  minio/minio server /data

docker run --name redis -d --rm --network gitlab redis

docker run --name jupyter --network gitlab -d --rm -p 8888:8888 -v $(pwd)/src:/src -v $(pwd)/jupyter:/root/.jupyter -v $(pwd)/notebooks:/opt/notebooks qooba/heygoogle /bin/bash -c "jupyter lab --notebook-dir=/opt/notebooks --ip='0.0.0.0' --port=8888 --no-browser --allow-root --NotebookApp.password='' --NotebookApp.token=''"

docker run -d --rm --network gitlab --name nginx -p 8081:80 -v $(pwd)/nginx/conf:/etc/nginx/conf.d openresty/openresty:alpine

docker run --name heygoogle-en -d --rm --network gitlab \
  -e "PROJECT_NAME=$PROJECT_NAME" \
  -e "MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY" \
  -e "MINIO_SECRET_KEY=$MINIO_SECRET_KEY" \
  -e "INITIAL_MODEL_NAME=20200821-232043" \
  -e "WELCOME_TEXT=Hello ! Ask me a question" \
  -e "LANGUAGE=en" \
  -v $(pwd)/src:/app \
  qooba/rasa:1.10.10_app

docker run --name heygoogle-pl -d --rm --network gitlab \
  -e "PROJECT_NAME=$PROJECT_NAME" \
  -e "MINIO_ACCESS_KEY=$MINIO_ACCESS_KEY" \
  -e "MINIO_SECRET_KEY=$MINIO_SECRET_KEY" \
  -e "INITIAL_MODEL_NAME=20200821-232519" \
  -e "WELCOME_TEXT=Cześć ! Zadaj mi pytanie" \
  -e "LANGUAGE=pl" \
  -v $(pwd)/src:/app \
  qooba/rasa:1.10.10_app

ngrok http 8081
