"""
SEMANTIC MEMORY ENGINE — Phase 2

The identity graph gives structure. This gives MEANING.

Instead of exact keyword matching, the twin can now:
- Find nodes by meaning ("what am I afraid of?" → fears)
- Find similar concepts across domains
- Answer open-ended questions by searching its own mind
- Rank relevance by semantic distance, not just edge weight

Uses numpy for cosine similarity with pre-computed embeddings
from Claude API (batched, cached, cheap).
"""

import json
import os
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph


class SemanticMemory:
    """
    Vector-based semantic search over the identity graph.

    Every node gets an embedding. Queries get embedded.
    Cosine similarity finds the closest nodes by MEANING.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.embeddings_path = self.data_dir / "embeddings.json"
        self.embeddings: dict[str, list[float]] = {}
        self._load_embeddings()

    def _load_embeddings(self):
        if self.embeddings_path.exists():
            with open(self.embeddings_path) as f:
                self.embeddings = json.load(f)

    def _save_embeddings(self):
        with open(self.embeddings_path, "w") as f:
            json.dump(self.embeddings, f)

    # ═══════════════════════════════════════════
    # EMBEDDING GENERATION (via Claude API)
    # ═══════════════════════════════════════════

    def embed_all_nodes(self):
        """Generate embeddings for all nodes using Claude API."""
        import anthropic
        client = anthropic.Anthropic()

        nodes_to_embed = []
        for node_id, node in self.graph.nodes.items():
            # Check if we already have a current embedding
            text = self._node_to_text(node)
            text_hash = hashlib.md5(text.encode()).hexdigest()
            cache_key = f"{node_id}:{text_hash}"

            if cache_key not in self.embeddings:
                nodes_to_embed.append((node_id, text, cache_key))

        if not nodes_to_embed:
            print("All nodes already embedded.")
            return

        print(f"Embedding {len(nodes_to_embed)} nodes...")

        # Batch embed using Claude to generate semantic representations
        # Since Claude doesn't have a native embedding endpoint,
        # we use a clever trick: ask Claude to generate a semantic fingerprint
        # as a structured vector of concept scores

        DIMENSIONS = 64  # Compact but expressive
        CONCEPTS = [
            "revenue", "growth", "risk", "technical", "creative",
            "social", "emotional", "strategic", "urgent", "long_term",
            "fear", "confidence", "learning", "building", "selling",
            "personal", "professional", "health", "faith", "legacy",
            "parallel", "sequential", "abstract", "concrete", "visual",
            "kinesthetic", "verbal", "intuitive", "analytical", "collaborative",
            "independent", "competitive", "empathetic", "ambitious", "patient",
            "impulsive", "disciplined", "creative_chaos", "structured", "momentum",
            "stagnation", "pain", "pleasure", "obligation", "passion",
            "family", "friendship", "business", "technology", "nature",
            "science", "art", "philosophy", "psychology", "finance",
            "law", "education", "leadership", "execution", "vision",
            "authenticity", "vulnerability", "strength", "adaptability", "focus",
            "curiosity", "determination", "humility", "pride",
        ]

        # Batch process in groups of 10
        batch_size = 10
        for i in range(0, len(nodes_to_embed), batch_size):
            batch = nodes_to_embed[i:i + batch_size]
            texts = [f"Node: {text}" for _, text, _ in batch]

            prompt = f"""Rate each of the following items on these {len(CONCEPTS)} dimensions from 0.0 to 1.0.
Return ONLY a JSON array of arrays (one inner array per item, each with {len(CONCEPTS)} floats).
No explanation, no markdown, just the JSON array.

Dimensions: {', '.join(CONCEPTS)}

