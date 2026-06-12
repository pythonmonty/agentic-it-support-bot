# VPN Certificate Renewal

**Article ID:** KB-009

## Summary
Renewing the device/user certificate the VPN uses for authentication. Certificates are valid 12 months and a lapse blocks all VPN logins.

## Symptoms
- VPN suddenly stops connecting with a certificate or authentication error
- "Certificate expired" / "server certificate is not valid"
- Was working yesterday, fails today
- Multiple users on the same renewal cohort fail together

## Troubleshooting Steps
1. Check the VPN certificate validity dates in the device certificate store.
2. Confirm whether a fleet-wide certificate batch expired (common cause of spikes).
3. Verify the device is compliant so it can receive a renewed certificate.

## Resolution Steps
1. Trigger certificate renewal/re-enrollment from Endpoint Management.
2. Re-deploy the renewed certificate to the device and restart the VPN client.
3. Confirm a successful VPN connection.

## Escalation Guidance
If a large batch expired simultaneously, declare an incident and notify Network/IAM teams.

## Related Systems
- VPN
- Endpoint Management
- Certificate Authority
