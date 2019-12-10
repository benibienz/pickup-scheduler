# PlayMaker
Pickup sport scheduling on the Cloud

## About

### The Problem
Successful pickup games currently rely on volunteers taking the initiative to organize a time, find people and book the facility. Thus the number of pickup games available in a local area is constrained by the number of willing organizers and their personal time availability, resulting in empty facilities and people who want to play sitting at home. The games that are arranged often suffer problems such as inconsistent numbers of people turning up and unbalanced teams.

### The Solution
PlayMaker seeks to tackle these problems by providing a scheduling service with the following characteristics:
* Two user types: Player and Facility Manager (FM).
FMs can upload and update a calendar of available timeslots for each of their facilities to the REST server. Each timeslot has a price associated with it.
* Players can upload a calendar of their availability and max prices they are willing to pay to the REST server.
* The Game Scheduler (GS) compares Player availability and facility timeslots. It will attempt to fill timeslots on a first-come first-served basis, organizing Players into two teams. Players can query the REST server to get upcoming game timeslots and team rosters.
* After the game is played, someone reports the outcome of the game to the REST server, which passes it to the GS. The GS assigns points to the players on each team depending on match outcome (3 for a win, 1 for a tie, 0 for a loss). These points are used to help assign balanced teams in future.
* The system has the potential to scale in complexity (e.g. location-based matching, preferred teammates, dynamic pricing and team sizing, Google Calendar integration etc.).


## How to run

1) Launch everything with `sh launch.sh`
2) Run `kubectl get service` to list services and view the external IP of the REST server
3) Run `kubectl get pods` to list pods and view the name of the logs pod
4) To see logs `kubectl logs <name of logs pod>`
4) To add scheduler `kubectl scale --current-replicas=1 --replicas=2 deployment/scheduler`

## Databases
There are three Redis DBs:

1) `gamesdb` hosts game info. Keys contain day and timeslot info (e.g. `Monday-20`) and values are dicts of the following format: `{'team A': <team list>, 'team B': <team list>, 'result' <'A', 'B', 'tie' or None if not played yet>}`
2) `facilitiesdb` stores facility calendars. Keys are Facility names and values are `FacilityCalendar` objects
3) `playersdb` stores player info. Keys are Player names and values are dicts of the following format: `{'calendar': <DataFrame of player calendar>, 'games': <List of game dates>, 'score': <player score for ranking>}, `