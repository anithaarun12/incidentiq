# Slow Database Queries

## Symptoms

* Increased API latency
* Database CPU spikes
* Long query execution times

## Root Cause

Missing indexes, inefficient joins, or large table scans.

## Investigation Steps

1. Review slow query logs
2. Analyze query plans
3. Check index usage

## Resolution

1. Add indexes
2. Rewrite inefficient queries
3. Archive old data
4. Tune database configuration

## Commands

EXPLAIN ANALYZE <query>;
SHOW INDEXES;

## Prevention

* Query performance monitoring
* Regular index review
* Database optimization audits
