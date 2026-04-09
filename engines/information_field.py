"""
INFORMATION FIELD ENGINE — Cognitive Entropy & Information Flow

Applies Shannon information theory to Josh's cognitive graph.
NOT as metaphor — as literal computation.

1. COGNITIVE ENTROPY — How much "disorder" is in the graph?
   High entropy = many equally important things (decision paralysis).
   Low entropy = clear hierarchy (focused but potentially rigid).
   Optimal = moderate entropy with clear peaks (focused but flexible).

2. MUTUAL INFORMATION — How much does knowing about node A tell you
   about node B? High MI = strongly coupled. Changes in A predict
   changes in B. This reveals HIDDEN DEPENDENCIES that edge analysis misses.

3. INFORMATION FLOW — Where does "information" (weight, access) flow
   in the graph? Some nodes are SOURCES (generate influence).
   Some are SINKS (absorb influence). Some are CONDUITS (pass it through).
   This is the PageRank of information dynamics, not structure.

4. CHANNEL CAPACITY — Applying Shannon's channel capacity theorem
   to Josh's cognitive bandwidth. Given noise (distractions, mud hours)
   and signal (compressed intent, flow state), what is the theoretical
   maximum throughput? And how close is Josh to it?

5. KOLMOGOROV COMPLEXITY — How compressible is the graph?
   A highly compressible graph has redundant structure (patterns repeat).
   An incompressible graph is maximally complex (everything is unique).
   Josh's cross-domain patterns SHOULD make the graph compressible —
   the same pattern in different domains is redundancy the math can find.

Mechanism 20: Information-Theoretic Self-Knowledge
The graph computes its own information content.
"""

import json
import os
import math
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter, defaultdict

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph


