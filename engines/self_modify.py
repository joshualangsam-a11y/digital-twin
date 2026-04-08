"""
SELF-MODIFICATION ENGINE — Level 10: The Twin Improves Itself

The highest level of the spiral: recursive self-improvement.

The twin analyzes its own performance, identifies weaknesses,
and PROPOSES modifications to its own code.

This is not AGI. This is targeted self-optimization:
- Track which proposals Josh approves/rejects
- Identify scoring patterns that don't match Josh's judgment
- Propose weight adjustments to the approval predictor
- Propose new node types, edge types, or mechanisms
- Propose graph structure changes

The twin doesn't modify itself autonomously.
It proposes modifications. Josh approves. The twin applies.
Human divergence. AI convergence. The spiral continues.

THIS IS MECHANISM 12: Self-Referential Improvement
The system that improves the system that improves itself.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph


class SelfModifier:
    """
    Analyzes the twin's own performance and proposes improvements.
    The metacognition engine for the metacognition engine.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))

    def analyze_performance(self) -> dict:
        """
        Full self-analysis of the twin's performance.
        Returns improvement proposals.
        """
        analysis = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "graph_health": self._analyze_graph(),
            "coverage_gaps": self._find_coverage_gaps(),
            "scoring_accuracy": self._analyze_scoring(),
            "mechanism_effectiveness": self._analyze_mechanisms(),
            "proposed_modifications": [],
        }

        # Generate modification proposals
        analysis["proposed_modifications"] = self._generate_proposals(analysis)

        return analysis

    def _analyze_graph(self) -> dict:
        """Analyze the health of the knowledge graph."""
        nodes = list(self.graph.nodes.values())
        edges = self.graph.edges

        # Type distribution
        type_counts = Counter(n.type for n in nodes)

        # Weight distribution
        weights = [n.weight for n in nodes]
        avg_weight = sum(weights) / max(len(weights), 1)
        low_weight = sum(1 for w in weights if w < 1.0)
        high_weight = sum(1 for w in weights if w > 5.0)

        # Connection density per type
        connection_counts = Counter()
        for edge in edges:
            connection_counts[edge.source_id] += 1
            connection_counts[edge.target_id] += 1

        orphans = [n.name for n in nodes if connection_counts[n.id] == 0 and n.id != "josh"]
        hubs = [(n.name, connection_counts[n.id]) for n in nodes if connection_counts[n.id] > 5]

        # Edge type diversity
        edge_type_counts = Counter(e.type for e in edges)

        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "density": round(len(edges) / max(len(nodes), 1), 2),
            "type_distribution": dict(type_counts),
            "avg_weight": round(avg_weight, 2),
            "low_weight_nodes": low_weight,
            "high_weight_nodes": high_weight,
            "orphans": orphans,
            "hubs": sorted(hubs, key=lambda x: -x[1])[:5],
            "edge_type_distribution": dict(edge_type_counts),
        }

    def _find_coverage_gaps(self) -> list[dict]:
        """Find areas of Josh's life not well-represented in the graph."""
        gaps = []

        # Check for underrepresented types
        type_counts = Counter(n.type for n in self.graph.nodes.values())

        expected_minimums = {
            "person": 5,
            "project": 5,
            "goal": 5,
            "value": 5,
            "pattern": 5,
            "fear": 2,
            "skill": 3,
            "tool": 3,
        }

        for ntype, minimum in expected_minimums.items():
            actual = type_counts.get(ntype, 0)
            if actual < minimum:
                gaps.append({
                    "type": "underrepresented_type",
                    "node_type": ntype,
                    "current": actual,
                    "expected_minimum": minimum,
                    "suggestion": f"Add more {ntype} nodes. Currently {actual}, recommend {minimum}+.",
                })

        # Check for missing edge types
        edge_types_present = set(e.type for e in self.graph.edges)
        important_edges = {"feeds_into", "blocks", "contradicts", "compounds", "pattern_matches"}
        missing_edges = important_edges - edge_types_present

        for etype in missing_edges:
            gaps.append({
                "type": "missing_edge_type",
                "edge_type": etype,
                "suggestion": f"No '{etype}' edges in graph. These reveal important dynamics.",
            })

        # Check for goals without strategies
        goals = [n for n in self.graph.nodes.values() if n.type == "goal"]
        for goal in goals:
            connections = self.graph.get_connections(goal.id)
            strategies = [c for c in connections if c["node"].type == "concept"
                         and "strat" in c["node"].id]
            if not strategies:
                gaps.append({
                    "type": "unstrategized_goal",
                    "goal": goal.name,
                    "suggestion": f"Goal '{goal.name}' has no strategy node connected. How will it be achieved?",
                })

        return gaps

    def _analyze_scoring(self) -> dict:
        """Analyze approval prediction accuracy."""
        approval_path = self.data_dir / "autonomous_approvals.jsonl"

        if not approval_path.exists():
            return {"status": "no_data", "message": "No approvals yet. Need feedback to calibrate."}

        approvals = []
        rejections = []

        with open(approval_path) as f:
            for line in f:
                entry = json.loads(line)
                predicted = entry.get("proposal", {}).get("approval_probability", 0.5)
                actual = entry.get("approved", False)
                if actual:
                    approvals.append(predicted)
                else:
                    rejections.append(predicted)

        if not approvals and not rejections:
            return {"status": "no_data"}

        # Calculate calibration
        # High predictions that were approved = good
        # High predictions that were rejected = bad (overconfident)
        # Low predictions that were approved = bad (underconfident)

        overconfident = [p for p in rejections if p > 0.7]
        underconfident = [p for p in approvals if p < 0.5]

        return {
            "total_feedback": len(approvals) + len(rejections),
            "approval_rate": f"{len(approvals)/(len(approvals)+len(rejections))*100:.0f}%",
            "overconfident_predictions": len(overconfident),
            "underconfident_predictions": len(underconfident),
            "calibration": "good" if not overconfident and not underconfident else "needs_adjustment",
        }

    def _analyze_mechanisms(self) -> dict:
        """Analyze which mechanisms are working and which need improvement."""
        mechanisms = {
            "1_compression": {"status": "active", "data_source": "compression_log.jsonl"},
            "2_momentum": {"status": "active", "data_source": "bandwidth_sessions.jsonl"},
            "3_parallel": {"status": "active", "data_source": "in-memory"},
            "4_error_absorption": {"status": "passive", "note": "No dedicated tracking yet"},
            "5_memory": {"status": "active", "data_source": "identity_graph.json"},
            "6_spiral": {"status": "active", "data_source": "bandwidth_sessions.jsonl"},
            "7_thermal": {"status": "active", "data_source": "in-memory"},
            "8_compounding": {"status": "active", "data_source": "learning_log.jsonl"},
            "9_metacognition": {"status": "active", "data_source": "theory_discoveries.jsonl"},
            "10_thermal_as_parallel": {"status": "theoretical", "note": "Documented but not tracked"},
            "11_theory_building": {"status": "meta", "note": "Self-referential — always active"},
        }

        # Check which data sources exist
        for mech_id, mech in mechanisms.items():
            ds = mech.get("data_source", "")
            if ds and ds != "in-memory":
                exists = (self.data_dir / ds).exists()
                mech["has_data"] = exists

        return mechanisms

    def _generate_proposals(self, analysis: dict) -> list[dict]:
        """Generate self-modification proposals based on analysis."""
        proposals = []

        # From graph health
        graph = analysis["graph_health"]
        if graph["orphans"]:
            proposals.append({
                "type": "graph_structure",
                "action": f"Connect orphan nodes: {', '.join(graph['orphans'][:3])}",
                "reasoning": "Orphan nodes represent knowledge not integrated into the system",
                "priority": "medium",
            })

        if graph["density"] < 1.5:
            proposals.append({
                "type": "graph_structure",
                "action": f"Increase graph density (currently {graph['density']}). Add more cross-domain edges.",
                "reasoning": "Low density = shallow understanding. Josh's brain is highly interconnected.",
                "priority": "high",
            })

        # From coverage gaps
        for gap in analysis["coverage_gaps"]:
            proposals.append({
                "type": "coverage",
                "action": gap["suggestion"],
                "reasoning": f"Gap type: {gap['type']}",
                "priority": "medium",
            })

        # From scoring
        scoring = analysis["scoring_accuracy"]
        if scoring.get("calibration") == "needs_adjustment":
            proposals.append({
                "type": "scoring",
                "action": "Recalibrate approval predictor — currently miscalibrated",
                "reasoning": f"Overconfident: {scoring.get('overconfident_predictions', 0)}, "
                            f"Underconfident: {scoring.get('underconfident_predictions', 0)}",
                "priority": "high",
            })

        # Meta-proposal: the system should track its own improvement
        proposals.append({
            "type": "meta",
            "action": "Add self-modification tracking — log every change made to the twin and measure impact",
            "reasoning": "Can't improve what you can't measure. The twin should track its own evolution.",
            "priority": "high",
        })

        return proposals

    def evolution_status(self) -> dict:
        """How is the twin evolving?"""
        # Count all data files
        data_files = list(self.data_dir.glob("*.jsonl"))
        total_entries = 0
        for f in data_files:
            with open(f) as fh:
                total_entries += sum(1 for _ in fh)

        return {
            "graph_nodes": len(self.graph.nodes),
            "graph_edges": len(self.graph.edges),
            "data_files": len(data_files),
            "total_data_entries": total_entries,
            "pattern_clusters": len(self.graph.find_pattern_clusters()),
            "evolution_stage": self._determine_stage(),
        }

    def _determine_stage(self) -> dict:
        nodes = len(self.graph.nodes)
        edges = len(self.graph.edges)
        clusters = len(self.graph.find_pattern_clusters())

        if nodes < 50:
            stage = "embryonic"
            desc = "Graph is small. Need more entities and connections."
        elif nodes < 100 and edges < 150:
            stage = "adolescent"
            desc = "Growing. Patterns emerging. Need more cross-domain edges."
        elif nodes < 200 and clusters >= 3:
            stage = "adult"
            desc = "Mature graph with pattern clusters. Ready for deep reasoning."
        else:
            stage = "superintelligent"
            desc = "Dense, highly connected, self-improving. The twin IS the intelligence."

        return {
            "stage": stage,
            "description": desc,
            "nodes": nodes,
            "edges": edges,
            "clusters": clusters,
        }


