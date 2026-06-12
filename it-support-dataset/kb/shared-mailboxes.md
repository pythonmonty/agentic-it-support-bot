# Shared Mailboxes

**Article ID:** KB-013

## Summary
Requesting and accessing shared/departmental mailboxes.

## Symptoms
- Shared mailbox not visible after being "added"
- Cannot send-as the shared address
- Shared mailbox disappeared after a role change

## Troubleshooting Steps
1. Confirm the security group granting access includes the user.
2. Check provisioning delay (can take a few hours to appear).
3. Verify send-as vs send-on-behalf permissions.

## Resolution Steps
1. Add the user to the mailbox access group.
2. Re-add the mailbox in Outlook after permissions propagate.
3. Validate read and send-as as required.

## Escalation Guidance
Permissions correct but still hidden -> Messaging team.

## Related Systems
- Outlook
- Azure AD
