# IT Support Dataset Generation Prompt

You are generating data for an internal IT support environment used to evaluate a conversational
AI system that can answer questions using both:

1. Structured support ticket data stored in a relational database.
2. Unstructured knowledge base articles stored as markdown files.

The goal is not to create random tickets.

The goal is to create realistic relationships between tickets and knowledge base articles so that
some user questions require combining information from both sources.

---

## Environment

The organization is a medium-sized private bank with approximately 6000 employees worldwide.

The dataset represents internal IT support operations for bank employees. Users include:

- Relationship managers
- Traders
- Investment advisors
- Compliance officers
- Financial analysts
- Operations staff
- Risk-management specialists
- Back-office personnel
- Software engineers
- Executives

The IT support organization manages employee access, security controls, endpoint devices,
collaboration tools, internal applications, and banking systems.

The dataset should model realistic operational issues encountered within a highly regulated
financial institution.

---

## Ticket Schema

Generate ticket records using the following schema:

```json
{
  "ticket_id": "T-1001",
  "created_at": "2025-03-14T09:15:00",
  "requester_user": "j.smith",
  "department": "Private Banking",
  "language": "en",

  "category": "access",
  "product": "Trading Platform",

  "priority": "high",
  "impact_level": "single_user",
  "application_criticality": "high",

  "subject": "Unable to access portfolio dashboard",
  "description": "User reports that the portfolio dashboard is unavailable after a recent role change.",

  "status": "resolved",

  "root_cause": "Required entitlement not assigned",
  "resolution": "Assigned missing portfolio access role and refreshed user permissions.",

  "resolution_time_hours": 4.5,

  "assigned_team": "Identity and Access Management",

  "tags": [
    "access",
    "entitlement",
    "portfolio"
  ]
}
```

---

## Departments

Private Banking
Investment Advisory
Trading
Operations
Compliance
Risk Management
Technology
Finance
Executive Office
Human Resources

---

## Categories

Use only:

- access
- hardware
- software
- network
- account
- security

---

## Products

Use:

VPN
MFA
SSO
Outlook
Microsoft Teams
Jira
Azure AD
Corporate WiFi
Endpoint Management
Trading Platform
Portfolio Management System
Client Reporting Portal
Market Data Platform
Core Banking Portal
Document Management System
Identity Governance Platform
Privileged Access Management

---

## Priorities

Use:

- low
- medium
- high
- critical

---

## Impact Levels

Use:

- single_user
- team
- department
- company_wide

---

## Application Criticality

- low
- medium
- high
- regulatory

---

## Language Requirements

All ticket data and knowledge base articles must be written in English. Use realistic employee
language, abbreviations, typos, and imperfect descriptions. Do not generate multilingual content.
The schema includes a language field for future extensibility but all generated records should
use "en".

---

## Important Requirements

- Generate approximately 150 tickets.
- The tickets must not be independent.
- Most tickets should describe symptoms rather than root causes.
- The relationship between a ticket and its root cause should often only become clear through the
  resolution field.
- At least 30-40% of user questions should require combining information from both historical
  tickets and knowledge base articles.
- Create recurring operational patterns where multiple tickets share the same root cause. At least
  five root causes should appear repeatedly across 8-15 tickets each. Examples include:
  - Missing entitlement
  - Expired VPN certificate
  - Failed MFA enrollment
  - Outlook profile corruption
  - Trading profile misconfiguration

## Recurring Root Cause Themes

Generate recurring incidents around:

Identity & Access:

- Missing entitlement
- Incorrect role assignment
- Delayed access provisioning
- Expired password
- Failed MFA enrollment
- Inactive account

Remote Access:

- Expired VPN certificate
- VPN client misconfiguration
- Device compliance failure

Security:

- Endpoint encryption non-compliance
- Suspicious login investigation
- Certificate trust issue
- Conditional access policy failure

Banking Systems:

- Missing market data entitlement
- Trading profile misconfiguration
- Portfolio access role missing
- Client reporting permissions not assigned

Infrastructure:

- DNS resolution failure
- WiFi authentication issue
- Outlook profile corruption

---

## Ticket Distribution

Identity & Access Management:
40 tickets

VPN & Remote Access:
25 tickets

Banking Applications:
35 tickets

Email & Collaboration:
20 tickets

Security:
20 tickets

Infrastructure & Endpoints:
10 tickets

---

## Temporal Incident Patterns

Generate 3-5 incident waves during the 12-month period.

Each wave should represent a recurring operational issue that causes multiple related tickets over
a short timeframe.

Examples:

March 2025:

- Expired VPN certificate causes 10-15 VPN-related tickets over two weeks.

June 2025:

- Failed MFA enrollment process causes 8-12 authentication tickets.

September 2025:

- Market Data entitlement issue causes 8-10 trading application tickets.

These incidents should create realistic spikes that enable questions such as:

- Did VPN issues increase during a specific period?
- Were there recurring authentication incidents?
- Which problems caused the largest operational impact?

---

## Knowledge Base Articles

Generate 15-20 markdown articles.

Each article should contain:

- Title
- Summary
- Symptoms
- Troubleshooting steps
- Resolution steps
- Escalation guidance
- Related systems

---

## Required Knowledge Base Topics

Identity and access:

- Password Reset Procedure
- MFA Enrollment
- MFA Recovery
- Account Lockout Recovery
- SSO Troubleshooting
- Role Change Access Process
- Privileged Access Request Process

Remote access:

- VPN Setup
- VPN Certificate Renewal
- Remote Access Troubleshooting

VPN:

- VPN Setup
- VPN Certificate Renewal
- VPN Troubleshooting

Email:

- Outlook Configuration
- Shared Mailboxes

Banking systems:

- Trading Platform Access
- Portfolio Management Permissions
- Market Data Entitlement Requests
- Client Reporting Portal Access
- Document Management System Access

Security:

- Phishing Reporting Procedure
- Device Encryption Requirements
- Security Incident Escalation
- Suspicious Login Investigation Process

Operations:

- Employee Onboarding
- Employee Offboarding
- Access Certification Process

---

## Relationship Requirements

Every knowledge base article should have multiple related tickets.

The ticket descriptions should almost never explicitly mention the root cause. Users should describe
symptoms, observations, or error messages instead.

The root cause should usually be discoverable through:

- historical ticket resolutions
- knowledge base procedures
- repeated ticket patterns

Example:

Knowledge Base article: Trading Platform Access

Related Tickets:

- Cannot view client positions
- Missing trade approval screen
- Market data unavailable
- Portfolio dashboard empty

Root Cause: Required entitlement not assigned

---

## Data Quality

Generate 10-15 tickets with:

- incorrect initial diagnosis
- reopened incidents
- incomplete resolutions
- recurring incidents after a temporary fix

---

## Output

Produce:

1. Ticket records in JSON.
2. Knowledge base articles as markdown.
3. Consistent references between tickets and Knowledge Base topics.
4. Realistic timestamps spanning 12 months.

Generate a fully realistic synthetic dataset matching all constraints, not a simplified version.
