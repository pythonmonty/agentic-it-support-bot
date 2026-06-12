# VPN Setup

**Article ID:** KB-008

## Summary
First-time VPN client installation and profile configuration for remote access.

## Symptoms
- VPN client not installed
- No corporate VPN profile available
- Client installed but no connection entry

## Troubleshooting Steps
1. Confirm the device is enrolled and compliant in Endpoint Management.
2. Verify the VPN client version matches the current standard.
3. Ensure the user has the remote-access entitlement.

## Resolution Steps
1. Push the VPN client and profile from Endpoint Management.
2. User signs in with corporate credentials and completes MFA.
3. Validate connectivity to an internal resource.

## Escalation Guidance
Profile pushes but authentication fails -> see VPN Troubleshooting / VPN Certificate Renewal.

## Related Systems
- VPN
- Endpoint Management
- Azure AD
