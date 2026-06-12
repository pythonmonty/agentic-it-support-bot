# Remote Access Troubleshooting

**Article ID:** KB-011

## Summary
End-to-end remote access checks when an employee cannot work off-site.

## Symptoms
- Cannot reach internal apps from home
- Blocked from a personal/unmanaged device
- Access works in office but not remotely

## Troubleshooting Steps
1. Confirm VPN session is healthy (certificate + compliance).
2. Check whether a conditional access policy blocks the location or device.
3. Verify the application is reachable for in-office users (to isolate scope).

## Resolution Steps
1. Remediate VPN/certificate/compliance as needed.
2. Adjust or satisfy the conditional access requirement.
3. Validate remote access to the affected application.

## Escalation Guidance
Policy-level blocks -> Security (Conditional Access).

## Related Systems
- VPN
- Conditional Access
- Endpoint Management
