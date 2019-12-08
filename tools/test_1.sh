#!/bin/sh

# Simple test for team size of 2
REST_ADDR=$(kubectl get service rest --output jsonpath='{.status.loadBalancer.ingress[0].ip}')
python rest-client.py --host="$REST_ADDR" --name="FM" --user="fm"
python rest-client.py --host="$REST_ADDR" --name="onetime"
python rest-client.py --host="$REST_ADDR" --name="twotimes"