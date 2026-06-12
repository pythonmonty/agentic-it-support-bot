# Trading Platform Access

**Article ID:** KB-014

## Summary
Granting and troubleshooting access to the Trading Platform and its modules. Most access issues are missing entitlements rather than outages.

## Symptoms
- Cannot view client positions
- Trade approval / blotter screen missing
- Portfolio dashboard empty after login
- Market data panels blank
- "You do not have permission" within the platform

## Troubleshooting Steps
1. Confirm the user holds the Trading Platform role entitlement.
2. Check for module-level entitlements (blotter, approvals, market data) separately.
3. Verify a recent role change did not strip the entitlement.
4. Confirm market data subscription if data panels are blank (see Market Data Entitlement Requests).

## Resolution Steps
1. Assign the missing platform/module entitlement via the access workflow.
2. Refresh user permissions and re-sync the trading profile.
3. Validate the previously failing screen now loads.

## Escalation Guidance
Trading profile present but misconfigured -> Trading Application Support.

## Related Systems
- Trading Platform
- Identity Governance Platform
- Market Data Platform
