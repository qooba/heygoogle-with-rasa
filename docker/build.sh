#!/bin/bash
#cp -r ../src .
docker build -t qooba/rasa:1.10.10 .
docker build -t qooba/rasa:1.10.10_app -f Dockerfile.app .
#rm -rf ./src
