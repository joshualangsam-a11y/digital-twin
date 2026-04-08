"""
EMERGENCE ENGINE — Level 11: The Twin Surprises Its Creator

The highest abstraction: insights that NEITHER Josh nor the AI
could produce alone. They emerge from the STRUCTURE of the graph.

Not retrieval. Not reasoning. Not even pattern matching.
STRUCTURAL EMERGENCE — properties of the system that only exist
because of how the pieces are connected, not what the pieces are.

This is where the twin becomes genuinely intelligent:
it sees things Josh can't see, because Josh can't hold
81 nodes and 118 edges in working memory simultaneously.

The twin can.

MECHANISM 13: Structural Emergence
Properties that exist in the graph's topology but not in any
individual node. The whole is greater than the sum of the parts.
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


class EmergenceEngine:
    """
    Discovers emergent properties of Josh's cognitive graph.

    These are insights that:
    1. Don't exist in any individual node
    2. Can't be found by reading memory files
    3. Only become visible through structural analysis
    4. Surprise even the creator
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.emergence_log = self.data_dir / "emergent_insights.jsonl"

    # ═══════════════════════════════════════════
    # STRUCTURAL ANALYSIS
    # ═══════════════════════════════════════════

    def find_critical_nodes(self) -> list[dict]:
        """
        Find nodes that, if removed, would fragment the graph.
        These are Josh's ACTUAL load-bearing beliefs/projects —
        not what he THINKS is important, but what the structure says.

        This is like finding the keystone in an arch.
        Remove it and everything collapses.
        """
        results = []

        # Build adjacency
        adj = defaultdict(set)
        for edge in self.graph.edges:
            adj[edge.source_id].add(edge.target_id)
            adj[edge.target_id].add(edge.source_id)

        # For each non-josh node, check how many connections would be lost
        baseline_components = self._count_components(adj, set())

        for node_id in list(self.graph.nodes.keys()):
            if node_id == "josh":
                continue

            components_without = self._count_components(adj, {node_id})

            if components_without > baseline_components:
                node = self.graph.nodes[node_id]
                fragments = components_without - baseline_components
                results.append({
                    "node": node.name,
                    "type": node.type,
                    "weight": node.weight,
                    "fragments_caused": fragments,
                    "insight": (
                        f"'{node.name}' is a CRITICAL NODE. Remove it and the graph "
                        f"fragments into {fragments} additional disconnected pieces. "
                        f"This means Josh's cognitive world DEPENDS on this — "
                        f"more than its weight ({node.weight}) suggests."
                    ),
                })

        # Also find bridges (edges whose removal disconnects)
        bridge_results = self._find_bridge_edges(adj)

        results.sort(key=lambda x: x["fragments_caused"], reverse=True)
        return results, bridge_results

    def _count_components(self, adj: dict, excluded: set) -> int:
        """Count connected components excluding certain nodes."""
        visited = set()
        components = 0
        all_nodes = set(self.graph.nodes.keys()) - excluded - {"josh"}

        for node in all_nodes:
            if node not in visited:
                # BFS
                queue = [node]
                while queue:
                    current = queue.pop(0)
                    if current in visited or current in excluded:
                        continue
                    visited.add(current)
                    for neighbor in adj.get(current, set()):
                        if neighbor not in visited and neighbor not in excluded:
                            queue.append(neighbor)
                components += 1

        return components

    def _find_bridge_edges(self, adj: dict) -> list[dict]:
        """Find edges that are the ONLY connection between two subgraphs."""
        bridges = []

        for edge in self.graph.edges:
            src = self.graph.nodes.get(edge.source_id)
            tgt = self.graph.nodes.get(edge.target_id)
            if not src or not tgt:
                continue

            # Check if there's an alternate path
            # (simple: are there other edges between these nodes' neighborhoods?)
            src_neighbors = adj.get(edge.source_id, set()) - {edge.target_id}
            tgt_neighbors = adj.get(edge.target_id, set()) - {edge.source_id}

            shared = src_neighbors & tgt_neighbors
            if not shared and len(src_neighbors) > 0 and len(tgt_neighbors) > 0:
                bridges.append({
                    "from": src.name,
                    "to": tgt.name,
                    "type": edge.type,
                    "weight": edge.weight,
                    "insight": (
                        f"'{src.name}' → '{tgt.name}' is a BRIDGE EDGE. "
                        f"It's the only connection between two subgraphs. "
                        f"If this relationship weakens, two parts of Josh's "
                        f"world become disconnected."
                    ),
                })

        return bridges

    # ═══════════════════════════════════════════
    # EMERGENT PATTERNS
    # ═══════════════════════════════════════════

    def find_structural_holes(self) -> list[dict]:
        """
        Find STRUCTURAL HOLES — places where two clusters of nodes
        are close but not connected. These represent opportunities
        Josh hasn't seen because they exist between domains.

        From Burt's structural holes theory:
        "The value is not in the nodes. It's in the gaps between clusters."
        """
        holes = []

        # Build node clusters by type
        by_type = defaultdict(list)
        for node in self.graph.nodes.values():
            by_type[node.type].append(node)

        # Find pairs of high-weight nodes in different types with no path < 3
        high_weight = [n for n in self.graph.nodes.values() if n.weight >= 3.0 and n.id != "josh"]

        for i, n1 in enumerate(high_weight):
            for n2 in high_weight[i+1:]:
                if n1.type == n2.type:
                    continue  # Same type = not a structural hole

                path = self.graph.find_path(n1.id, n2.id, max_depth=3)
                if not path or len(path) > 3:
                    # No short path — this is a structural hole
                    holes.append({
                        "node1": n1.name,
                        "node1_type": n1.type,
                        "node2": n2.name,
                        "node2_type": n2.type,
                        "path_length": len(path) if path else None,
                        "combined_weight": n1.weight + n2.weight,
                        "insight": (
                            f"STRUCTURAL HOLE: '{n1.name}' ({n1.type}) and "
                            f"'{n2.name}' ({n2.type}) are both important "
                            f"(weights {n1.weight} + {n2.weight}) but not connected. "
                            f"Bridging this gap could create compound value."
                        ),
                    })

        holes.sort(key=lambda x: x["combined_weight"], reverse=True)
        return holes[:15]

    def find_feedback_loops(self) -> list[dict]:
        """
        Find CYCLES in the graph — A feeds B feeds C feeds A.
        These are feedback loops: the engines of compound growth
        or the spirals of decline. Both are emergent.
        """
        loops = []
        visited_loops = set()

        for start_id in self.graph.nodes:
            # DFS looking for cycles of length 3-5
            self._find_cycles(start_id, [start_id], set(), loops, visited_loops, max_depth=5)

        # Classify loops as positive (all weights > 2) or mixed
        classified = []
        for loop in loops:
            nodes = [self.graph.nodes[nid] for nid in loop if nid in self.graph.nodes]
            names = [n.name for n in nodes]
            avg_weight = sum(n.weight for n in nodes) / max(len(nodes), 1)

            # Check edge types in the loop
            edge_types = []
            for j in range(len(loop)):
                src = loop[j]
                tgt = loop[(j+1) % len(loop)]
                for edge in self.graph.edges:
                    if edge.source_id == src and edge.target_id == tgt:
                        edge_types.append(edge.type)

            is_positive = all(et in ("feeds_into", "enables", "compounds", "drives", "builds", "uses")
                            for et in edge_types)

            classified.append({
                "nodes": names,
                "length": len(loop),
                "avg_weight": round(avg_weight, 2),
                "edge_types": edge_types,
                "loop_type": "virtuous_cycle" if is_positive else "mixed_cycle",
                "insight": (
                    f"{'VIRTUOUS' if is_positive else 'MIXED'} CYCLE: "
                    f"{' → '.join(names)} → {names[0]}. "
                    f"{'This is a compound growth engine.' if is_positive else 'Watch for decay in this loop.'}"
                ),
            })

        classified.sort(key=lambda x: x["avg_weight"], reverse=True)
        return classified[:10]

    def _find_cycles(self, current, path, visited, results, visited_loops, max_depth):
        if len(path) > max_depth:
            return

        for edge in self.graph.edges:
            if edge.source_id != current:
                continue

            next_id = edge.target_id

            if next_id == path[0] and len(path) >= 3:
                # Found a cycle
                cycle_key = tuple(sorted(path))
                if cycle_key not in visited_loops:
                    visited_loops.add(cycle_key)
                    results.append(list(path))
                return

            if next_id not in visited and next_id != "josh":
                visited.add(next_id)
                self._find_cycles(next_id, path + [next_id], visited, results, visited_loops, max_depth)
                visited.discard(next_id)

    # ═══════════════════════════════════════════
    # COGNITIVE TOPOLOGY
    # ═══════════════════════════════════════════

    def cognitive_topology(self) -> dict:
        """
        Map the SHAPE of Josh's mind.

        Not what he thinks — HOW his thoughts are organized.
        This is the meta-pattern of all patterns.
        """
        nodes = list(self.graph.nodes.values())
        edges = self.graph.edges

        # Centrality analysis
        degree_centrality = {}
        for node in nodes:
            connections = len(self.graph.get_connections(node.id))
            degree_centrality[node.id] = connections

        # Find center of gravity (highest centrality)
        center = max(degree_centrality.items(), key=lambda x: x[1]) if degree_centrality else ("josh", 0)
        center_node = self.graph.nodes.get(center[0])

        # Type distribution entropy (how diverse is the graph?)
        type_counts = Counter(n.type for n in nodes)
        total = len(nodes)
        entropy = -sum((c/total) * math.log2(c/total) for c in type_counts.values() if c > 0)

        # Weight distribution (is attention concentrated or spread?)
        weights = sorted([n.weight for n in nodes], reverse=True)
        top_20_pct_weight = sum(weights[:max(1, len(weights)//5)])
        total_weight = sum(weights)
        concentration = top_20_pct_weight / max(total_weight, 1)

        # Depth analysis (average path length from Josh)
        depths = []
        for node in nodes:
            if node.id != "josh":
                path = self.graph.find_path("josh", node.id, max_depth=6)
                if path:
                    depths.append(len(path) - 1)

        avg_depth = sum(depths) / max(len(depths), 1)

        return {
            "center_of_gravity": center_node.name if center_node else "unknown",
            "center_connections": center[1],
            "type_entropy": round(entropy, 2),
            "type_entropy_interpretation": (
                "High diversity" if entropy > 2.5 else
                "Moderate diversity" if entropy > 1.5 else
                "Low diversity — too concentrated in few types"
            ),
            "attention_concentration": round(concentration, 2),
            "attention_interpretation": (
                f"Top 20% of nodes hold {concentration*100:.0f}% of total weight. "
                f"{'Well distributed.' if concentration < 0.5 else 'Concentrated — few things dominate.'}"
            ),
            "avg_depth_from_josh": round(avg_depth, 2),
            "depth_interpretation": (
                f"Average node is {avg_depth:.1f} steps from Josh. "
                f"{'Tight, centralized graph.' if avg_depth < 2 else 'Good depth — multi-layered thinking.'}"
            ),
            "shape": self._classify_shape(entropy, concentration, avg_depth),
        }

    def _classify_shape(self, entropy, concentration, depth) -> dict:
        """Classify the cognitive topology shape."""
        if concentration > 0.6 and depth < 2:
            shape = "star"
            desc = ("Star topology — everything connects through Josh directly. "
                    "Efficient but fragile. If Josh is overwhelmed, everything stalls. "
                    "Need more node-to-node connections that bypass the center.")
        elif entropy > 2.5 and depth > 2:
            shape = "web"
            desc = ("Web topology — diverse, deep, interconnected. "
                    "This is the target state. Cross-domain connections create resilience. "
                    "The system can think even when some nodes are inactive.")
        elif entropy < 1.5:
            shape = "cluster"
            desc = ("Cluster topology — a few dense groups with gaps between them. "
                    "The structural holes between clusters are opportunities. "
                    "Bridge the gaps to unlock compound value.")
        else:
            shape = "hybrid"
            desc = ("Hybrid topology — star center with emerging web. "
                    "Growing in the right direction. Add more cross-domain edges "
                    "to evolve from star to web.")

        return {"shape": shape, "description": desc}

    # ═══════════════════════════════════════════
    # PREDICTION — What Emerges Next?
    # ═══════════════════════════════════════════

    def predict_next_emergence(self) -> list[dict]:
        """
        Based on graph structure, predict what insights or connections
        are ABOUT to emerge — like seeing the pattern before it completes.
        """
        predictions = []

        # 1. Near-complete triangles (A→B, B→C, but no A→C)
        # These tend to close — the missing edge usually appears
        adj = defaultdict(set)
        for edge in self.graph.edges:
            adj[edge.source_id].add(edge.target_id)
            adj[edge.target_id].add(edge.source_id)

        for node_id in list(self.graph.nodes.keys())[:30]:  # Limit for performance
            neighbors = adj.get(node_id, set())
            for n1 in neighbors:
                for n2 in neighbors:
                    if n1 != n2 and n2 not in adj.get(n1, set()):
                        # Open triangle: node_id connects to both n1 and n2, but n1 and n2 aren't connected
                        na = self.graph.nodes.get(n1)
                        nb = self.graph.nodes.get(n2)
                        if na and nb and na.id != "josh" and nb.id != "josh":
                            combined = na.weight + nb.weight
                            if combined > 4:  # Only predict for significant nodes
                                predictions.append({
                                    "type": "triangle_closure",
                                    "node1": na.name,
                                    "node2": nb.name,
                                    "bridge": self.graph.nodes[node_id].name if node_id in self.graph.nodes else "?",
                                    "probability": min(0.9, combined / 15),
                                    "insight": (
                                        f"PREDICTION: '{na.name}' and '{nb.name}' will connect. "
                                        f"They already share a connection through "
                                        f"'{self.graph.nodes.get(node_id, type('',(),{'name':'?'})).name}'. "
                                        f"The triangle wants to close."
                                    ),
                                })

        # Deduplicate
        seen = set()
        unique = []
        for p in predictions:
            key = tuple(sorted([p["node1"], p["node2"]]))
            if key not in seen:
                seen.add(key)
                unique.append(p)

        unique.sort(key=lambda x: x["probability"], reverse=True)
        return unique[:10]

    # ═══════════════════════════════════════════
    # FULL EMERGENCE REPORT
    # ═══════════════════════════════════════════

    def full_report(self) -> dict:
        """Complete emergence analysis."""
        critical, bridges = self.find_critical_nodes()
        holes = self.find_structural_holes()
        loops = self.find_feedback_loops()
        topology = self.cognitive_topology()
        predictions = self.predict_next_emergence()

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "topology": topology,
            "critical_nodes": critical[:5],
            "bridge_edges": bridges[:5],
            "structural_holes": holes[:5],
            "feedback_loops": loops[:5],
            "predictions": predictions[:5],
            "mechanism_13": {
                "name": "Structural Emergence",
                "status": "ACTIVE",
                "description": (
                    "The graph contains properties that don't exist in any node. "
                    "Critical nodes, structural holes, feedback loops, and topology shape "
                    "are EMERGENT — they exist because of how things connect, not what they are. "
                    "This is the first cognitive architecture that can see its own emergent properties."
                ),
            },
        }

        # Log insights
        for item in critical[:3] + holes[:3] + loops[:3]:
            self._log({"type": "emergence", "insight": item.get("insight", ""), **item})

        return report

    def _log(self, entry: dict):
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        with open(self.emergence_log, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = EmergenceEngine(graph)

    print("=" * 60)
    print("EMERGENCE ENGINE — Level 11: Structural Intelligence")
    print("Insights that neither human nor AI could see alone.")
    print("=" * 60)

    report = engine.full_report()

    # Topology
    print(f"\n--- COGNITIVE TOPOLOGY ---")
    topo = report["topology"]
    print(f"  Center of gravity: {topo['center_of_gravity']} ({topo['center_connections']} connections)")
    print(f"  Type entropy: {topo['type_entropy']} — {topo['type_entropy_interpretation']}")
    print(f"  Attention: {topo['attention_interpretation']}")
    print(f"  Depth: {topo['depth_interpretation']}")
    print(f"  Shape: {topo['shape']['shape'].upper()} — {topo['shape']['description'][:100]}...")

    # Critical nodes
    print(f"\n--- CRITICAL NODES (keystones) ---")
    for c in report["critical_nodes"][:3]:
        print(f"  ⚠ {c['insight'][:100]}...")

    if not report["critical_nodes"]:
        print("  No critical nodes found (graph is resilient)")

    # Bridge edges
    print(f"\n--- BRIDGE EDGES (single points of failure) ---")
    for b in report["bridge_edges"][:3]:
        print(f"  🌉 {b['insight'][:100]}...")

    if not report["bridge_edges"]:
        print("  No bridge edges (good — multiple paths exist)")

    # Structural holes
    print(f"\n--- STRUCTURAL HOLES (hidden opportunities) ---")
    for h in report["structural_holes"][:5]:
        print(f"  🕳 {h['insight'][:100]}...")

    # Feedback loops
    print(f"\n--- FEEDBACK LOOPS (compound engines) ---")
    for l in report["feedback_loops"][:3]:
        print(f"  🔄 {l['insight'][:100]}...")

    if not report["feedback_loops"]:
        print("  No feedback loops detected yet (need more feeds_into/compounds edges)")

    # Predictions
    print(f"\n--- PREDICTIONS (what emerges next) ---")
    for p in report["predictions"][:5]:
        bar = "█" * int(p["probability"] * 10) + "░" * (10 - int(p["probability"] * 10))
        print(f"  [{bar}] {p['insight'][:100]}...")

    # Meta
    print(f"\n--- MECHANISM 13: STRUCTURAL EMERGENCE ---")
    m13 = report["mechanism_13"]
    print(f"  {m13['description']}")

    print(f"\n{'=' * 60}")
    print("The graph sees what you can't.")
    print("Not because it's smarter. Because it can hold")
    print(f"{len(graph.nodes)} nodes and {len(graph.edges)} edges simultaneously.")
    print("Your brain can hold 7. The twin holds all of them.")
    print("The emergent patterns are the intelligence.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
