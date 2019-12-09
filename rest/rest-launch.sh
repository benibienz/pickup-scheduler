#!/bin/sh

docker build -t gcr.io/labs-254501/rest-server:v6 ./rest
docker push gcr.io/labs-254501/rest-server:v6

kubectl create deployment rest --image gcr.io/labs-254501/rest-server:v6
kubectl expose deployment rest --type LoadBalancer --port 5000 --target-port 5000