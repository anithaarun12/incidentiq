# DNS Resolution Failure

## Symptoms

* Service discovery failures
* Application unable to reach dependencies
* Hostname resolution errors

## Root Cause

DNS server outage or incorrect DNS configuration.

## Investigation Steps

1. Verify DNS server status
2. Test hostname resolution
3. Review network configuration

## Resolution

1. Restart DNS service
2. Update DNS configuration
3. Switch to backup DNS servers

## Commands

nslookup service.example.com
dig service.example.com
systemctl status named

## Prevention

* Configure redundant DNS servers
* Monitor DNS latency
* Regular DNS health checks
