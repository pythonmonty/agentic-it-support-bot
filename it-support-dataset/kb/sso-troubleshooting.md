# SSO Troubleshooting

**Article ID:** KB-005

## Summary
Diagnosing single sign-on failures across federated banking applications.

## Symptoms
- Login page reloads in a loop
- "Token expired" or "AADSTS" errors
- Works in one app but not another
- Prompted to sign in repeatedly

## Troubleshooting Steps
1. Confirm conditional access is not blocking the device (see Conditional Access).
2. Clear browser cache/cookies for the identity provider domain.
3. Verify device compliance state in Endpoint Management.
4. Check workstation time sync.

## Resolution Steps
1. Re-establish the SSO session after clearing tokens.
2. If a conditional access policy blocked access, remediate device compliance.
3. Confirm access to the previously failing application.

## Escalation Guidance
Federation/metadata errors affecting an entire app -> Identity and Access Management.

## Related Systems
- SSO
- Azure AD
- Outlook
- Trading Platform
