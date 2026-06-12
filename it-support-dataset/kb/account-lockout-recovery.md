# Account Lockout Recovery

**Article ID:** KB-004

## Summary
Resolving repeated account lockouts and restoring sign-in.

## Symptoms
- "Your account is locked" message
- Locks again shortly after being unlocked
- Multiple failed sign-ins from old devices or mapped drives

## Troubleshooting Steps
1. Identify lockout source via sign-in logs (often a stale cached credential on a phone or service).
2. Check for an expired password driving repeated failures.
3. Look for mapped network drives or Outlook profiles using old credentials.

## Resolution Steps
1. Unlock the account and clear the offending cached credential.
2. If password expired, follow Password Reset Procedure.
3. Confirm no further lockouts over the next hour.

## Escalation Guidance
Persistent re-lockouts with unknown source -> Security for brute-force review.

## Related Systems
- Azure AD
- SSO
- Core Banking Portal
