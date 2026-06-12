# Market Data Entitlement Requests

**Article ID:** KB-016

## Summary
Requesting exchange/vendor market-data entitlements. Lapsed vendor entitlements blank out live data.

## Symptoms
- Live quotes not updating / showing stale or blank
- "Entitlement required" on a data feed
- Charts load but prices are missing
- Several traders lose the same feed at once

## Troubleshooting Steps
1. Identify the specific feed/exchange affected.
2. Check whether the vendor entitlement batch lapsed (common cause of spikes).
3. Confirm the user's desk is mapped to the required entitlement.

## Resolution Steps
1. Submit/restore the market data entitlement for the user or desk.
2. Re-sync the feed and confirm live updates.
3. Validate quotes and charts populate.

## Escalation Guidance
Feed-wide outage affecting many users -> Market Data vendor management + incident.

## Related Systems
- Market Data Platform
- Trading Platform