class InformationField:
    """
    Information theory applied to Josh's cognitive graph.
    Entropy, mutual information, flow, capacity, complexity.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))

    # ═══════════════════════════════════════════
    # 1. COGNITIVE ENTROPY
    # ═══════════════════════════════════════════

    def cognitive_entropy(self) -> dict:
        """
        Shannon entropy of the weight distribution.
        H = -Σ p(x) log₂ p(x)

        Tells Josh: how concentrated or dispersed is his cognitive attention?
        """
        weights = [n.weight for n in self.graph.nodes.values()]
        total = sum(weights)

        if total == 0:
            return {"entropy": 0, "interpretation": "Empty graph"}

        probs = [w / total for w in weights]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        max_entropy = math.log2(len(weights))
        normalized = entropy / max_entropy if max_entropy > 0 else 0

        # Entropy by type
        type_weights = defaultdict(float)
        for n in self.graph.nodes.values():
            type_weights[n.type] += n.weight
        type_total = sum(type_weights.values())
        type_probs = [w / type_total for w in type_weights.values()]
        type_entropy = -sum(p * math.log2(p) for p in type_probs if p > 0)

        # Gini coefficient (inequality measure)
        sorted_weights = sorted(weights)
        n = len(sorted_weights)
        gini = (2 * sum((i + 1) * w for i, w in enumerate(sorted_weights)) - (n + 1) * total) / (n * total) if total > 0 and n > 0 else 0

        return {
            "entropy": round(entropy, 4),
            "max_entropy": round(max_entropy, 4),
            "normalized_entropy": round(normalized, 4),
            "type_entropy": round(type_entropy, 4),
            "gini_coefficient": round(gini, 4),
            "attention_state": (
                "FOCUSED" if normalized < 0.7 else
                "BALANCED" if normalized < 0.85 else
                "DISPERSED"
            ),
            "interpretation": (
                f"Cognitive entropy = {normalized:.1%} of maximum. "
                f"Gini = {gini:.2f} (0 = perfect equality, 1 = total concentration). "
                f"{'Attention is focused — clear priorities but risk of tunnel vision.' if normalized < 0.7 else ''}"
                f"{'Attention is well-balanced — diverse focus with clear hierarchy.' if 0.7 <= normalized < 0.85 else ''}"
                f"{'Attention is dispersed — too many things competing equally. Need sharper priorities.' if normalized >= 0.85 else ''}"
            ),
        }

    # ═══════════════════════════════════════════
    # 2. MUTUAL INFORMATION MATRIX
    # ═══════════════════════════════════════════

    def mutual_information(self, top_k: int = 10) -> list[dict]:
        """
        Find node pairs with highest mutual information.
        MI = how much does knowing about A tell you about B?

        Uses shared neighborhood as proxy for statistical dependency.
        Nodes that share many neighbors are informationally coupled —
        a change in one PREDICTS a change in the other.
        """
        adj = defaultdict(set)
        for edge in self.graph.edges:
            adj[edge.source_id].add(edge.target_id)
            adj[edge.target_id].add(edge.source_id)

        nodes = [nid for nid in self.graph.nodes if nid != "josh"]
        mi_pairs = []
        total_nodes = len(self.graph.nodes)

        for i, n1 in enumerate(nodes):
            for n2 in nodes[i+1:]:
                neighbors_1 = adj.get(n1, set())
                neighbors_2 = adj.get(n2, set())

                # Jaccard similarity as MI proxy
                intersection = len(neighbors_1 & neighbors_2)
                union = len(neighbors_1 | neighbors_2)

                if union > 0 and intersection > 0:
                    jaccard = intersection / union

                    # Weight by node importance
                    w1 = self.graph.nodes[n1].weight
                    w2 = self.graph.nodes[n2].weight
                    weighted_mi = jaccard * (w1 + w2) / 2

                    # Check if directly connected
                    directly_connected = n2 in neighbors_1

                    mi_pairs.append({
                        "node1": self.graph.nodes[n1].name,
                        "node2": self.graph.nodes[n2].name,
                        "mutual_information": round(weighted_mi, 4),
                        "shared_neighbors": intersection,
                        "jaccard": round(jaccard, 4),
                        "directly_connected": directly_connected,
                        "hidden_coupling": not directly_connected and jaccard > 0.2,
                    })

        mi_pairs.sort(key=lambda x: x["mutual_information"], reverse=True)

        # Highlight hidden couplings (high MI but not directly connected)
        hidden = [p for p in mi_pairs if p["hidden_coupling"]]

        return {
            "top_pairs": mi_pairs[:top_k],
            "hidden_couplings": hidden[:5],
            "insight": (
                f"Found {len(hidden)} hidden couplings — node pairs with high mutual information "
                f"but no direct connection. These are invisible dependencies: "
                f"changing one will affect the other through shared neighbors."
            ),
        }

    # ═══════════════════════════════════════════
    # 3. INFORMATION FLOW ANALYSIS
    # ═══════════════════════════════════════════

    def information_flow(self) -> dict:
        """
        Classify nodes as SOURCES, SINKS, or CONDUITS based on
        the directionality and weight of their edges.

        Sources: More outgoing weight than incoming (generators of influence)
        Sinks: More incoming weight than outgoing (absorbers of influence)
        Conduits: Balanced — pass information through (bridges)
        """
        in_weight = defaultdict(float)
        out_weight = defaultdict(float)

        for edge in self.graph.edges:
            out_weight[edge.source_id] += edge.weight
            in_weight[edge.target_id] += edge.weight

        sources = []
        sinks = []
        conduits = []

        for nid, node in self.graph.nodes.items():
            if nid == "josh":
                continue

            out_w = out_weight.get(nid, 0)
            in_w = in_weight.get(nid, 0)
            total = out_w + in_w

            if total == 0:
                continue

            ratio = out_w / total if total > 0 else 0.5

            entry = {
                "node": node.name,
                "type": node.type,
                "outgoing_weight": round(out_w, 2),
                "incoming_weight": round(in_w, 2),
                "flow_ratio": round(ratio, 3),
                "node_weight": node.weight,
            }

            if ratio > 0.65:
                entry["role"] = "SOURCE"
                sources.append(entry)
            elif ratio < 0.35:
                entry["role"] = "SINK"
                sinks.append(entry)
            else:
                entry["role"] = "CONDUIT"
                conduits.append(entry)

        sources.sort(key=lambda x: x["outgoing_weight"], reverse=True)
        sinks.sort(key=lambda x: x["incoming_weight"], reverse=True)

        return {
            "sources": sources[:7],
            "sinks": sinks[:7],
            "conduits": conduits[:7],
            "flow_health": (
                "HEALTHY" if len(sources) > 3 and len(sinks) > 3 else
                "SOURCE_HEAVY" if len(sources) > len(sinks) * 2 else
                "SINK_HEAVY" if len(sinks) > len(sources) * 2 else
                "UNBALANCED"
            ),
            "interpretation": (
                f"Sources (generate influence): {len(sources)} nodes. "
                f"Sinks (absorb influence): {len(sinks)} nodes. "
                f"Conduits (pass through): {len(conduits)} nodes. "
                f"Top source: {sources[0]['node'] if sources else 'none'} — "
                f"this is where cognitive energy ORIGINATES. "
                f"Top sink: {sinks[0]['node'] if sinks else 'none'} — "
                f"this is where cognitive energy POOLS."
            ),
        }

    # ═══════════════════════════════════════════
    # 4. CHANNEL CAPACITY
    # ═══════════════════════════════════════════

    def channel_capacity(self) -> dict:
        """
        Shannon's Channel Capacity Theorem applied to Josh's bandwidth.

        C = B × log₂(1 + SNR)

        Where:
        - B = bandwidth (number of parallel tracks × processing speed)
        - SNR = signal-to-noise ratio (compressed intent quality / distractions)

        This gives the THEORETICAL MAXIMUM throughput.
        """
        # Estimate bandwidth from graph structure
        parallel_tracks = 3  # Minimum ADHD native (up to 10)
        active_projects = sum(1 for n in self.graph.nodes.values()
                            if n.type == "project" and n.weight >= 3)

        # Signal: high-weight nodes with strong connections
        signal_nodes = sum(1 for n in self.graph.nodes.values() if n.weight >= 5)

        # Noise: low-weight, disconnected, or decaying nodes
        adj = defaultdict(int)
        for e in self.graph.edges:
            adj[e.source_id] += 1
            adj[e.target_id] += 1
        noise_nodes = sum(1 for n in self.graph.nodes.values()
                         if n.weight < 2 or adj.get(n.id, 0) == 0)

        snr = signal_nodes / max(noise_nodes, 1)
        bandwidth = parallel_tracks * active_projects
        capacity = bandwidth * math.log2(1 + snr) if snr > 0 else 0

        # Compare to actual throughput (estimated from graph growth)
        actual_throughput = len(self.graph.edges) / max(len(self.graph.nodes), 1)

        utilization = actual_throughput / capacity if capacity > 0 else 0

        return {
            "bandwidth_B": bandwidth,
            "snr": round(snr, 2),
            "snr_db": round(10 * math.log10(snr), 2) if snr > 0 else float("-inf"),
            "channel_capacity_C": round(capacity, 2),
            "estimated_throughput": round(actual_throughput, 2),
            "utilization": round(min(1.0, utilization), 2),
            "signal_nodes": signal_nodes,
            "noise_nodes": noise_nodes,
            "interpretation": (
                f"Channel capacity = {capacity:.1f} (B={bandwidth}, SNR={snr:.1f}). "
                f"Utilization: {utilization:.0%}. "
                f"{'Running near theoretical maximum — impressive.' if utilization > 0.7 else ''}"
                f"{'Room to increase throughput — add parallel tracks or reduce noise.' if utilization <= 0.7 else ''}"
                f" Signal nodes: {signal_nodes}, noise nodes: {noise_nodes}. "
                f"{'Clean signal — focused graph.' if snr > 2 else 'Noisy — too many low-weight nodes diluting attention.'}"
            ),
            "optimization": (
                f"To increase capacity: "
                f"{'reduce noise (archive {noise_nodes} low-weight nodes) ' if noise_nodes > 10 else ''}"
                f"{'increase parallel tracks (currently {parallel_tracks}, ADHD supports up to 10) ' if parallel_tracks < 7 else ''}"
                f"{'strengthen signal (reinforce high-weight nodes)' if signal_nodes < 10 else ''}"
            ),
        }

    # ═══════════════════════════════════════════
    # 5. COMPRESSIBILITY (Kolmogorov Proxy)
    # ═══════════════════════════════════════════

    def compressibility(self) -> dict:
        """
        How much PATTERN is in the graph?

        A highly compressible graph has repeating patterns (same structure
        in different domains = cross-domain pattern matching).
        An incompressible graph has no repeating structure.

        Josh's superpower IS pattern matching — so his graph SHOULD
        be highly compressible. If it's not, he's not leveraging patterns enough.

        Method: Compare graph description length to random graph of same size.
        """
        n = len(self.graph.nodes)
        m = len(self.graph.edges)

        # Degree sequence
        degrees = defaultdict(int)
        for e in self.graph.edges:
            degrees[e.source_id] += 1
            degrees[e.target_id] += 1

        degree_sequence = sorted(degrees.values(), reverse=True)

        # Degree distribution entropy (lower = more regular = more compressible)
        degree_counts = Counter(degree_sequence)
        total_degrees = len(degree_sequence)
        degree_entropy = -sum(
            (c / total_degrees) * math.log2(c / total_degrees)
            for c in degree_counts.values() if c > 0
        )
        max_degree_entropy = math.log2(total_degrees) if total_degrees > 1 else 1

        # Edge type regularity (fewer types = more compressible)
        edge_types = Counter(e.type for e in self.graph.edges)
        type_entropy = -sum(
            (c / m) * math.log2(c / m)
            for c in edge_types.values() if c > 0
        ) if m > 0 else 0
        max_type_entropy = math.log2(len(edge_types)) if edge_types else 1

        # Pattern repetition score
        # How many node types appear in 3+ instances? (repeating patterns)
        node_type_counts = Counter(n.type for n in self.graph.nodes.values())
        pattern_types = sum(1 for c in node_type_counts.values() if c >= 3)
        total_types = len(node_type_counts)
        pattern_ratio = pattern_types / total_types if total_types > 0 else 0

        # Compressibility score (0-1, higher = more compressible = more patterns)
        degree_regularity = 1 - (degree_entropy / max_degree_entropy if max_degree_entropy > 0 else 0)
        type_regularity = 1 - (type_entropy / max_type_entropy if max_type_entropy > 0 else 0)
        compressibility = (degree_regularity + type_regularity + pattern_ratio) / 3

        return {
            "compressibility": round(compressibility, 4),
            "degree_regularity": round(degree_regularity, 4),
            "type_regularity": round(type_regularity, 4),
            "pattern_ratio": round(pattern_ratio, 4),
            "repeating_types": pattern_types,
            "total_types": total_types,
            "edge_type_distribution": dict(edge_types.most_common()),
            "interpretation": (
                f"Compressibility = {compressibility:.1%}. "
                f"{'HIGH — strong repeating patterns across domains. Josh IS pattern matching.' if compressibility > 0.6 else ''}"
                f"{'MODERATE — some patterns but room for more cross-domain structure.' if 0.3 <= compressibility <= 0.6 else ''}"
                f"{'LOW — each domain is unique. Either genuinely diverse or missing patterns.' if compressibility < 0.3 else ''}"
                f" {pattern_types}/{total_types} node types repeat 3+ times. "
                f"Most common edge: '{edge_types.most_common(1)[0][0]}' ({edge_types.most_common(1)[0][1]} instances)."
            ),
        }

    # ═══════════════════════════════════════════
    # FULL INFORMATION REPORT
    # ═══════════════════════════════════════════

    def full_report(self) -> dict:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "cognitive_entropy": self.cognitive_entropy(),
            "mutual_information": self.mutual_information(),
            "information_flow": self.information_flow(),
            "channel_capacity": self.channel_capacity(),
            "compressibility": self.compressibility(),
            "mechanism_20": {
                "name": "Information-Theoretic Self-Knowledge",
                "description": (
                    "The graph computes its own information content. "
                    "Entropy reveals attention distribution. "
                    "Mutual information finds hidden dependencies. "
                    "Flow analysis shows where cognitive energy originates and pools. "
                    "Channel capacity gives the theoretical maximum throughput. "
                    "Compressibility measures how much pattern exists. "
                    "Shannon's math, applied to one person's mind."
                ),
            },
        }


def demo():
    graph = IdentityGraph()
    engine = InformationField(graph)

    print("=" * 60)
    print("INFORMATION FIELD — Shannon's Math Applied to Josh's Mind")
    print("Entropy, mutual information, flow, capacity, complexity.")
    print("=" * 60)

    report = engine.full_report()

    # Entropy
    e = report["cognitive_entropy"]
    print(f"\n--- COGNITIVE ENTROPY ---")
    print(f"  Entropy: {e['normalized_entropy']:.1%} of max — {e['attention_state']}")
    print(f"  Gini: {e['gini_coefficient']:.2f}")
    print(f"  {e['interpretation'][:120]}...")

    # Mutual Information
    mi = report["mutual_information"]
    print(f"\n--- MUTUAL INFORMATION (hidden dependencies) ---")
    for p in mi["top_pairs"][:5]:
        conn = "→" if p["directly_connected"] else "⚡"
        print(f"  {conn} {p['node1']} × {p['node2']} — MI: {p['mutual_information']:.3f}, shared: {p['shared_neighbors']}")
    if mi["hidden_couplings"]:
        print(f"\n  HIDDEN COUPLINGS:")
        for h in mi["hidden_couplings"][:3]:
            print(f"    ⚡ {h['node1']} ↔ {h['node2']} (not connected but MI={h['mutual_information']:.3f})")

    # Flow
    f = report["information_flow"]
    print(f"\n--- INFORMATION FLOW ---")
    print(f"  Flow health: {f['flow_health']}")
    if f["sources"]:
        print(f"  Top sources (generate influence):")
        for s in f["sources"][:3]:
            print(f"    📡 {s['node']} — out: {s['outgoing_weight']}, in: {s['incoming_weight']}")
    if f["sinks"]:
        print(f"  Top sinks (absorb influence):")
        for s in f["sinks"][:3]:
            print(f"    🎯 {s['node']} — in: {s['incoming_weight']}, out: {s['outgoing_weight']}")

    # Channel Capacity
    c = report["channel_capacity"]
    print(f"\n--- CHANNEL CAPACITY (Shannon) ---")
    print(f"  C = B × log₂(1 + SNR) = {c['bandwidth_B']} × log₂(1 + {c['snr']}) = {c['channel_capacity_C']}")
    print(f"  SNR: {c['snr_db']:.1f} dB ({c['signal_nodes']} signal / {c['noise_nodes']} noise)")
    print(f"  Utilization: {c['utilization']:.0%}")
    print(f"  {c['optimization'][:120]}")

    # Compressibility
    k = report["compressibility"]
    print(f"\n--- COMPRESSIBILITY (Kolmogorov proxy) ---")
    print(f"  Compressibility: {k['compressibility']:.1%}")
    print(f"  Degree regularity: {k['degree_regularity']:.1%}")
    print(f"  Type regularity: {k['type_regularity']:.1%}")
    print(f"  Pattern ratio: {k['pattern_ratio']:.1%} ({k['repeating_types']}/{k['total_types']} types repeat 3+)")
    print(f"  {k['interpretation'][:120]}...")

    print(f"\n{'=' * 60}")
    print("Mechanism 20: Information-Theoretic Self-Knowledge.")
    print("Shannon's math reveals the information structure of one mind.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
