# MFA Recovery

**Article ID:** KB-003

## Summary
How to recover access when an employee loses their MFA device or is locked out of authentication.

## Symptoms
- Lost or replaced phone with the authenticator app
- No longer receiving verification prompts
- "We could not verify your identity" at sign-in

## Troubleshooting Steps
1. Verify identity through the service desk callback procedure.
2. Confirm whether a backup method (phone/token) is registered.
3. Check for tenant-wide MFA outages before treating as individual.

## Resolution Steps
1. IAM removes the lost method and issues a temporary access pass.
2. User re-enrolls a new method via MFA Enrollment.
3. Temporary access pass is revoked once enrollment is confirmed.

## Escalation Guidance
Suspected account compromise during recovery must go to Security per Suspicious Login Investigation Process.

## Related Systems
- MFA
- Azure AD
