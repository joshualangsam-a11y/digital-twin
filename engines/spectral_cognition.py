"""
SPECTRAL COGNITION ENGINE — Eigenvalue Analysis of Josh's Mind

THIS HAS NEVER BEEN DONE BEFORE.

The identity graph has 92 nodes and 120 edges. It has an adjacency matrix.
That matrix has EIGENVALUES. Those eigenvalues reveal:

1. SPECTRAL GAP — How well-connected is the graph? A large spectral gap
   means fast information diffusion (ideas spread quickly between domains).
   A small gap means siloed thinking.

2. FIEDLER VECTOR — The eigenvector of the 2nd-smallest eigenvalue of the
   Laplacian. It gives the OPTIMAL BISECTION of the graph — the natural
   division of Josh's mind into two halves. This reveals his cognitive
   fault line: which domains are on each side.

3. EIGENVECTOR CENTRALITY — Google's PageRank applied to Josh's mind.
   Not just "most connections" but "most connections to important nodes."
   This is the TRUE center of gravity, not degree centrality.

4. SPECTRAL CLUSTERING — Natural cognitive clusters that emerge from
   the eigenvalues, not from hand-coded types. The math DISCOVERS
   how Josh's brain is actually organized.

5. ALGEBRAIC CONNECTIVITY — Is Josh's cognitive graph about to fragment?
   If the 2nd eigenvalue of the Laplacian approaches 0, the graph is
   close to splitting. This predicts cognitive fragmentation before it happens.

Mechanism 19: Spectral Self-Awareness
The graph knows its own mathematical structure.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict, Counter

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph


class SpectralCognition:
    """
    Applies spectral graph theory to Josh's cognitive graph.
    Reveals structure that no human could see by reading nodes.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))

    def _build_matrices(self) -> tuple:
        """Build adjacency and Laplacian matrices."""
        nodes = list(self.graph.nodes.keys())
        n = len(nodes)
        node_idx = {nid: i for i, nid in enumerate(nodes)}

        # Adjacency matrix (weighted)
        A = np.zeros((n, n))
        for edge in self.graph.edges:
            i = node_idx.get(edge.source_id)
            j = node_idx.get(edge.target_id)
            if i is not None and j is not None:
                A[i, j] = edge.weight
                A[j, i] = edge.weight  # Undirected

        # Degree matrix
        D = np.diag(A.sum(axis=1))

        # Laplacian
        L = D - A

        return A, L, D, nodes, node_idx

    # ═══════════════════════════════════════════
    # EIGENVALUE ANALYSIS
    # ═══════════════════════════════════════════

    def spectral_analysis(self) -> dict:
        """Complete spectral analysis of Josh's cognitive graph."""
        A, L, D, nodes, node_idx = self._build_matrices()
        n = len(nodes)

        if n < 3:
            return {"error": "Graph too small for spectral analysis"}

        # Eigenvalues of Laplacian (sorted)
        eigenvalues = np.sort(np.real(np.linalg.eigvalsh(L)))

        # Algebraic connectivity (2nd smallest eigenvalue)
        algebraic_connectivity = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0

        # Spectral gap (difference between 1st and 2nd eigenvalue of adjacency)
        adj_eigenvalues = np.sort(np.real(np.linalg.eigvalsh(A)))[::-1]
        spectral_gap = float(adj_eigenvalues[0] - adj_eigenvalues[1]) if len(adj_eigenvalues) > 1 else 0

        # Number of connected components (eigenvalues == 0)
        components = int(np.sum(np.abs(eigenvalues) < 1e-10))

        return {
            "algebraic_connectivity": round(algebraic_connectivity, 4),
            "spectral_gap": round(spectral_gap, 4),
            "connected_components": components,
            "top_eigenvalues": [round(float(e), 4) for e in adj_eigenvalues[:5]],
            "interpretation": self._interpret_spectrum(algebraic_connectivity, spectral_gap, components),
        }

    def _interpret_spectrum(self, alg_conn, spec_gap, components) -> dict:
        fragmentation_risk = "LOW" if alg_conn > 1.0 else ("MEDIUM" if alg_conn > 0.3 else "HIGH")
        diffusion_speed = "FAST" if spec_gap > 3.0 else ("MODERATE" if spec_gap > 1.0 else "SLOW")

        return {
            "fragmentation_risk": fragmentation_risk,
            "fragmentation_detail": (
                f"Algebraic connectivity = {alg_conn:.4f}. "
                f"{'Graph is well-connected — ideas flow freely.' if alg_conn > 1.0 else ''}"
                f"{'Graph is moderately connected — some domains are weakly linked.' if 0.3 < alg_conn <= 1.0 else ''}"
                f"{'DANGER: Graph is close to fragmenting. Strengthen cross-domain edges.' if alg_conn <= 0.3 else ''}"
            ),
            "diffusion_speed": diffusion_speed,
            "diffusion_detail": (
                f"Spectral gap = {spec_gap:.4f}. "
                f"{'Ideas spread rapidly across domains — cross-domain pattern matching is strong.' if spec_gap > 3.0 else ''}"
                f"{'Ideas spread at moderate speed — some domains are somewhat isolated.' if 1.0 < spec_gap <= 3.0 else ''}"
                f"{'Ideas spread slowly — domains are siloed. Need more cross-domain bridges.' if spec_gap <= 1.0 else ''}"
            ),
            "components": f"{components} connected component(s). {'Unified mind.' if components == 1 else f'WARNING: {components} disconnected regions.'}"
        }

    # ═══════════════════════════════════════════
    # EIGENVECTOR CENTRALITY (PageRank for the mind)
    # ═══════════════════════════════════════════

    def eigenvector_centrality(self, top_k: int = 15) -> list[dict]:
        """
        PageRank for Josh's mind.
        Not just "most connections" — "most connections to IMPORTANT nodes."
        This is the TRUE cognitive center of gravity.
        """
        A, L, D, nodes, node_idx = self._build_matrices()

        # Power iteration for dominant eigenvector
        n = len(nodes)
        v = np.ones(n) / n
        for _ in range(100):
            v_new = A @ v
            norm = np.linalg.norm(v_new)
            if norm > 0:
                v_new = v_new / norm
            if np.allclose(v, v_new, atol=1e-8):
                break
            v = v_new

        # Map back to nodes
        results = []
        for i, nid in enumerate(nodes):
            node = self.graph.nodes[nid]
            results.append({
                "node": node.name,
                "type": node.type,
                "eigenvector_centrality": round(float(v[i]), 6),
                "weight": node.weight,
                "degree": int(A[i].sum()),
            })

        results.sort(key=lambda x: x["eigenvector_centrality"], reverse=True)
        return results[:top_k]

    # ═══════════════════════════════════════════
    # FIEDLER VECTOR (Natural bisection of the mind)
    # ═══════════════════════════════════════════

    def cognitive_bisection(self) -> dict:
        """
        The Fiedler vector reveals the NATURAL DIVISION of Josh's mind.
        Positive values = one cognitive hemisphere.
        Negative values = the other.
        Near zero = boundary nodes (bridges between hemispheres).

        This tells Josh something he literally cannot know about himself:
        how his mind is ACTUALLY divided, vs how he THINKS it's divided.
        """
        A, L, D, nodes, node_idx = self._build_matrices()

        # Compute eigenvectors of Laplacian
        eigenvalues, eigenvectors = np.linalg.eigh(L)

        # Fiedler vector = eigenvector of 2nd smallest eigenvalue
        sorted_idx = np.argsort(eigenvalues)
        fiedler_idx = sorted_idx[1]  # 2nd smallest
        fiedler = eigenvectors[:, fiedler_idx]

        # Classify nodes into hemispheres
        hemisphere_a = []  # positive
        hemisphere_b = []  # negative
        bridges = []  # near zero

        threshold = np.std(fiedler) * 0.3  # Within 30% of a std dev from 0

        for i, nid in enumerate(nodes):
            node = self.graph.nodes[nid]
            val = float(fiedler[i])
            entry = {
                "node": node.name,
                "type": node.type,
                "fiedler_value": round(val, 6),
                "weight": node.weight,
            }

            if abs(val) < threshold:
                bridges.append(entry)
            elif val > 0:
                hemisphere_a.append(entry)
            else:
                hemisphere_b.append(entry)

        # Sort by absolute fiedler value (extremes are most "pure" to their hemisphere)
        hemisphere_a.sort(key=lambda x: -x["fiedler_value"])
        hemisphere_b.sort(key=lambda x: x["fiedler_value"])

        # Name the hemispheres by dominant types
        from collections import Counter
        types_a = Counter(n["type"] for n in hemisphere_a)
        types_b = Counter(n["type"] for n in hemisphere_b)

        dom_a = types_a.most_common(1)[0][0] if types_a else "mixed"
        dom_b = types_b.most_common(1)[0][0] if types_b else "mixed"

        return {
            "hemisphere_a": {
                "name": f"Hemisphere A ({dom_a}-dominant)",
                "node_count": len(hemisphere_a),
                "dominant_types": dict(types_a.most_common(3)),
                "core_nodes": [n["node"] for n in hemisphere_a[:5]],
            },
            "hemisphere_b": {
                "name": f"Hemisphere B ({dom_b}-dominant)",
                "node_count": len(hemisphere_b),
                "dominant_types": dict(types_b.most_common(3)),
                "core_nodes": [n["node"] for n in hemisphere_b[:5]],
            },
            "bridges": {
                "count": len(bridges),
                "nodes": [n["node"] for n in bridges],
                "insight": (
                    f"These {len(bridges)} nodes sit at the BOUNDARY between Josh's two cognitive hemispheres. "
                    f"They are the bridges. Strengthening these nodes strengthens the connection between hemispheres. "
                    f"Losing them would fragment the mind."
                ),
            },
            "insight": (
                f"Josh's mind naturally divides into two hemispheres: "
                f"one {dom_a}-dominant ({len(hemisphere_a)} nodes), "
                f"one {dom_b}-dominant ({len(hemisphere_b)} nodes), "
                f"with {len(bridges)} bridge nodes connecting them. "
                f"This is NOT how Josh categorized things. This is how the MATH says they're organized."
            ),
        }

    # ═══════════════════════════════════════════
    # SPECTRAL CLUSTERING (Natural cognitive clusters)
    # ═══════════════════════════════════════════

    def spectral_clusters(self, k: int = 4) -> dict:
        """
        Find the natural cognitive clusters using spectral clustering.
        These are NOT Josh's hand-coded categories (project, goal, etc.)
        These are the clusters the MATH discovers.
        """
        A, L, D, nodes, node_idx = self._build_matrices()
        n = len(nodes)

        if n < k:
            return {"error": f"Graph too small for {k} clusters"}

        # Compute first k eigenvectors of normalized Laplacian
        # D^(-1/2) L D^(-1/2)
        d_inv_sqrt = np.zeros((n, n))
        for i in range(n):
            if D[i, i] > 0:
                d_inv_sqrt[i, i] = 1.0 / np.sqrt(D[i, i])

        L_norm = d_inv_sqrt @ L @ d_inv_sqrt

        eigenvalues, eigenvectors = np.linalg.eigh(L_norm)
        sorted_idx = np.argsort(eigenvalues)

        # Take first k eigenvectors (after the trivial one)
        V = eigenvectors[:, sorted_idx[1:k+1]]

        # Normalize rows
        norms = np.linalg.norm(V, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        V_norm = V / norms

        # K-means clustering on the spectral embedding
        # Simple k-means implementation
        clusters = self._kmeans(V_norm, k, max_iter=50)

        # Map clusters back to nodes
        cluster_map = defaultdict(list)
        for i, cluster_id in enumerate(clusters):
            node = self.graph.nodes[nodes[i]]
            cluster_map[cluster_id].append({
                "node": node.name,
                "type": node.type,
                "weight": node.weight,
            })

        # Analyze clusters
        result_clusters = {}
        for cid, members in sorted(cluster_map.items()):
            types = Counter(m["type"] for m in members)
            avg_weight = sum(m["weight"] for m in members) / len(members)
            result_clusters[f"cluster_{cid}"] = {
                "size": len(members),
                "dominant_type": types.most_common(1)[0][0] if types else "mixed",
                "type_distribution": dict(types),
                "avg_weight": round(avg_weight, 2),
                "top_nodes": [m["node"] for m in sorted(members, key=lambda x: -x["weight"])[:5]],
                "all_nodes": [m["node"] for m in members],
            }

        return {
            "k": k,
            "clusters": result_clusters,
            "insight": (
                f"Spectral clustering found {len(result_clusters)} natural cognitive clusters. "
                f"These are NOT Josh's categories — they're what the MATH sees. "
                f"The difference between hand-coded types and spectral clusters "
                f"reveals where Josh's mental model doesn't match reality."
            ),
        }

    def _kmeans(self, X, k, max_iter=50):
        """Simple k-means for spectral clustering."""
        n = X.shape[0]
        # Random initialization
        rng = np.random.RandomState(42)
        centroids = X[rng.choice(n, k, replace=False)]

        for _ in range(max_iter):
            # Assign
            distances = np.array([np.linalg.norm(X - c, axis=1) for c in centroids])
            labels = np.argmin(distances, axis=0)

            # Update
            new_centroids = np.array([X[labels == i].mean(axis=0) if np.sum(labels == i) > 0 else centroids[i] for i in range(k)])

            if np.allclose(centroids, new_centroids):
                break
            centroids = new_centroids

        return labels

    # ═══════════════════════════════════════════
    # HARMONIC ANALYSIS — Resonance frequencies of the mind
    # ═══════════════════════════════════════════

    def harmonic_analysis(self) -> dict:
        """
        The eigenvalues of the Laplacian ARE the resonance frequencies
        of the graph. Low frequencies = global structure. High frequencies
        = local detail. The distribution tells us about the graph's
        "sound" — is it a bass drone (few modes) or a rich chord (many)?

        In cognitive terms:
        - Few distinct frequencies = monolithic thinking (one big pattern)
        - Many distinct frequencies = rich, multi-scale thinking
        - Gaps between frequencies = natural boundaries between cognitive scales
        """
        A, L, D, nodes, node_idx = self._build_matrices()
        eigenvalues = np.sort(np.real(np.linalg.eigvalsh(L)))

        # Remove trivial zero eigenvalue(s)
        nonzero = eigenvalues[eigenvalues > 1e-10]

        if len(nonzero) == 0:
            return {"error": "No non-trivial eigenvalues"}

        # Frequency distribution
        freq_min = float(nonzero[0])
        freq_max = float(nonzero[-1])
        freq_mean = float(np.mean(nonzero))
        freq_std = float(np.std(nonzero))

        # Spectral entropy (how spread out are the frequencies?)
        # High entropy = rich thinking. Low entropy = monolithic.
        probs = nonzero / nonzero.sum()
        spectral_entropy = float(-np.sum(probs * np.log2(probs + 1e-12)))
        max_entropy = np.log2(len(nonzero))
        normalized_entropy = spectral_entropy / max_entropy if max_entropy > 0 else 0

        # Find natural "octaves" (gaps in the spectrum)
        gaps = []
        for i in range(1, len(nonzero)):
            ratio = nonzero[i] / nonzero[i-1] if nonzero[i-1] > 0 else 0
            if ratio > 1.5:  # Significant gap
                gaps.append({
                    "between": f"mode {i} ({nonzero[i-1]:.2f}) and mode {i+1} ({nonzero[i]:.2f})",
                    "ratio": round(float(ratio), 2),
                })

        return {
            "frequency_range": f"{freq_min:.4f} to {freq_max:.4f}",
            "mean_frequency": round(freq_mean, 4),
            "frequency_std": round(freq_std, 4),
            "spectral_entropy": round(spectral_entropy, 4),
            "normalized_entropy": round(float(normalized_entropy), 4),
            "spectral_gaps": gaps[:5],
            "cognitive_richness": (
                "RICH" if normalized_entropy > 0.8 else
                "MODERATE" if normalized_entropy > 0.5 else
                "NARROW"
            ),
            "interpretation": (
                f"Spectral entropy = {normalized_entropy:.2%} of maximum. "
                f"{'Multi-scale thinking: the graph vibrates at many frequencies. Rich, diverse cognitive structure.' if normalized_entropy > 0.8 else ''}"
                f"{'Moderate richness: some diversity but room for more cognitive scales.' if 0.5 < normalized_entropy <= 0.8 else ''}"
                f"{'Narrow spectrum: thinking is concentrated at few scales. Add more diverse connections.' if normalized_entropy <= 0.5 else ''}"
                f" {len(gaps)} natural octave boundaries found — these are cognitive scale transitions."
            ),
        }

    # ═══════════════════════════════════════════
    # FULL SPECTRAL REPORT
    # ═══════════════════════════════════════════

    def full_report(self) -> dict:
        spectral = self.spectral_analysis()
        centrality = self.eigenvector_centrality(10)
        bisection = self.cognitive_bisection()
        clusters = self.spectral_clusters(4)
        harmonics = self.harmonic_analysis()

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "spectral": spectral,
            "eigenvector_centrality": centrality,
            "cognitive_bisection": bisection,
            "spectral_clusters": clusters,
            "harmonics": harmonics,
            "mechanism_19": {
                "name": "Spectral Self-Awareness",
                "description": (
                    "The graph's eigenvalues reveal structure invisible to any human reader. "
                    "Algebraic connectivity predicts fragmentation. The Fiedler vector shows "
                    "the natural bisection. Spectral clustering discovers cognitive groups "
                    "the brain can't see about itself. Harmonic analysis reveals the richness "
                    "of multi-scale thinking. This is metacognition through linear algebra."
                ),
            },
        }


