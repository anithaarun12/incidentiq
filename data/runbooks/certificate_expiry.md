# SSL Certificate Expiry

## Symptoms

* HTTPS connection failures
* Browser security warnings
* SSL handshake errors

## Root Cause

TLS/SSL certificate expired.

## Investigation Steps

1. Verify certificate expiration date
2. Check certificate chain
3. Review SSL logs

## Resolution

1. Renew certificate
2. Deploy updated certificate
3. Restart web server

## Commands

openssl x509 -enddate -noout -in cert.pem
openssl s_client -connect domain.com:443

## Prevention

* Automated certificate renewal
* Expiry alerts before 30 days
* Certificate inventory management
