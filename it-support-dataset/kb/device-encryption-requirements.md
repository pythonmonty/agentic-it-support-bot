# Device Encryption Requirements

**Article ID:** KB-020

## Summary
All endpoints must have full-disk encryption; non-compliant devices are blocked from corporate resources.

## Symptoms
- Device blocked as "non-compliant"
- "Encryption required" notification
- Conditional access denies sign-in from the laptop

## Troubleshooting Steps
1. Check encryption status in Endpoint Management.
2. Confirm the recovery key escrowed successfully.
3. Verify the compliance policy evaluated after encryption.

## Resolution Steps
1. Enable/repair full-disk encryption and escrow the recovery key.
2. Force a compliance re-evaluation.
3. Confirm the device is compliant and access is restored.

## Escalation Guidance
Encryption fails on hardware -> Endpoint Engineering.

## Related Systems
- Endpoint Management
- Security
- Conditional Access
