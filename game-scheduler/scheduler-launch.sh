#!/bin/sh

docker build -t gcr.io/labs-254501/game-scheduler:v1 ./game-scheduler
docker push gcr.io/labs-254501/game-scheduler:v1

kubectl create deployment game-scheduler --image gcr.io/labs-254501/game-scheduler:v1