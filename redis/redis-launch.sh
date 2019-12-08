#!/bin/sh

docker pull redis:5.0.7
kubectl create deployment redis --image redis:5.0.7
kubectl expose deployment redis --port 6379 --target-port 6379