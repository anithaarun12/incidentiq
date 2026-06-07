# Database Connection Pool Exhausted

## Symptoms

* Database timeout errors
* Slow application response
* Connection refused messages
* Increased request failures

## Root Cause

Application consumed all available database connections.

## Investigation Steps

1. Check active database connections
2. Review application logs
3. Analyze connection pool metrics

## Resolution

1. Increase connection pool size
2. Close idle connections
3. Restart application services
4. Optimize long-running queries

## Commands

SELECT count(*) FROM pg_stat_activity;
SHOW max_connections;

## Prevention

* Implement connection pooling
* Configure idle timeout
* Monitor pool utilization