Items:
{chr(10).join(f'{j+1}. {t}' for j, t in enumerate(texts))}"""

            try:
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=4096,
                    messages=[{"role": "user", "content": prompt}],
                )

                # Parse response
                response_text = response.content[0].text.strip()
                # Clean up potential markdown
                if response_text.startswith("```"):
                    response_text = response_text.split("\n", 1)[1].rsplit("```", 1)[0]

                vectors = json.loads(response_text)

                for j, (node_id, text, cache_key) in enumerate(batch):
                    if j < len(vectors):
                        # Pad or trim to exact dimensions
                        vec = vectors[j][:DIMENSIONS]
                        while len(vec) < DIMENSIONS:
                            vec.append(0.0)
                        self.embeddings[cache_key] = vec
                        # Also store by node_id for quick lookup
                        self.embeddings[node_id] = vec

                print(f"  Embedded batch {i//batch_size + 1}/{(len(nodes_to_embed) + batch_size - 1)//batch_size}")

            except Exception as e:
                print(f"  Error embedding batch: {e}")
                continue

        self._save_embeddings()
        print(f"Saved {len(self.embeddings)} embeddings")

    def embed_query(self, query: str) -> list[float]:
        """Embed a query string for similarity search."""
        import anthropic
        client = anthropic.Anthropic()

        DIMENSIONS = 64
        CONCEPTS = [
            "revenue", "growth", "risk", "technical", "creative",
            "social", "emotional", "strategic", "urgent", "long_term",
            "fear", "confidence", "learning", "building", "selling",
            "personal", "professional", "health", "faith", "legacy",
            "parallel", "sequential", "abstract", "concrete", "visual",
            "kinesthetic", "verbal", "intuitive", "analytical", "collaborative",
            "independent", "competitive", "empathetic", "ambitious", "patient",
            "impulsive", "disciplined", "creative_chaos", "structured", "momentum",
            "stagnation", "pain", "pleasure", "obligation", "passion",
            "family", "friendship", "business", "technology", "nature",
            "science", "art", "philosophy", "psychology", "finance",
            "law", "education", "leadership", "execution", "vision",
            "authenticity", "vulnerability", "strength", "adaptability", "focus",
            "curiosity", "determination", "humility", "pride",
        ]

        prompt = f"""Rate this query on these {len(CONCEPTS)} dimensions from 0.0 to 1.0.
Return ONLY a JSON array of {len(CONCEPTS)} floats. No explanation.

Dimensions: {', '.join(CONCEPTS)}

