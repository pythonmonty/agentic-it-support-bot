# Synthetic IT-Support Dataset for a Private Bank

This dataset was generated with Claude's Opus 4.8 model by feeding it [rename this doc](../dataset-generation.md)

A synthetic dataset for evaluating a conversational AI that answers questions by combining
**structured support tickets** (relational/JSON) with **unstructured knowledge base articles** (markdown).
It models internal IT operations at a ~6,000-employee private bank over the 2025 calendar year.

## Files
- `tickets.json` — 150 support tickets (schema below).
- `kb/` — 25 knowledge base articles (markdown).
- `relationships.json` — ground-truth links (KB ⇄ root cause ⇄ tickets), incident waves, and example evaluation questions.

## Design principles
- **Symptoms, not causes.** Ticket `description` fields read like real users (typos, abbreviations) and rarely name the cause.
- **Cause is discoverable, not stated.** The root cause surfaces only via the `root_cause`/`resolution` fields of *resolved* tickets, recurring patterns, and KB procedures — so many questions require joining sources.
- **Recurring operational patterns.** Six root causes each span 8+ tickets; three incident waves create realistic spikes.

## Ticket schema
```
ticket_id, created_at, requester_user, department, language,
category, product, priority, impact_level, application_criticality,
subject, description, status, root_cause, resolution,
resolution_time_hours, assigned_team, tags[]
```
Complex tickets may also carry: `reopened_count`, `work_notes[]`.
`root_cause`/`resolution`/`resolution_time_hours` are populated only for resolved/closed/reopened tickets.

## Distribution
- **By area:** Identity & Access 40 · VPN & Remote Access 25 · Banking Apps 35 · Email & Collaboration 20 · Security 20 · Infra & Endpoints 10.
- **By category:** {'access': 51, 'account': 10, 'network': 33, 'security': 30, 'software': 24, 'hardware': 2}
- **By status:** {'closed': 21, 'resolved': 106, 'in_progress': 16, 'reopened': 4, 'open': 3}
- **Data quality:** 4 reopened (recurred after a temporary fix), 4 misdiagnosed (wrong initial diagnosis), 5 incomplete (still pending).

## Recurring root causes (8+ tickets)
| Root cause | Tickets |
|---|---|
| Expired VPN certificate | 13 |
| Failed MFA enrollment | 10 |
| Outlook profile corruption | 9 |
| Portfolio access role missing | 9 |
| Trading profile misconfiguration | 8 |
| Missing market data entitlement | 8 |

## Incident waves
- **Mar 2025** — Expired VPN certificate batch → spike in VPN tickets.
- **Jun 2025** — Failed MFA enrollment process → spike in authentication tickets.
- **Sep 2025** — Market-data entitlement lapse → spike in trading-app tickets.

## Relationships
Every KB article links to multiple tickets (2–15 each). The full mapping, including secondary
cross-references (e.g., MFA Recovery ↔ MFA enrollment tickets), lives in `relationships.json`.

## Example evaluation questions
Single-source, cross-source (require joining tickets + KB), temporal/aggregate, and data-quality
questions are listed in `relationships.json` under `example_evaluation_questions`. The majority are
cross-source by design.

> Synthetic data. All names, usernames, and events are fabricated.
