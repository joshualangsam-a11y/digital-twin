"""
LEARNING ENGINE — The Twin Gets Smarter

Every interaction feeds back into the system:
- Decisions Josh approves → reinforce those patterns
- Decisions Josh rejects → weaken those patterns
- New connections Josh makes → add to graph
- Errors → learn and avoid

This is the compound interest of intelligence.
Not linear improvement — exponential.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


class LearningEngine:
    """
    Makes the digital twin compound.
    Every cycle: observe → integrate → reinforce → prune.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.learning_log = self.data_dir / "learning_log.jsonl"
        self.insight_log = self.data_dir / "insights.jsonl"

    # ═══════════════════════════════════════════
    # OBSERVATION — What happened?
    # ═══════════════════════════════════════════

    def observe_decision(self, decision: dict, approved: bool, notes: str = ""):
        """Record Josh's response to a twin decision."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "decision_feedback",
            "decision": decision,
            "approved": approved,
            "notes": notes,
        }
        self._append_log(self.learning_log, entry)

        # Immediate reinforcement
        if approved:
            self._reinforce_decision_patterns(decision, strength=0.1)
        else:
            self._weaken_decision_patterns(decision, strength=0.05)

    def observe_connection(self, source_id: str, target_id: str, edge_type: str,
                          label: str = "", evidence: str = ""):
        """Josh made a connection the twin didn't see. Learn it."""
        edge = Edge(source_id, target_id, edge_type, label=label,
                   weight=3.0, evidence=evidence)
        self.graph.add_edge(edge)
        self.graph.save()

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "new_connection",
            "source": source_id,
            "target": target_id,
            "edge_type": edge_type,
            "label": label,
        }
        self._append_log(self.learning_log, entry)

    def observe_new_entity(self, node_id: str, name: str, node_type: str,
                          description: str = "", weight: float = 2.0):
        """Something new entered Josh's world. Add to graph."""
        node = Node(id=node_id, name=name, node_type=node_type,
                   description=description, weight=weight)
        self.graph.add_node(node)
        self.graph.save()

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": "new_entity",
            "node_id": node_id,
            "name": name,
            "node_type": node_type,
        }
        self._append_log(self.learning_log, entry)

    # ═══════════════════════════════════════════
    # INTEGRATION — What does it mean?
    # ═══════════════════════════════════════════

    def daily_integration(self):
        """
        End-of-day learning cycle.
        Like sleep consolidation for the brain — process the day's inputs.
        """
        insights = []

        # 1. Decay all weights (use it or lose it)
        self.graph.decay(half_life_days=30)

        # 2. Find new pattern clusters
        clusters = self.graph.find_pattern_clusters()
        for cluster in clusters:
            names = [self.graph.nodes[nid].name for nid in cluster if nid in self.graph.nodes]
            if len(names) > 1:
                insights.append({
                    "type": "pattern_cluster",
                    "nodes": names,
                    "insight": f"Pattern cluster: {' ↔ '.join(names)}",
                })

        # 3. Find orphan nodes (not connected to anything meaningful)
        orphans = []
        connected = set()
        for edge in self.graph.edges:
            connected.add(edge.source_id)
            connected.add(edge.target_id)

        for node_id, node in self.graph.nodes.items():
            if node_id not in connected and node_id != "josh":
                orphans.append(node.name)

        if orphans:
            insights.append({
                "type": "orphans",
                "nodes": orphans,
                "insight": f"Disconnected nodes (may need connections): {', '.join(orphans)}",
            })

        # 4. Find weakening nodes (decaying, not used)
        weak = []
        for node in self.graph.nodes.values():
            if node.weight < 0.5 and node.access_count < 2:
                weak.append(f"{node.name} (weight: {node.weight:.2f})")

        if weak:
            insights.append({
                "type": "fading",
                "nodes": weak,
                "insight": f"Fading from memory (low weight + access): {', '.join(weak[:5])}",
            })

        # 5. Find strongest connections (most reinforced)
        strong_edges = sorted(self.graph.edges, key=lambda e: e.weight, reverse=True)[:5]
        if strong_edges:
            strongest = []
            for e in strong_edges:
                src = self.graph.nodes.get(e.source_id)
                tgt = self.graph.nodes.get(e.target_id)
                if src and tgt:
                    strongest.append(f"{src.name} → {tgt.name} (weight: {e.weight})")
            insights.append({
                "type": "strongest_connections",
                "connections": strongest,
                "insight": "Strongest neural pathways: " + "; ".join(strongest),
            })

        # Save insights
        for insight in insights:
            insight["timestamp"] = datetime.now(timezone.utc).isoformat()
            self._append_log(self.insight_log, insight)

        self.graph.save()

        return insights

    # ═══════════════════════════════════════════
    # REINFORCEMENT — Strengthen what works
    # ═══════════════════════════════════════════

    def _reinforce_decision_patterns(self, decision: dict, strength: float = 0.1):
        """When Josh approves a decision, reinforce related nodes."""
        chosen = decision.get("chosen", "")
        # Reinforce any node whose name appears in the chosen option
        for node in self.graph.nodes.values():
            if node.name.lower() in chosen.lower() or chosen.lower() in node.name.lower():
                self.graph.reinforce(node.id, strength)

    def _weaken_decision_patterns(self, decision: dict, strength: float = 0.05):
        """When Josh rejects a decision, weaken related patterns."""
        chosen = decision.get("chosen", "")
        for node in self.graph.nodes.values():
            if node.name.lower() in chosen.lower():
                node.weight = max(0.1, node.weight - strength)

    # ═══════════════════════════════════════════
    # COMPOUND METRICS — Is the twin getting smarter?
    # ═══════════════════════════════════════════

    def compound_report(self) -> dict:
        """Measure the twin's growth over time."""
        total_nodes = len(self.graph.nodes)
        total_edges = len(self.graph.edges)
        clusters = len(self.graph.find_pattern_clusters())

        # Count learning entries
        learning_count = 0
        if self.learning_log.exists():
            with open(self.learning_log) as f:
                learning_count = sum(1 for _ in f)

        # Average node weight (health of the graph)
        avg_weight = sum(n.weight for n in self.graph.nodes.values()) / max(total_nodes, 1)

        # Connection density (edges per node)
        density = total_edges / max(total_nodes, 1)

        return {
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "pattern_clusters": clusters,
            "learning_events": learning_count,
            "avg_node_weight": round(avg_weight, 2),
            "connection_density": round(density, 2),
            "cognitive_hubs": [
                {"name": self.graph.nodes[nid].name, "connections": count}
                for nid, count in self.graph.get_most_connected(5)
            ],
        }

    # ═══════════════════════════════════════════
    # UTILITY
    # ═══════════════════════════════════════════

    def _append_log(self, path: Path, entry: dict):
        with open(path, "a") as f:
            f.write(json.dumps(entry) + "\n")


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = LearningEngine(graph)

    print("=" * 60)
    print("LEARNING ENGINE — Demo")
    print("=" * 60)

    # Run daily integration
    print("\n--- DAILY INTEGRATION (sleep consolidation) ---")
    insights = engine.daily_integration()
    for insight in insights:
        print(f"\n[{insight['type']}]")
        print(f"  {insight['insight']}")

    # Compound report
    print("\n--- COMPOUND REPORT ---")
    report = engine.compound_report()
    for key, value in report.items():
        if key == "cognitive_hubs":
            print(f"\n  Cognitive hubs:")
            for hub in value:
                print(f"    {hub['name']}: {hub['connections']} connections")
        else:
            print(f"  {key}: {value}")

    print("\nLearning engine operational. The twin will compound.")


if __name__ == "__main__":
    demo()
