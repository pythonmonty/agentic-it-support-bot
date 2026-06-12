# Privileged Access Request Process

**Article ID:** KB-007

## Summary
Requesting, approving, and activating just-in-time privileged access.

## Symptoms
- Cannot perform admin action despite being "approved"
- Privileged session ends unexpectedly
- "Elevation required" prompts

## Troubleshooting Steps
1. Confirm the PAM request was approved AND activated (JIT is time-boxed).
2. Check the activation window has not expired.
3. Verify MFA was satisfied during elevation.

## Resolution Steps
1. Re-activate the approved role for the required window in PAM.
2. Complete MFA challenge to start the privileged session.
3. Confirm the admin action now succeeds.

## Escalation Guidance
Approval stuck or role missing from catalog -> Privileged Access Management team.

## Related Systems
- Privileged Access Management
- Identity Governance Platform
