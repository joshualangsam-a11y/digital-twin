"""
AUTONOMOUS ENGINE — The Twin Acts Without Being Asked

Level 9 of the spiral: AGENCY

The twin doesn't wait for commands. It:
- Monitors the environment continuously
- Detects situations that match Josh's decision patterns
- Proposes AND DRAFTS actions (never sends — drafts only)
- Learns from approval/rejection to propose better next time

This is the difference between a tool and a teammate.
A tool waits. A teammate shows up with the work half done.

The key insight from the paper: compressed intent works because
the AI understands the CONTEXT well enough to decompress.
The autonomous engine flips this: the twin generates compressed
intent on Josh's behalf based on the context it already has.

Josh's gut decides in seconds. The twin pre-computes what
Josh's gut would say, so when he checks in, the decision
is already made — he just confirms or rejects.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge
from engines.reasoning import ReasoningEngine
from engines.action import ActionEngine
from engines.bandwidth_expander import BandwidthExpander


class AutonomousEngine:
    """
    Proactive intelligence that mirrors Josh's decision-making.

    Doesn't replace Josh — pre-computes his likely decisions
    so he can approve in seconds instead of thinking from scratch.

    This IS compressed intent, reversed:
    - Normal: Josh gives compressed intent → AI decompresses into action
    - Autonomous: AI compresses the situation → presents to Josh's gut → done
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.reasoning = ReasoningEngine(self.graph)
        self.action = ActionEngine(self.graph)
        self.bandwidth = BandwidthExpander(self.graph)
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.proposals_path = self.data_dir / "autonomous_proposals.jsonl"
        self.approval_path = self.data_dir / "autonomous_approvals.jsonl"

    # ═══════════════════════════════════════════
    # THE DAILY AUTONOMOUS CYCLE
    # ═══════════════════════════════════════════

    def run_cycle(self) -> dict:
        """
        Complete autonomous cycle:
        1. Scan environment
        2. Match to Josh's patterns
        3. Draft proposals
        4. Rank by Josh's likely approval
        5. Present for gut-check (approve/reject)
        """
        cycle = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "proposals": [],
        }

        # Run all proposal generators
        cycle["proposals"].extend(self._propose_pipeline_actions())
        cycle["proposals"].extend(self._propose_build_priorities())
        cycle["proposals"].extend(self._propose_pattern_exploits())
        cycle["proposals"].extend(self._propose_relationship_moves())
        cycle["proposals"].extend(self._propose_learning_actions())

        # Rank by predicted approval probability
        for p in cycle["proposals"]:
            p["approval_probability"] = self._predict_approval(p)

        cycle["proposals"].sort(key=lambda x: x["approval_probability"], reverse=True)

        # Log
        self._log(self.proposals_path, cycle)

        return cycle

    # ═══════════════════════════════════════════
    # PROPOSAL GENERATORS
    # ═══════════════════════════════════════════

    def _propose_pipeline_actions(self) -> list[dict]:
        """Scan pipeline, draft follow-ups Josh would send."""
        proposals = []

        # Check for contacts in graph
        contacts = [n for n in self.graph.nodes.values() if n.type == "contact"]

        for contact in contacts:
            if "stale" in contact.description.lower():
                proposals.append({
                    "type": "pipeline",
                    "action": f"Draft follow-up to {contact.name}",
                    "reasoning": f"{contact.name} going cold — loss: competitor closes them",
                    "draft": f"Hey {contact.name.split()[0]}, wanted to circle back on Litigation Juris. "
                             f"I know you're busy — just 5 minutes to show you what's changed. When works?",
                    "urgency": 8,
                    "josh_pattern": "Josh follows up warm and brief, never pushy",
                })

            if "demo" in contact.description.lower():
                proposals.append({
                    "type": "pipeline",
                    "action": f"Send pilot proposal to {contact.name}",
                    "reasoning": f"Post-demo is highest conversion window",
                    "draft": f"Hi {contact.name.split()[0]}, following up from our demo. "
                             f"I'd love to get you started with a 90-day free pilot — "
                             f"white-glove setup, I handle everything. Sound good?",
                    "urgency": 9,
                    "josh_pattern": "Josh offers value first, asks for commitment second",
                })

        return proposals

    def _propose_build_priorities(self) -> list[dict]:
        """Based on graph state, propose what to build next."""
        proposals = []

        priorities = self.reasoning.daily_priorities("peak")

        for p in priorities[:3]:
            # Find what's blocking this project
            project_node = None
            for n in self.graph.nodes.values():
                if n.name == p["project"]:
                    project_node = n
                    break

            if project_node:
                blockers = self.graph.get_connections(project_node.id, "depends_on")
                blocker_names = [c["node"].name for c in blockers]

                proposals.append({
                    "type": "build",
                    "action": f"Advance {p['project']} — weight {p['weight']}",
                    "reasoning": f"Priority #{priorities.index(p)+1}. "
                                 f"Feeds: {', '.join(p['feeds_goals']) or 'needs goal link'}. "
                                 f"Blockers: {', '.join(blocker_names) or 'none'}",
                    "urgency": min(10, int(p["weight"])),
                    "josh_pattern": "Josh builds the highest-weight thing during peak hours",
                })

        return proposals

    def _propose_pattern_exploits(self) -> list[dict]:
        """Find cross-domain patterns that can be exploited."""
        proposals = []

        clusters = self.graph.find_pattern_clusters()
        for cluster in clusters:
            names = [self.graph.nodes[nid].name for nid in cluster if nid in self.graph.nodes]
            if len(names) >= 2:
                proposals.append({
                    "type": "pattern",
                    "action": f"Extract shared system from {' + '.join(names)}",
                    "reasoning": f"Pattern cluster: {' ↔ '.join(names)}. "
                                 "Shared infrastructure = compound leverage.",
                    "urgency": 5,
                    "josh_pattern": "Josh sees cross-domain patterns — this is his superpower",
                })

        return proposals

    def _propose_relationship_moves(self) -> list[dict]:
        """Propose strategic relationship actions."""
        proposals = []

        # Check for high-weight people with no recent edge
        people = [n for n in self.graph.nodes.values() if n.type == "person" and n.id != "josh"]

        for person in people:
            connections = self.graph.get_connections(person.id)
            trust_edges = [c for c in connections if c["edge"].type == "trusts"]

            if person.weight >= 3.0 and not trust_edges:
                proposals.append({
                    "type": "relationship",
                    "action": f"Deepen relationship with {person.name}",
                    "reasoning": f"High-weight connection ({person.weight}) but no trust edge. "
                                 f"Context: {person.description[:80]}",
                    "urgency": 3,
                    "josh_pattern": "Josh values genuine relationships over transactional ones",
                })

        return proposals

    def _propose_learning_actions(self) -> list[dict]:
        """Propose what the twin should learn next."""
        proposals = []

        # Find graph gaps
        goals_without_projects = []
        for n in self.graph.nodes.values():
            if n.type == "goal":
                feeds = [c for c in self.graph.get_connections(n.id)
                        if c["edge"].type == "feeds_into" and c["direction"] == "incoming"]
                if not feeds:
                    goals_without_projects.append(n.name)

        if goals_without_projects:
            proposals.append({
                "type": "learning",
                "action": f"Create plans for unlinked goals: {', '.join(goals_without_projects[:3])}",
                "reasoning": "Goals without feeding projects are wishes, not plans",
                "urgency": 4,
                "josh_pattern": "Josh converts vision to systems — goals need projects",
            })

        # Check for low-weight nodes that might need reinforcement
        fading = [n for n in self.graph.nodes.values()
                  if n.weight < 1.0 and n.type in ("project", "goal")]
        if fading:
            proposals.append({
                "type": "learning",
                "action": f"Review fading priorities: {', '.join(n.name for n in fading[:3])}",
                "reasoning": "These are decaying in the graph — decide: reinforce or let go",
                "urgency": 3,
                "josh_pattern": "Josh prunes decisively — no half-commitments",
            })

        return proposals

    # ═══════════════════════════════════════════
    # APPROVAL PREDICTION
    # ═══════════════════════════════════════════

    def _predict_approval(self, proposal: dict) -> float:
        """
        Predict whether Josh would approve this proposal.
        Based on his decision patterns from the brain map.
        """
        score = 0.5  # Base

        # Josh approves revenue-generating actions faster
        if any(w in proposal.get("action", "").lower()
               for w in ["revenue", "client", "send", "follow", "demo", "pipeline"]):
            score += 0.15

        # Josh approves building during peak hours
        hour = datetime.now().hour
        if proposal["type"] == "build" and 11 <= hour <= 23:
            score += 0.1

        # Higher urgency = higher approval
        urgency = proposal.get("urgency", 5)
        score += urgency * 0.03

        # Josh pattern matching
        if "cross-domain" in proposal.get("reasoning", "").lower():
            score += 0.1  # Josh loves pattern exploitation

        # Loss framing increases approval
        if "loss" in proposal.get("reasoning", "").lower() or "competitor" in proposal.get("reasoning", "").lower():
            score += 0.1

        return round(min(1.0, score), 2)

    # ═══════════════════════════════════════════
    # APPROVAL/REJECTION PROCESSING
    # ═══════════════════════════════════════════

    def approve(self, proposal_index: int, proposals: list) -> dict:
        """Josh approved. Execute and reinforce."""
        if proposal_index >= len(proposals):
            return {"error": "Invalid index"}

        proposal = proposals[proposal_index]
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "proposal": proposal,
            "approved": True,
        }
        self._log(self.approval_path, entry)

        # Reinforce related graph nodes
        action_lower = proposal["action"].lower()
        for node in self.graph.nodes.values():
            if any(word in action_lower for word in node.name.lower().split() if len(word) > 3):
                self.graph.reinforce(node.id, 0.2)

        self.graph.save()
        return {"status": "approved", "action": proposal["action"]}

    def reject(self, proposal_index: int, proposals: list, reason: str = "") -> dict:
        """Josh rejected. Weaken and learn."""
        if proposal_index >= len(proposals):
            return {"error": "Invalid index"}

        proposal = proposals[proposal_index]
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "proposal": proposal,
            "approved": False,
            "reason": reason,
        }
        self._log(self.approval_path, entry)

        # Weaken related patterns
        action_lower = proposal["action"].lower()
        for node in self.graph.nodes.values():
            if any(word in action_lower for word in node.name.lower().split() if len(word) > 3):
                node.weight = max(0.1, node.weight - 0.1)

        self.graph.save()
        return {"status": "rejected", "action": proposal["action"], "reason": reason}

    def _log(self, path: Path, entry: dict):
        with open(path, "a") as f:
            f.write(json.dumps(entry) + "\n")


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = AutonomousEngine(graph)

    print("=" * 60)
    print("AUTONOMOUS ENGINE — Level 9: Agency")
    print("The twin proposes. Josh's gut approves.")
    print("=" * 60)

    cycle = engine.run_cycle()
    proposals = cycle["proposals"]

    print(f"\n{len(proposals)} proposals generated:\n")
    for i, p in enumerate(proposals):
        bar = "█" * int(p["approval_probability"] * 10) + "░" * (10 - int(p["approval_probability"] * 10))
        print(f"  [{bar}] #{i+1} ({p['type']}) — {p['action']}")
        print(f"    Why: {p['reasoning'][:80]}")
        if p.get("draft"):
            print(f"    Draft: \"{p['draft'][:80]}...\"")
        print(f"    Approval prediction: {p['approval_probability']*100:.0f}%")
        print(f"    Josh pattern: {p.get('josh_pattern', 'N/A')}")
        print()

    print(f"{'=' * 60}")
    print("The twin doesn't wait. It shows up with the work half done.")
    print("Josh's gut approves or rejects. Each response makes it smarter.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
