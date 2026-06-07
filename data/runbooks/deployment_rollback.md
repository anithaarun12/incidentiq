# Deployment Rollback

## Symptoms

* Errors immediately after deployment
* Increased failure rates
* Performance degradation

## Root Cause

Defective application release.

## Investigation Steps

1. Compare current and previous versions
2. Review deployment logs
3. Validate release notes

## Resolution

1. Roll back deployment
2. Verify service health
3. Notify stakeholders

## Commands

kubectl rollout undo deployment <deployment-name>
kubectl rollout history deployment <deployment-name>

## Prevention

* Canary deployments
* Blue-green deployments
* Automated testing
