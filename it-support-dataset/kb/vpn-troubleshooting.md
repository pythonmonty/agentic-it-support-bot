# VPN Troubleshooting

**Article ID:** KB-010

## Summary
General VPN connectivity diagnosis after setup is complete.

## Symptoms
- Connects then drops repeatedly
- Authentication succeeds but no internal access
- Slow or timing-out tunnel

## Troubleshooting Steps
1. Rule out an expired certificate first (see VPN Certificate Renewal).
2. Check device compliance state; non-compliant devices are blocked.
3. Validate local network/DNS is functioning.
4. Confirm the VPN client config/profile is the current version.

## Resolution Steps
1. Reset the VPN profile or re-import the current configuration.
2. Remediate device compliance if blocked.
3. Confirm stable connectivity to internal resources.

## Escalation Guidance
Region-wide connectivity loss -> Network operations.

## Related Systems
- VPN
- Endpoint Management
- Corporate WiFi
