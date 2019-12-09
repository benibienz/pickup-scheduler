# PlayMaker
Pickup sport scheduling on the Cloud

## How to run

1) Launch everything with `sh launch.sh`
2) Run `kubectl get service` to list services and view the external IP of the REST server
3) Run `kubectl get pods` to list pods and view the name of the logs pod
4) To see logs `kubectl logs <name of logs pod>`
4) To add scheduler `kubectl scale --current-replicas=1 --replicas=2 deployment/scheduler`

## About

## Databases
There are three Redis DBs:

1) `gamesdb` hosts game info. Keys contain day and timeslot info (e.g. `Monday-20`) and values are dicts of the following format: `{'team A': <team list>, 'team B': <team list>, 'result' <'A', 'B', 'tie' or None if not played yet>}`
2) `facilitiesdb` stores facility calendars. Keys are Facility names and values are `FacilityCalendar` objects
3) `playersdb` stores player info. Keys are Player names and values are dicts of the following format: `{'calendar': <DataFrame of player calendar>, 'games': <List of game dates>, 'score': <player score for ranking>}, `