from it_support_bot.llm.base import EmbeddingProvider
from it_support_bot.retrieval.bm25_retriever import BM25Retriever
from it_support_bot.retrieval.chunking import chunk_markdown
from it_support_bot.retrieval.vector_retriever import VectorRetriever

ARTICLE = """\
# VPN Certificate Renewal

## Summary
Renewing the certificate the VPN uses for authentication.

## Symptoms
- VPN suddenly stops connecting with a certificate error

## Resolution Steps
1. Trigger certificate renewal from Endpoint Management.
"""


def test_chunk_markdown_splits_sections_and_keeps_title():
    chunks = chunk_markdown("vpn-certificate-renewal.md", ARTICLE)
    assert [c.section for c in chunks] == ["Summary", "Symptoms", "Resolution Steps"]
    assert all(c.title == "VPN Certificate Renewal" for c in chunks)
    assert all(c.doc_id == "vpn-certificate-renewal.md" for c in chunks)


def _corpus():
    chunks = chunk_markdown("vpn-certificate-renewal.md", ARTICLE)
    chunks += chunk_markdown(
        "outlook-configuration.md",
        "# Outlook Configuration\n\n## Summary\nRebuilding a corrupted Outlook profile.\n",
    )
    return chunks


def test_bm25_ranks_relevant_article_first():
    retriever = BM25Retriever(_corpus())
    results = retriever.search("vpn certificate error", top_k=3)
    assert results
    assert results[0].chunk.doc_id == "vpn-certificate-renewal.md"


class _KeywordEmbedding(EmbeddingProvider):
    KEYWORDS = ["vpn", "certificate", "outlook", "profile"]

    def embed(self, texts):
        return [[float(word in text.lower()) for word in self.KEYWORDS] for text in texts]

    @property
    def model_id(self) -> str:
        return "fake-keyword-model"


def test_vector_retriever_uses_cosine_and_caches(tmp_path):
    retriever = VectorRetriever(_corpus(), _KeywordEmbedding(), cache_dir=tmp_path)
    results = retriever.search("outlook profile broken", top_k=1)
    assert results[0].chunk.doc_id == "outlook-configuration.md"
    cache_files = list(tmp_path.glob("embeddings-*.json"))
    assert len(cache_files) == 1
