#!/bin/sh

# ranking test for team size of 2
REST_ADDR=$(kubectl get service rest --output jsonpath='{.status.loadBalancer.ingress[0].ip}')
python rest-client.py --host="$REST_ADDR" --name="FM" --user="fm" --teamsize=2
python rest-client.py --host="$REST_ADDR" --name="Alice"
python rest-client.py --host="$REST_ADDR" --name="Bob"
python rest-client.py --host="$REST_ADDR" --name="Colin"
python rest-client.py --host="$REST_ADDR" --name="David"


FULL_REST_ADDR="http://"""$REST_ADDR""":5000"
printf "\nCheck for game:\n"
curl "$FULL_REST_ADDR""/game/Monday-20"

printf "\nReport win for team A:\n"
curl "$FULL_REST_ADDR""/report/Monday-20/A" --request PUT

printf "\nCheck game again:\n"
curl "$FULL_REST_ADDR""/game/Monday-20"

printf "\nInspect player info - scores should have updated:\n"
curl "$FULL_REST_ADDR""/player/Alice"
curl "$FULL_REST_ADDR""/player/Bob"
curl "$FULL_REST_ADDR""/player/Colin"
curl "$FULL_REST_ADDR""/player/David"

printf "\nNew week\n"
curl "$FULL_REST_ADDR""/new" --request PUT

printf "\nInspect player info - scores should remain:\n"
curl "$FULL_REST_ADDR""/player/Alice"
curl "$FULL_REST_ADDR""/player/Bob"
curl "$FULL_REST_ADDR""/player/Colin"
curl "$FULL_REST_ADDR""/player/David"

printf "\nInput calendars again\n"
python rest-client.py --host="$REST_ADDR" --name="FM" --user="fm" --teamsize=2
python rest-client.py --host="$REST_ADDR" --name="Alice"
python rest-client.py --host="$REST_ADDR" --name="Bob"
python rest-client.py --host="$REST_ADDR" --name="Colin"
python rest-client.py --host="$REST_ADDR" --name="David"

printf "\nCheck for game - teams should be different, with the winners from last time separated:\n"
curl "$FULL_REST_ADDR""/game/Monday-20"