Query: {query}"""

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            response_text = response.content[0].text.strip()
            if response_text.startswith("```"):
                response_text = response_text.split("\n", 1)[1].rsplit("```", 1)[0]
            vec = json.loads(response_text)[:DIMENSIONS]
            while len(vec) < DIMENSIONS:
                vec.append(0.0)
            return vec
        except Exception as e:
            print(f"Error embedding query: {e}")
            return [0.0] * DIMENSIONS

    # ═══════════════════════════════════════════
    # SEMANTIC SEARCH
    # ═══════════════════════════════════════════

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        """
        Search the twin's mind by meaning.

        "What am I afraid of?" → finds fear nodes
        "How do I make money?" → finds revenue-related nodes
        "What connects hemp to Anthropic?" → finds the path
        """
        query_vec = self.embed_query(query)
        query_arr = np.array(query_vec)

        results = []
        for node_id, node in self.graph.nodes.items():
            if node_id in self.embeddings:
                node_vec = np.array(self.embeddings[node_id])
                similarity = self._cosine_similarity(query_arr, node_vec)
                results.append({
                    "node_id": node_id,
                    "name": node.name,
                    "type": node.type,
                    "description": node.description,
                    "similarity": round(float(similarity), 4),
                    "weight": node.weight,
                    "relevance": round(float(similarity) * node.weight, 4),
                })

        # Sort by relevance (similarity * weight)
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:top_k]

    def find_similar(self, node_id: str, top_k: int = 5) -> list[dict]:
        """Find nodes semantically similar to a given node."""
        if node_id not in self.embeddings:
            return []

        target_vec = np.array(self.embeddings[node_id])
        results = []

        for other_id, other_node in self.graph.nodes.items():
            if other_id == node_id:
                continue
            if other_id in self.embeddings:
                other_vec = np.array(self.embeddings[other_id])
                similarity = self._cosine_similarity(target_vec, other_vec)
                results.append({
                    "node_id": other_id,
                    "name": other_node.name,
                    "type": other_node.type,
                    "similarity": round(float(similarity), 4),
                })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def discover_hidden_patterns(self) -> list[dict]:
        """
        Find nodes that are semantically similar but NOT connected in the graph.
        These are potential cross-domain insights Josh hasn't made yet.
        """
        discoveries = []

        node_ids = [nid for nid in self.graph.nodes if nid in self.embeddings]

        for i, nid1 in enumerate(node_ids):
            vec1 = np.array(self.embeddings[nid1])
            for nid2 in node_ids[i+1:]:
                vec2 = np.array(self.embeddings[nid2])
                similarity = self._cosine_similarity(vec1, vec2)

                if similarity > 0.85:  # High semantic similarity
                    # Check if they're connected in the graph
                    connected = any(
                        e for e in self.graph.edges
                        if {e.source_id, e.target_id} == {nid1, nid2}
                    )

                    if not connected:
                        n1 = self.graph.nodes[nid1]
                        n2 = self.graph.nodes[nid2]
                        discoveries.append({
                            "node1": n1.name,
                            "node1_type": n1.type,
                            "node2": n2.name,
                            "node2_type": n2.type,
                            "similarity": round(float(similarity), 4),
                            "insight": f"'{n1.name}' and '{n2.name}' are semantically close ({similarity:.2f}) but not connected — potential hidden pattern",
                        })

        discoveries.sort(key=lambda x: x["similarity"], reverse=True)
        return discoveries[:20]

    # ═══════════════════════════════════════════
    # UTILITY
    # ═══════════════════════════════════════════

    def _node_to_text(self, node) -> str:
        """Convert a node to searchable text."""
        parts = [
            f"Name: {node.name}",
            f"Type: {node.type}",
        ]
        if node.description:
            parts.append(f"Description: {node.description}")
        if node.metadata:
            for k, v in node.metadata.items():
                parts.append(f"{k}: {v}")
        return " | ".join(parts)

    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return float(np.dot(a, b) / (norm_a * norm_b))

    def stats(self) -> dict:
        embedded = sum(1 for nid in self.graph.nodes if nid in self.embeddings)
        return {
            "total_nodes": len(self.graph.nodes),
            "embedded_nodes": embedded,
            "coverage": f"{embedded / max(len(self.graph.nodes), 1) * 100:.0f}%",
            "embedding_dimensions": 64,
        }


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    memory = SemanticMemory(graph)

    print("=" * 60)
    print("SEMANTIC MEMORY ENGINE — Phase 2")
    print("=" * 60)

    stats = memory.stats()
    print(f"\nCoverage: {stats['coverage']} ({stats['embedded_nodes']}/{stats['total_nodes']} nodes)")

    if stats["embedded_nodes"] == 0:
        print("\nNo embeddings yet. Generating...")
        memory.embed_all_nodes()
        print(f"\nNow: {memory.stats()['coverage']} coverage")

    # Search demos
    queries = [
        "What am I most afraid of?",
        "How do I make money?",
        "What makes me different from other founders?",
        "What should I do when I'm stuck?",
        "What connects my hemp route to my tech career?",
    ]

    for query in queries:
        print(f"\n--- SEARCH: '{query}' ---")
        results = memory.search(query, top_k=5)
        for r in results:
            print(f"  [{r['similarity']:.2f}] {r['name']} ({r['type']}) — {r['description'][:60]}")

    # Hidden patterns
    print("\n--- HIDDEN PATTERNS (semantic but not connected) ---")
    patterns = memory.discover_hidden_patterns()
    for p in patterns[:5]:
        print(f"  [{p['similarity']:.2f}] {p['insight']}")

    print("\nSemantic memory operational.")


if __name__ == "__main__":
    demo()
