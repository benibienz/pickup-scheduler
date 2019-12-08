#!/bin/sh
PROJECT_NAME="labs-254501"
#gcloud config set project $PROJECT_NAME
#gcloud config set compute/zone us-west1-b
#gcloud container clusters create --preemptible playmaker

#sh redis/redis-launch.sh
#sh rabbitmq/rabbitmq-launch.sh
#sh rest/rest-launch.sh
sh scheduler/scheduler-launch.sh
#sh logs/logs-launch.sh