# API Rate Limit Exceeded

## Symptoms

* HTTP 429 responses
* Client request failures
* Increased retry traffic

## Root Cause

Application exceeded API provider request limits.

## Investigation Steps

1. Review API usage metrics
2. Check rate-limit headers
3. Identify traffic spikes

## Resolution

1. Reduce request frequency
2. Implement request batching
3. Upgrade API plan
4. Introduce caching

## Commands

curl -I https://api.example.com

## Prevention

* Request throttling
* Caching layer
* API usage monitoring
