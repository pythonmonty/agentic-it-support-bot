# Synthetic IT-Support Dataset for a Private Bank

The datasets were generated with Claude's Opus 4.8 model by feeding it the prompt
[dataset_generation_prompt.md](../dataset_generation_prompt.md).


A synthetic dataset with **structured support tickets** (relational/JSON) and
**unstructured knowledge base articles** (markdown). It models internal IT operations at a
~6,000-employee private bank over the 2025 calendar year.

## Files
- `tickets.json`: 150 support tickets (schema below).
- `kb/`: 25 knowledge base articles (markdown).
- `relationships.json`: ground-truth links between KB <-> root cause <-> tickets, incident waves,
  and example evaluation questions. This dataset can be used for evaluation purposes.

> Synthetic data. All names, usernames, and events are fabricated.
