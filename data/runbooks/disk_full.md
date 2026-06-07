# Disk Full

## Symptoms

* Write failures
* Application crashes
* Database unable to write logs
* System alerts indicating low storage

## Root Cause

Available disk space reached critical threshold.

## Investigation Steps

1. Check filesystem utilization
2. Identify large files
3. Review log growth

## Resolution

1. Remove temporary files
2. Archive old logs
3. Expand storage volume
4. Restart affected services

## Commands

df -h
du -sh /*
find /var/log -type f -size +100M

## Prevention

* Configure log rotation
* Set storage alerts
* Periodic cleanup jobs
