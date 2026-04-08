"""
ACTION ENGINE — The Twin Does Things

Not reactive. PROACTIVE. This engine:
- Scans the graph for opportunities
- Detects stale pipelines and drafts follow-ups
- Notices missing connections and suggests them
- Generates overnight build plans
- Surfaces "you should do X" before Josh asks

The difference between a tool and a twin:
A tool waits. A twin acts.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph
from engines.reasoning import ReasoningEngine


class ActionEngine:
    """
    Proactive intelligence layer.
    Scans state, identifies opportunities, proposes actions.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.reasoning = ReasoningEngine(self.graph)
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.actions_log = self.data_dir / "proposed_actions.jsonl"

    # ═══════════════════════════════════════════
    # PROACTIVE SCANS
    # ═══════════════════════════════════════════

    def scan_all(self) -> list[dict]:
        """Run all proactive scans and return prioritized actions."""
        actions = []

        actions.extend(self.scan_stale_connections())
        actions.extend(self.scan_unlinked_goals())
        actions.extend(self.scan_momentum_risks())
        actions.extend(self.scan_compound_opportunities())
        actions.extend(self.scan_missing_patterns())

        # Prioritize by urgency
        actions.sort(key=lambda x: x.get("urgency", 0), reverse=True)

        # Log proposed actions
        for action in actions:
            action["proposed_at"] = datetime.now(timezone.utc).isoformat()
            self._log(action)

        return actions

    def scan_stale_connections(self) -> list[dict]:
        """Find contacts/leads going cold."""
        actions = []
        contacts = [n for n in self.graph.nodes.values() if n.type == "contact"]

        for contact in contacts:
            # Check if "stale" or "going stale" in description
            if "stale" in contact.description.lower():
                actions.append({
                    "type": "stale_contact",
                    "urgency": 7,
                    "target": contact.name,
                    "action": f"Follow up with {contact.name} — going cold",
                    "reasoning": "Every day without contact, close probability drops ~5%",
                    "loss_frame": f"Lose {contact.name} as a lead if no contact this week",
                })

            # Check if "demo" in description (high-value, needs follow-through)
            if "demo" in contact.description.lower():
                actions.append({
                    "type": "demo_followup",
                    "urgency": 8,
                    "target": contact.name,
                    "action": f"Send demo follow-up to {contact.name}",
                    "reasoning": "Post-demo is highest conversion window",
                    "loss_frame": f"{contact.name} will choose a competitor if you don't follow up",
                })

        return actions

    def scan_unlinked_goals(self) -> list[dict]:
        """Find goals with no project feeding them."""
        actions = []
        goals = [n for n in self.graph.nodes.values() if n.type == "goal"]

        for goal in goals:
            incoming = self.graph.get_connections(goal.id)
            feeds = [c for c in incoming if c["edge"].type == "feeds_into"]

            if not feeds:
                actions.append({
                    "type": "unlinked_goal",
                    "urgency": 5,
                    "target": goal.name,
                    "action": f"Goal '{goal.name}' has no project feeding it — needs a plan",
                    "reasoning": "A goal without a feeding project is a wish, not a plan",
                    "loss_frame": f"'{goal.name}' will remain a dream without a system",
                })

        return actions

    def scan_momentum_risks(self) -> list[dict]:
        """Detect patterns that could break momentum."""
        actions = []

        # Check for too many parallel tracks
        active_projects = [n for n in self.graph.nodes.values()
                          if n.type == "project" and n.weight > 3]
        if len(active_projects) > 7:
            actions.append({
                "type": "overload_risk",
                "urgency": 6,
                "action": f"{len(active_projects)} active projects — risk of context switching overload",
                "reasoning": "ADHD parallel processing has limits. 3-7 tracks optimal, >7 = fragmentation",
                "loss_frame": "Spreading too thin means nothing ships",
            })

        # Check for high-weight projects with no recent activity
        # (Would need session data — placeholder for Phase 4)

        return actions

    def scan_compound_opportunities(self) -> list[dict]:
        """Find places where one action amplifies multiple projects."""
        actions = []

        # Find nodes connected to 3+ projects
        for node_id, node in self.graph.nodes.items():
            if node.type in ("tool", "skill", "concept"):
                project_connections = [
                    c for c in self.graph.get_connections(node_id)
                    if c["node"].type == "project"
                ]
                if len(project_connections) >= 3:
                    project_names = [c["node"].name for c in project_connections[:5]]
                    actions.append({
                        "type": "compound_leverage",
                        "urgency": 4,
                        "target": node.name,
                        "action": f"Investing in '{node.name}' compounds across {len(project_connections)} projects: {', '.join(project_names)}",
                        "reasoning": "Cross-project leverage = highest ROI work",
                        "loss_frame": "Building project-specific instead of shared infrastructure wastes 3x effort",
                    })

        # Find pattern_matches edges — these are cross-domain insights
        clusters = self.graph.find_pattern_clusters()
        for cluster in clusters:
            names = [self.graph.nodes[nid].name for nid in cluster if nid in self.graph.nodes]
            if len(names) >= 2:
                actions.append({
                    "type": "pattern_exploit",
                    "urgency": 3,
                    "target": " ↔ ".join(names),
                    "action": f"Pattern cluster detected: {' ↔ '.join(names)} — can you extract a shared system?",
                    "reasoning": "Cross-domain patterns are Josh's superpower. Codify them.",
                    "loss_frame": "Leaving patterns implicit means rebuilding the wheel each time",
                })

        return actions

    def scan_missing_patterns(self) -> list[dict]:
        """Find nodes that SHOULD be connected but aren't."""
        actions = []

        # Projects with same node_type but no pattern_matches edge
        projects = [n for n in self.graph.nodes.values() if n.type == "project"]
        for i, p1 in enumerate(projects):
            for p2 in projects[i+1:]:
                # Check if they share a connection to the same node
                p1_conns = {c["node"].id for c in self.graph.get_connections(p1.id)}
                p2_conns = {c["node"].id for c in self.graph.get_connections(p2.id)}
                shared = p1_conns & p2_conns - {"josh"}

                if len(shared) >= 2:
                    # These projects share multiple connections — might be a pattern
                    existing_pattern = any(
                        e for e in self.graph.edges
                        if e.type == "pattern_matches"
                        and {e.source_id, e.target_id} == {p1.id, p2.id}
                    )
                    if not existing_pattern:
                        shared_names = [self.graph.nodes[s].name for s in shared if s in self.graph.nodes]
                        actions.append({
                            "type": "missing_pattern",
                            "urgency": 2,
                            "target": f"{p1.name} ↔ {p2.name}",
                            "action": f"Potential pattern: {p1.name} and {p2.name} share connections to {', '.join(shared_names[:3])}",
                            "reasoning": "Undetected patterns = untapped leverage",
                        })

        return actions

    def generate_overnight_plan(self, energy: str = "deep_night") -> dict:
        """
        Generate a plan for what the twin should do overnight.
        Autonomous builds, research, pipeline maintenance.
        """
        priorities = self.reasoning.daily_priorities(energy)
        scan_results = self.scan_all()

        plan = {
            "generated": datetime.now(timezone.utc).isoformat(),
            "energy": energy,
            "build_tasks": [],
            "research_tasks": [],
            "pipeline_tasks": [],
            "learning_tasks": [],
        }

        # Highest urgency scans become pipeline tasks
        for action in scan_results:
            if action.get("urgency", 0) >= 6:
                if "contact" in action.get("type", "") or "followup" in action.get("type", ""):
                    plan["pipeline_tasks"].append(action["action"])
                else:
                    plan["build_tasks"].append(action["action"])

        # Top 3 priorities become build suggestions
        for p in priorities[:3]:
            plan["build_tasks"].append(f"Advance {p['project']} (weight: {p['weight']})")

        # Always learn
        plan["learning_tasks"].append("Run daily integration (decay, cluster detection, insight generation)")
        plan["learning_tasks"].append("Check for new memory files and ingest into graph")

        return plan

    def _log(self, entry: dict):
        with open(self.actions_log, "a") as f:
            f.write(json.dumps(entry) + "\n")


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = ActionEngine(graph)

    print("=" * 60)
    print("ACTION ENGINE — Proactive Intelligence")
    print("=" * 60)

    # Full scan
    print("\n--- PROACTIVE SCAN ---")
    actions = engine.scan_all()
    for action in actions:
        urgency_bar = "█" * action.get("urgency", 0) + "░" * (10 - action.get("urgency", 0))
        print(f"\n[{urgency_bar}] {action['type'].upper()}")
        print(f"  Action: {action['action']}")
        if "loss_frame" in action:
            print(f"  Loss: {action['loss_frame']}")

    # Overnight plan
    print("\n--- OVERNIGHT BUILD PLAN ---")
    plan = engine.generate_overnight_plan()
    for category, tasks in plan.items():
        if category in ("generated", "energy"):
            continue
        if tasks:
            print(f"\n  {category}:")
            for task in tasks:
                print(f"    → {task}")

    print("\nAction engine operational. The twin doesn't wait — it acts.")


if __name__ == "__main__":
    demo()
