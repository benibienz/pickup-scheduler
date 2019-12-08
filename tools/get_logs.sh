#!/bin/sh

GSPOD=$(kubectl get pod -l app=scheduler -o jsonpath="{.items[0].metadata.name}")
kubectl logs $GSPOD -f