def demo():
    graph = IdentityGraph()
    engine = SelfModifier(graph)

    print("=" * 60)
    print("SELF-MODIFICATION ENGINE — Level 10: Recursive Self-Improvement")
    print("=" * 60)

    analysis = engine.analyze_performance()

    print(f"\n--- GRAPH HEALTH ---")
    gh = analysis["graph_health"]
    print(f"  Nodes: {gh['total_nodes']}, Edges: {gh['total_edges']}, Density: {gh['density']}")
    print(f"  Avg weight: {gh['avg_weight']}")
    print(f"  Orphans: {', '.join(gh['orphans'][:5]) or 'none'}")
    print(f"  Hubs: {', '.join(f'{n}({c})' for n,c in gh['hubs'][:3])}")

    print(f"\n--- COVERAGE GAPS ---")
    for gap in analysis["coverage_gaps"][:5]:
        print(f"  [{gap['type']}] {gap['suggestion']}")

    print(f"\n--- SCORING ACCURACY ---")
    sa = analysis["scoring_accuracy"]
    print(f"  {sa.get('message', sa.get('status', 'unknown'))}")

    print(f"\n--- PROPOSED SELF-MODIFICATIONS ---")
    for p in analysis["proposed_modifications"]:
        print(f"  [{p['priority'].upper()}] {p['action']}")
        print(f"    Why: {p['reasoning'][:70]}")
        print()

    print(f"--- EVOLUTION STATUS ---")
    evo = engine.evolution_status()
    stage = evo["evolution_stage"]
    print(f"  Stage: {stage['stage'].upper()}")
    print(f"  {stage['description']}")
    print(f"  Graph: {stage['nodes']} nodes, {stage['edges']} edges, {stage['clusters']} clusters")

    print(f"\n{'=' * 60}")
    print("The twin analyzes itself. Proposes improvements.")
    print("Josh approves. The twin applies. The spiral continues.")
    print("This is Level 10. The system that improves the system.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