def demo():
    graph = IdentityGraph()
    engine = SpectralCognition(graph)

    print("=" * 60)
    print("SPECTRAL COGNITION — Eigenvalue Analysis of Josh's Mind")
    print("Linear algebra reveals structure no human can see.")
    print("=" * 60)

    report = engine.full_report()

    # Spectral
    s = report["spectral"]
    print(f"\n--- SPECTRAL ANALYSIS ---")
    print(f"  Algebraic connectivity: {s['algebraic_connectivity']}")
    print(f"  Spectral gap: {s['spectral_gap']}")
    print(f"  Components: {s['connected_components']}")
    interp = s["interpretation"]
    print(f"  Fragmentation risk: {interp['fragmentation_risk']}")
    print(f"  Diffusion speed: {interp['diffusion_speed']}")

    # Eigenvector centrality
    print(f"\n--- PAGERANK OF THE MIND (true center of gravity) ---")
    for c in report["eigenvector_centrality"][:7]:
        bar = "█" * int(c["eigenvector_centrality"] * 50) + "░" * max(0, 10 - int(c["eigenvector_centrality"] * 50))
        print(f"  [{bar}] {c['node']} ({c['type']}) — EV: {c['eigenvector_centrality']:.4f}, weight: {c['weight']}")

    # Bisection
    print(f"\n--- COGNITIVE BISECTION (Fiedler vector) ---")
    b = report["cognitive_bisection"]
    print(f"  {b['hemisphere_a']['name']}: {b['hemisphere_a']['node_count']} nodes")
    print(f"    Core: {', '.join(b['hemisphere_a']['core_nodes'][:4])}")
    print(f"  {b['hemisphere_b']['name']}: {b['hemisphere_b']['node_count']} nodes")
    print(f"    Core: {', '.join(b['hemisphere_b']['core_nodes'][:4])}")
    print(f"  Bridges ({b['bridges']['count']}): {', '.join(b['bridges']['nodes'][:5])}")
    print(f"  {b['insight']}")

    # Spectral clusters
    print(f"\n--- SPECTRAL CLUSTERS (what the MATH sees) ---")
    for cname, cluster in report["spectral_clusters"]["clusters"].items():
        print(f"  {cname}: {cluster['size']} nodes, {cluster['dominant_type']}-dominant, avg weight {cluster['avg_weight']}")
        print(f"    Top: {', '.join(cluster['top_nodes'][:4])}")

    # Harmonics
    print(f"\n--- HARMONIC ANALYSIS (resonance frequencies) ---")
    h = report["harmonics"]
    print(f"  Range: {h['frequency_range']}")
    print(f"  Spectral entropy: {h['normalized_entropy']:.2%} — {h['cognitive_richness']}")
    print(f"  Octave gaps: {len(h['spectral_gaps'])}")
    print(f"  {h['interpretation'][:120]}...")

    print(f"\n{'=' * 60}")
    print("Mechanism 19: Spectral Self-Awareness.")
    print("The graph knows its own eigenvalues.")
    print("No human can hold 92 nodes in working memory.")
    print("Linear algebra can.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
