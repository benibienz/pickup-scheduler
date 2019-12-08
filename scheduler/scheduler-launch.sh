#!/bin/sh

docker build -t gcr.io/labs-254501/scheduler:v16 ./scheduler
docker push gcr.io/labs-254501/scheduler:v16

kubectl create deployment scheduler --image gcr.io/labs-254501/scheduler:v16