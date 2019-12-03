#!/bin/sh

docker build -t gcr.io/labs-254501/logs:v2 ./logs
docker push gcr.io/labs-254501/logs:v2

kubectl create deployment logs --image gcr.io/labs-254501/logs:v2