# EXCERPT of src/agents/seo_rag.py (production repo): semantic memory for the content engine
# Pinecone index + OpenAI embeddings (OpenRouter fallback); duplicate detection by cosine similarity.

"""Semantic memory layer for the SEO engine, backed by Pinecone + OpenAI
embeddings (with an OpenRouter fallback for embeddings when the OpenAI
account is out of quota -- same OPENROUTER_API_KEY already used by
seo_content_agent.py for chat completions). Reads
PINECONE_API_KEY/OPENAI_API_KEY/OPENROUTER_API_KEY directly via os.getenv --
same bolt-on pattern as GSC_* in seo_feedback_agent.py, not part of core
Settings. Every public method degrades to a safe no-op return when not
configured, so the production content/feedback pipelines never crash if
these keys are absent."""
import os

INDEX_NAME = "aion-seo"
EMBEDDING_MODEL = "text-embedding-3-small"
OPENROUTER_EMBEDDING_MODEL = "openai/text-embedding-3-small"
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"
EMBEDDING_DIMENSION = 1536
DEFAULT_DUPLICATE_THRESHOLD = 0.92

# Gate against cross-project contamination -- the exact "site" string is the
# only thing separating one project's memory from another's inside the
# shared aion-seo index (2026-08-14, after fixing hours of AION/PMOC domain
# mixing on the actual live sites). A typo or copy-pasted default here
# would silently blend one project's history into another's without any
# error. New real domains get added here deliberately, not passed in loose.
KNOWN_SITES = {"aionreceptionist.com", "global-engenharia.com"}




class SEOSemanticMemory:
    # ...

    def check_semantic_duplicate(
        self, site: str, doc_type: str, text: str, threshold: float = DEFAULT_DUPLICATE_THRESHOLD
    ) -> dict | None:
        """Returns the best match's {id, score, metadata} if it scores at or
        above `threshold`, else None. Used to catch near-duplicate content
        the existing exact-hash dedup in seo_content_agent.py would miss."""
        _validate_site(site)
        if not self.is_configured():
            return None
        try:
            vector = self._embed(text)
            index = self._get_index()
            result = index.query(
                vector=vector, top_k=1, namespace=doc_type,
                filter={"site": {"$eq": site}}, include_metadata=True,
            ).to_dict()
            matches = result.get("matches", [])
            if matches and matches[0]["score"] >= threshold:
                return {"id": matches[0]["id"], "score": matches[0]["score"], "metadata": matches[0].get("metadata", {})}
            return None
        except Exception as e:
            print(f"[SEO-RAG] check_semantic_duplicate failed: {e!r}")
            return None

