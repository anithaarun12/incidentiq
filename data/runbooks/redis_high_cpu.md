# Redis High CPU Usage

## Symptoms

* Increased response times
* Elevated CPU utilization
* Cache request latency

## Root Cause

Expensive Redis commands or excessive traffic.

## Investigation Steps

1. Check Redis metrics
2. Identify slow commands
3. Review client connections

## Resolution

1. Optimize queries
2. Increase Redis resources
3. Scale Redis cluster
4. Remove expensive operations

## Commands

redis-cli info cpu
redis-cli slowlog get
redis-cli info clients

## Prevention

* Monitor slow logs
* Use Redis clustering
* Implement rate limiting
