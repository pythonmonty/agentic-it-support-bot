# Suspicious Login Investigation Process

**Article ID:** KB-022

## Summary
Investigating risky or impossible-travel sign-ins flagged by identity protection.

## Symptoms
- "Unusual sign-in" alert
- Login from an unexpected country/IP
- Risk detection raised on the account

## Troubleshooting Steps
1. Review sign-in logs for location, device, and risk level.
2. Confirm with the user whether the activity was theirs.
3. Check whether MFA was satisfied on the flagged sign-in.

## Resolution Steps
1. If benign, dismiss the risk and document.
2. If suspicious, reset credentials, revoke sessions, re-enroll MFA.
3. Apply/verify conditional access controls.

## Escalation Guidance
Confirmed compromise -> Security Incident Escalation.

## Related Systems
- Azure AD
- Security
- Conditional Access
