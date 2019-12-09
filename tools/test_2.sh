#!/bin/sh

# new week
curl "$FULL_REST_ADDR""/new" --request PUT

# ranking test for team size of 2
REST_ADDR=$(kubectl get service rest --output jsonpath='{.status.loadBalancer.ingress[0].ip}')
python rest-client.py --host="$REST_ADDR" --name="FM" --user="fm" --teamsize=2
python rest-client.py --host="$REST_ADDR" --name="Alice"
python rest-client.py --host="$REST_ADDR" --name="Bob"
python rest-client.py --host="$REST_ADDR" --name="Colin"
python rest-client.py --host="$REST_ADDR" --name="David"

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
curl "$FULL_REST_ADDR""/player/Colin"
curl "$FULL_REST_ADDR""/player/David"

# new week
curl "$FULL_REST_ADDR""/new" --request PUT

printf "\n"
# inspect player info - scores should remain
curl "$FULL_REST_ADDR""/player/Alice"
curl "$FULL_REST_ADDR""/player/Bob"
curl "$FULL_REST_ADDR""/player/Colin"
curl "$FULL_REST_ADDR""/player/David"

printf "\n"
python rest-client.py --host="$REST_ADDR" --name="FM" --user="fm" --teamsize=2
python rest-client.py --host="$REST_ADDR" --name="Alice"
python rest-client.py --host="$REST_ADDR" --name="Bob"
python rest-client.py --host="$REST_ADDR" --name="Colin"
python rest-client.py --host="$REST_ADDR" --name="David"

# check for game - teams should be different, with the winners
# from last time separated
curl "$FULL_REST_ADDR""/game/Monday-20"