# MFA Enrollment

**Article ID:** KB-002

## Summary
Steps for first-time multi-factor authentication enrollment using the authenticator app or hardware token.

## Symptoms
- "Action required: set up multi-factor authentication"
- Authenticator app not receiving push prompts
- Enrollment wizard fails or times out
- QR code will not scan during setup

## Troubleshooting Steps
1. Confirm the user is licensed for MFA in Azure AD.
2. Check that the enrollment session was started from a compliant device.
3. Verify the authenticator app is updated and time-sync is enabled.
4. Confirm the registration did not partially complete and leave a stale method.

## Resolution Steps
1. Remove any partial/stale MFA method, then re-run enrollment from aka.ms/mfasetup.
2. If push fails, register a phone or hardware token as the method instead.
3. Validate by forcing a re-authentication after enrollment completes.

## Escalation Guidance
If enrollment repeatedly fails for multiple users at once, raise a possible service incident to IAM.

## Related Systems
- MFA
- Azure AD
- SSO
