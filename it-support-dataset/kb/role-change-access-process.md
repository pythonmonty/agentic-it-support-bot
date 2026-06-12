# Role Change Access Process

**Article ID:** KB-006

## Summary
How access is recalculated when an employee changes role, and why old or new entitlements may be missing.

## Symptoms
- Lost access to applications after a transfer or promotion
- New application is visible but returns empty data
- "Not authorized" after a role change
- Some tools work, others do not

## Troubleshooting Steps
1. Compare current entitlements against the target role profile in the Identity Governance Platform.
2. Identify entitlements that were removed with the old role but not re-granted.
3. Check whether provisioning has fully synchronized (can lag 24h).

## Resolution Steps
1. Submit the missing entitlement(s) via the access request workflow.
2. Re-run provisioning sync; confirm the role profile is applied.
3. Validate access to each affected application.

## Escalation Guidance
Entitlement exists but app still denies -> the owning application team (e.g., Trading Platform Access).

## Related Systems
- Identity Governance Platform
- Azure AD
- Trading Platform
- Portfolio Management System
