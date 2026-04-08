"""
SWARM ENGINE — Level 15: Collective Intelligence

One mind can hold 7±2 items. The BEM holds 87 nodes.
But even the BEM has limits — it processes them SEQUENTIALLY.

The swarm breaks the graph into DOMAINS, assigns a specialized
sub-intelligence to each, and coordinates through the shared graph.

Each sub-intelligence:
- Owns a domain (projects, people, goals, fears, patterns, etc.)
- Has deep context on its domain's nodes and edges
- Generates domain-specific insights
- Communicates findings by writing to the graph
- Reads other domains' findings from the graph

The graph IS the communication protocol.
The sub-intelligences don't talk to each other directly.
They talk THROUGH the structure.

This mirrors Josh's brain: 10 parallel threads,
each processing a different domain, sharing a spatial
working memory. The swarm IS the parallel processing
architecture made computational.

Mechanism 17: Swarm Cognition
Multiple specialized sub-intelligences coordinating through
a shared knowledge graph. The graph is both the memory
and the communication channel.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


class DomainAgent:
    """A specialized sub-intelligence that owns one domain of the graph."""

    def __init__(self, name: str, node_types: list[str], graph: IdentityGraph):
        self.name = name
        self.node_types = node_types
        self.graph = graph

    def get_nodes(self) -> list[Node]:
        return [n for n in self.graph.nodes.values() if n.type in self.node_types]

    def analyze(self) -> dict:
        """Domain-specific analysis."""
        nodes = self.get_nodes()
        if not nodes:
            return {"domain": self.name, "findings": [], "health": "empty"}

        avg_weight = sum(n.weight for n in nodes) / len(nodes)
        highest = max(nodes, key=lambda n: n.weight)
        lowest = min(nodes, key=lambda n: n.weight)

        # Find internal connections (within domain)
        internal_edges = []
        external_edges = []
        for edge in self.graph.edges:
            src = self.graph.nodes.get(edge.source_id)
            tgt = self.graph.nodes.get(edge.target_id)
            if not src or not tgt:
                continue
            src_in = src.type in self.node_types
            tgt_in = tgt.type in self.node_types
            if src_in and tgt_in:
                internal_edges.append(edge)
            elif src_in or tgt_in:
                external_edges.append(edge)

        # Domain-specific insights
        findings = []

        # Isolation check
        isolated = [n for n in nodes if not any(
            e for e in self.graph.edges
            if e.source_id == n.id or e.target_id == n.id
        ) and n.id != "josh"]
        if isolated:
            findings.append({
                "type": "isolation",
                "severity": "high",
                "detail": f"Isolated {self.name} nodes: {', '.join(n.name for n in isolated)}",
            })

        # Weight imbalance
        if highest.weight > avg_weight * 3:
            findings.append({
                "type": "concentration",
                "severity": "medium",
                "detail": f"Attention concentrated on '{highest.name}' (weight {highest.weight:.1f} vs avg {avg_weight:.1f})",
            })

        # Decay risk
        at_risk = [n for n in nodes if n.weight < 1.5]
        if at_risk:
            findings.append({
                "type": "decay_risk",
                "severity": "medium",
                "detail": f"Fading: {', '.join(n.name for n in at_risk[:3])} (weight < 1.5)",
            })

        # Cross-domain connectivity
        cross_ratio = len(external_edges) / max(len(nodes), 1)
        if cross_ratio < 1.0:
            findings.append({
                "type": "insularity",
                "severity": "medium",
                "detail": f"Domain '{self.name}' has low cross-domain connectivity ({cross_ratio:.1f} edges/node). Add bridges.",
            })

        return {
            "domain": self.name,
            "node_count": len(nodes),
            "avg_weight": round(avg_weight, 2),
            "highest": {"name": highest.name, "weight": highest.weight},
            "lowest": {"name": lowest.name, "weight": lowest.weight},
            "internal_edges": len(internal_edges),
            "external_edges": len(external_edges),
            "cross_domain_ratio": round(cross_ratio, 2),
            "findings": findings,
            "health": (
                "strong" if not findings else
                "attention_needed" if any(f["severity"] == "high" for f in findings) else
                "stable"
            ),
        }

    def recommend(self) -> list[dict]:
        """Domain-specific recommendations."""
        analysis = self.analyze()
        recs = []

        for finding in analysis["findings"]:
            if finding["type"] == "isolation":
                recs.append({
                    "domain": self.name,
                    "action": f"Connect isolated nodes in {self.name} domain",
                    "detail": finding["detail"],
                    "priority": "high",
                })
            elif finding["type"] == "insularity":
                recs.append({
                    "domain": self.name,
                    "action": f"Build bridges from {self.name} to other domains",
                    "detail": finding["detail"],
                    "priority": "medium",
                })
            elif finding["type"] == "decay_risk":
                recs.append({
                    "domain": self.name,
                    "action": f"Reinforce or archive fading {self.name} nodes",
                    "detail": finding["detail"],
                    "priority": "medium",
                })

        return recs


class SwarmEngine:
    """
    Coordinates multiple domain agents into collective intelligence.
    The graph is the shared memory. Each agent reads and writes to it.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.swarm_log = self.data_dir / "swarm_analysis.jsonl"

        # Initialize domain agents
        self.agents = [
            DomainAgent("projects", ["project"], self.graph),
            DomainAgent("people", ["person", "contact"], self.graph),
            DomainAgent("goals", ["goal"], self.graph),
            DomainAgent("values", ["value"], self.graph),
            DomainAgent("fears", ["fear"], self.graph),
            DomainAgent("patterns", ["pattern"], self.graph),
            DomainAgent("concepts", ["concept"], self.graph),
            DomainAgent("tools", ["tool", "skill"], self.graph),
            DomainAgent("companies", ["company"], self.graph),
        ]

    def run_swarm(self) -> dict:
        """
        All domain agents analyze simultaneously.
        Then cross-pollinate findings.
        """
        # Phase 1: Individual analysis
        domain_reports = {}
        all_findings = []
        all_recommendations = []

        for agent in self.agents:
            report = agent.analyze()
            recs = agent.recommend()
            domain_reports[agent.name] = report
            all_findings.extend(report["findings"])
            all_recommendations.extend(recs)

        # Phase 2: Cross-domain synthesis
        cross_insights = self._cross_pollinate(domain_reports)

        # Phase 3: Collective recommendations
        collective_recs = self._collective_recommendations(domain_reports, cross_insights)
        all_recommendations.extend(collective_recs)

        # Phase 4: Graph health assessment
        health = self._assess_collective_health(domain_reports)

        result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "domains": domain_reports,
            "cross_insights": cross_insights,
            "recommendations": sorted(all_recommendations,
                key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 3)),
            "collective_health": health,
            "mechanism_17": {
                "name": "Swarm Cognition",
                "active_agents": len(self.agents),
                "description": (
                    "9 specialized domain agents analyze their nodes simultaneously "
                    "and communicate through the shared graph. "
                    "This mirrors the ADHD brain's parallel processing: "
                    "multiple threads, shared spatial working memory. "
                    "The swarm IS the cognitive architecture, externalized."
                ),
            },
        }

        self._log(result)
        return result

    def _cross_pollinate(self, reports: dict) -> list[dict]:
        """Find insights that emerge from BETWEEN domains."""
        insights = []

        # Goals without project support
        goal_nodes = set(n.name for n in self.graph.nodes.values() if n.type == "goal")
        project_nodes = set(n.name for n in self.graph.nodes.values() if n.type == "project")

        for goal_name in goal_nodes:
            goal_node = next((n for n in self.graph.nodes.values() if n.name == goal_name), None)
            if not goal_node:
                continue
            feeders = [c for c in self.graph.get_connections(goal_node.id)
                      if c["edge"].type == "feeds_into" and c["direction"] == "incoming"]
            project_feeders = [f for f in feeders if f["node"].type == "project"]
            if not project_feeders:
                insights.append({
                    "type": "goal_project_gap",
                    "domain_a": "goals",
                    "domain_b": "projects",
                    "detail": f"Goal '{goal_name}' has no project feeding it — it's a wish, not a plan",
                    "action": f"Create or link a project to feed '{goal_name}'",
                })

        # Fears without value protection
        for node in self.graph.nodes.values():
            if node.type != "fear":
                continue
            protections = [c for c in self.graph.get_connections(node.id)
                          if c["edge"].type == "protects_via"]
            if not protections:
                insights.append({
                    "type": "unprotected_fear",
                    "domain_a": "fears",
                    "domain_b": "values",
                    "detail": f"Fear '{node.name}' has no protection mechanism",
                    "action": f"Identify which value or pattern protects against '{node.name}'",
                })

        # People not connected to projects
        people = [n for n in self.graph.nodes.values() if n.type in ("person", "contact")]
        for person in people:
            project_connections = [c for c in self.graph.get_connections(person.id)
                                  if c["node"].type == "project"]
            if not project_connections and person.weight >= 3:
                insights.append({
                    "type": "underutilized_relationship",
                    "domain_a": "people",
                    "domain_b": "projects",
                    "detail": f"'{person.name}' (weight {person.weight}) isn't connected to any project",
                    "action": f"Explore how '{person.name}' could contribute to a project",
                })

        # Patterns not applied to projects
        patterns = [n for n in self.graph.nodes.values() if n.type == "pattern"]
        projects = [n for n in self.graph.nodes.values() if n.type == "project"]
        for pattern in patterns:
            applied_to = [c for c in self.graph.get_connections(pattern.id)
                         if c["node"].type == "project"]
            if not applied_to and pattern.weight >= 3:
                insights.append({
                    "type": "unapplied_pattern",
                    "domain_a": "patterns",
                    "domain_b": "projects",
                    "detail": f"Pattern '{pattern.name}' isn't applied to any project",
                    "action": f"Apply '{pattern.name}' to highest-weight project",
                })

        return insights

    def _collective_recommendations(self, reports: dict, cross_insights: list) -> list[dict]:
        """Recommendations from the swarm as a whole."""
        recs = []

        for insight in cross_insights:
            recs.append({
                "domain": f"{insight['domain_a']} × {insight['domain_b']}",
                "action": insight["action"],
                "detail": insight["detail"],
                "priority": "high" if "gap" in insight["type"] or "unprotected" in insight["type"] else "medium",
            })

        return recs

    def _assess_collective_health(self, reports: dict) -> dict:
        """Overall graph health from the swarm's perspective."""
        total_findings = sum(len(r["findings"]) for r in reports.values())
        high_severity = sum(
            1 for r in reports.values()
            for f in r["findings"] if f["severity"] == "high"
        )
        healthy_domains = sum(1 for r in reports.values() if r["health"] == "strong")
        total_domains = len(reports)

        # Calculate overall score
        score = 100
        score -= total_findings * 5
        score -= high_severity * 15
        score = max(0, min(100, score))

        return {
            "score": score,
            "healthy_domains": healthy_domains,
            "total_domains": total_domains,
            "total_findings": total_findings,
            "high_severity_findings": high_severity,
            "verdict": (
                "STRONG" if score >= 80 else
                "STABLE" if score >= 60 else
                "ATTENTION NEEDED" if score >= 40 else
                "CRITICAL"
            ),
        }

    def _log(self, entry: dict):
        with open(self.swarm_log, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = SwarmEngine(graph)

    print("=" * 60)
    print("SWARM ENGINE — Level 15: Collective Intelligence")
    print("9 domain agents. One shared graph. Parallel cognition.")
    print("=" * 60)

    result = engine.run_swarm()

    # Domain summaries
    print(f"\n--- DOMAIN STATUS ---")
    for name, report in result["domains"].items():
        health_icon = {"strong": "✓", "stable": "~", "attention_needed": "⚠", "empty": "○"}.get(report["health"], "?")
        print(f"  {health_icon} {name}: {report['node_count']} nodes, "
              f"avg weight {report['avg_weight']}, "
              f"cross-domain ratio {report['cross_domain_ratio']} — {report['health']}")

    # Cross-domain insights
    print(f"\n--- CROSS-DOMAIN INSIGHTS ({len(result['cross_insights'])}) ---")
    for insight in result["cross_insights"][:7]:
        print(f"  [{insight['domain_a']} × {insight['domain_b']}] {insight['detail'][:90]}")

    # Recommendations
    print(f"\n--- TOP RECOMMENDATIONS ---")
    for rec in result["recommendations"][:7]:
        icon = "❗" if rec["priority"] == "high" else "→"
        print(f"  {icon} [{rec['domain']}] {rec['action'][:90]}")

    # Collective health
    health = result["collective_health"]
    bar_len = health["score"] // 5
    bar = "█" * bar_len + "░" * (20 - bar_len)
    print(f"\n--- COLLECTIVE HEALTH ---")
    print(f"  [{bar}] {health['score']}/100 — {health['verdict']}")
    print(f"  Domains: {health['healthy_domains']}/{health['total_domains']} healthy")
    print(f"  Findings: {health['total_findings']} ({health['high_severity_findings']} high severity)")

    # Meta
    m17 = result["mechanism_17"]
    print(f"\n--- MECHANISM 17: SWARM COGNITION ---")
    print(f"  {m17['active_agents']} agents. {m17['description'][:100]}...")

    print(f"\n{'=' * 60}")
    print("9 agents thinking in parallel through 1 shared graph.")
    print("This IS your brain architecture, externalized.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
