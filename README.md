# Agentic IT Support Bot

Chat in natural language with an internal IT Knowledge Base (KB) that combines **structured data**
(150 historical support tickets in a relational database) and **unstructured data** (25 knowledge
base articles in markdown).

The agent is implemented as an LLM-driven tool-use loop built on the OpenAI SDK. The model decides
each step whether to:

- run read-only SQL over the ticket database,
- semantically search the KB,
- read a full article
- or answer with citations to ticket IDs and KB articles.

## Requirements

- Python 3.13
- [uv](https://docs.astral.sh/uv/)
- An OpenAI-compatible LLM endpoint. For testing purposes a local [Ollama](https://ollama.com)
  was used.

To use the local llama model, run the commands below:

> **Note**: Make sure to run `ollama serve` beforehand to be able to pull the models. The pull of
> the chat model will take some time due to the model size.

```bash
ollama pull llama3.1:8b        # chat model
ollama pull nomic-embed-text   # embedding model
```

## Run

```bash
uv sync
uv run it-support-bot            # interactive chat
```

> **Note**: Make sure to run this from the repo root (the dataset is located via the `DATASET_DIR`
> setting, default `./it-support-dataset`).

### Configuration (environment variables)

| Variable              | Default                     | Purpose                                                 |
|-----------------------|-----------------------------|---------------------------------------------------------|
| `LLM_BASE_URL`        | `http://localhost:11434/v1` | Any OpenAI-compatible endpoint                          |
| `LLM_API_KEY`         | `ollama`                    | API key for that endpoint                               |
| `LLM_CHAT_MODEL`      | `llama3.1:8b`               | Chat model (must support tool calling)                  |
| `LLM_EMBEDDING_MODEL` | `nomic-embed-text`          | Embedding model                                         |
| `RETRIEVER`           | `auto`                      | `vector`, `bm25`, or `auto` (vector with BM25 fallback) |
| `DATASET_DIR`         | `it-support-dataset`        | Dataset location                                        |
| `MAX_AGENT_STEPS`     | `8`                         | Tool-use iterations per question                        |

With `RETRIEVER=auto`, if the embedding endpoint is unreachable the system degrades to a local
BM25 keyword retriever (`rank-bm25`) instead of failing.

## Tests & code quality

To run tests:

```bash
uv run pytest
```

To run pre-commit hooks:

```bash
uv run pre-commit install
uv run pre-commit run --all-files
```
