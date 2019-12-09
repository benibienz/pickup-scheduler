#!/bin/sh

# new week
curl "$FULL_REST_ADDR""/new" --request PUT

# Simple test for team size of 1
REST_ADDR=$(kubectl get service rest --output jsonpath='{.status.loadBalancer.ingress[0].ip}')
python rest-client.py --host="$REST_ADDR" --name="FM" --user="fm" --teamsize=1
python rest-client.py --host="$REST_ADDR" --name="Alice"
python rest-client.py --host="$REST_ADDR" --name="Bob"

printf "\n"
FULL_REST_ADDR="http://"""$REST_ADDR""":5000"
# check for game
curl "$FULL_REST_ADDR""/game/Monday-20"

# report win for team A
curl "$FULL_REST_ADDR""/report/Monday-20/A" --request PUT

# check game again
curl "$FULL_REST_ADDR""/game/Monday-20"

printf "\n"
# inspect player info - scores should have updated
curl "$FULL_REST_ADDR""/player/Alice"
curl "$FULL_REST_ADDR""/player/Bob"

# new week
curl "$FULL_REST_ADDR""/new" --request PUT

printf "\n"
# inspect player info - scores should remain
curl "$FULL_REST_ADDR""/player/Alice"
curl "$FULL_REST_ADDR""/player/Bob"