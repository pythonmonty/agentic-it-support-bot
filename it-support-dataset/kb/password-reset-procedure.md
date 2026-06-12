# Password Reset Procedure

**Article ID:** KB-001

## Summary
How employees reset an expired or forgotten corporate password and restore access to SSO-protected applications.

## Symptoms
- "Your password has expired" prompt at login
- Cannot sign in to SSO even with the correct password
- Repeated authentication failures after a recent password change
- Applications loop back to the login page

## Troubleshooting Steps
1. Confirm the account is not locked (see Account Lockout Recovery).
2. Verify the employee is using the corporate password, not a cached local one.
3. Check the password age in Azure AD; corporate policy expires passwords every 90 days.
4. Ensure the workstation clock is correct, as skew can break SSO tokens.

## Resolution Steps
1. Direct the user to the self-service password reset portal and complete identity verification.
2. If self-service fails, IAM resets the password and forces a change at next logon.
3. Have the user sign out of all sessions and sign back in to refresh SSO tokens.

## Escalation Guidance
If reset succeeds but SSO still fails, escalate to Identity and Access Management for token/federation review.

## Related Systems
- Azure AD
- SSO
- Core Banking Portal
