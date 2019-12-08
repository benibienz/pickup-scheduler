# PlayMaker
Pickup sport scheduling on the Cloud

## How to run

1) Launch everything with `sh launch.sh`
2) Run `kubectl get service` to list services and view the external IP of the REST server
3) Run `kubectl get pods` to list pods and view the name of the logs pod
4) To see logs `kubectl logs <name of logs pod>`
4) To add worker `kubectl scale --current-replicas=1 --replicas=2 deployment/worker`