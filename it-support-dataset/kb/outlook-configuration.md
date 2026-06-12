# Outlook Configuration

**Article ID:** KB-012

## Summary
Configuring and repairing the Outlook desktop profile.

## Symptoms
- Outlook stuck on "Loading profile" or keeps crashing
- Repeated password prompts in Outlook
- Mailbox shows "disconnected" or won't sync
- Search returns no results / folders missing

## Troubleshooting Steps
1. Confirm the issue is profile-specific (test via webmail).
2. Check for a corrupted local profile or oversized OST cache.
3. Verify credentials/SSO token are current.
4. Rule out an account lockout from a stale Outlook credential.

## Resolution Steps
1. Recreate the Outlook profile and rebuild the OST cache.
2. Re-authenticate with current corporate credentials.
3. Confirm mail sync and search work after rebuild.

## Escalation Guidance
Server-side mailbox errors -> Messaging/Exchange team.

## Related Systems
- Outlook
- Azure AD
- SSO
