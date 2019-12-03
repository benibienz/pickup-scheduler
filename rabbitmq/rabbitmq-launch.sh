#!/bin/sh

docker pull rabbitmq
kubectl create deployment rabbitmq --image rabbitmq
kubectl expose deployment rabbitmq --port 5672 --target-port 5672