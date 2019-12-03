#!/bin/sh

docker pull redis
kubectl create deployment redis --image redis
kubectl expose deployment redis --port 6379 --target-port 6379