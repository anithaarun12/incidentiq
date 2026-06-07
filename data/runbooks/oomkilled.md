# OOMKilled Kubernetes Pod

## Symptoms

* Pod repeatedly restarting
* Status shows OOMKilled
* Increased application latency
* Frequent container crashes

## Root Cause

The container exceeded its allocated memory limit and Kubernetes terminated the process.

## Investigation Steps

1. Check pod status:
   kubectl get pods

2. Describe pod:
   kubectl describe pod <pod-name>

3. Review memory usage:
   kubectl top pod <pod-name>

## Resolution

1. Increase memory requests and limits
2. Optimize application memory usage
3. Restart deployment

## Commands

kubectl top pod <pod-name>
kubectl describe pod <pod-name>
kubectl rollout restart deployment <deployment-name>

## Prevention

* Configure Horizontal Pod Autoscaler
* Enable memory monitoring alerts
* Perform load testing before releases
