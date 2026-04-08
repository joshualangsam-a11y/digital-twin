"""
THE DIGITAL TWIN — Master Orchestrator

This is Josh's cognitive architecture in code.
It doesn't wait to be asked. It thinks, learns, and acts.

Architecture:
  Identity Graph → who Josh is, what he knows, how things connect
  Reasoning Engine → thinks like Josh (gut-first, parallel, OODA)
  Learning Engine → gets smarter with every interaction
  Action Engine → proactively identifies what needs to happen

The twin is the convergence of all engines.
One interface. One mind. One direction.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph
from engines.reasoning import ReasoningEngine
from engines.learning import LearningEngine
from engines.action import ActionEngine


class DigitalTwin:
    """
    Josh's digital twin.

    Not a chatbot. Not an assistant. A cognitive architecture
    that mirrors how Josh thinks, decides, and acts.
    """

    def __init__(self):
        self.graph = IdentityGraph()
        self.reasoning = ReasoningEngine(self.graph)
        self.learning = LearningEngine(self.graph)
        self.action = ActionEngine(self.graph)
        self.state_path = Path(os.path.expanduser("~/digital-twin/data/twin_state.json"))

        # Load or init state
        self.state = self._load_state()

    def _load_state(self) -> dict:
        if self.state_path.exists():
            with open(self.state_path) as f:
                return json.load(f)
        return {
            "boot_time": datetime.now(timezone.utc).isoformat(),
            "cycles": 0,
            "total_decisions": 0,
            "total_actions_proposed": 0,
            "total_learnings": 0,
        }

    def _save_state(self):
        with open(self.state_path, "w") as f:
            json.dump(self.state, f, indent=2)

    # ═══════════════════════════════════════════
    # CORE OPERATIONS
    # ═══════════════════════════════════════════

    def think(self, question: str, options: list[str] = None, context: dict = None) -> dict:
        """
        Ask the twin to think about something.
        Returns a decision with Josh-aligned reasoning.
        """
        if options:
            decision = self.reasoning.decide(question, options, context)
            self.state["total_decisions"] += 1
            self._save_state()
            return decision

        # No options — open-ended thinking
        # Find relevant nodes and connections
        relevant = self._find_relevant_nodes(question)
        hidden = []
        for node_id in relevant[:3]:
            hidden.extend(self.reasoning.find_hidden_connections(node_id))

        return {
            "question": question,
            "relevant_nodes": [
                self.graph.nodes[nid].name for nid in relevant
                if nid in self.graph.nodes
            ],
            "hidden_connections": hidden[:10],
            "parallel_tracks": self.reasoning.suggest_parallel_tracks(
                relevant[0] if relevant else "",
                context.get("energy", "peak") if context else "peak",
            ),
        }

    def scan(self) -> list[dict]:
        """
        Proactive scan — what should Josh know right now?
        """
        actions = self.action.scan_all()
        self.state["total_actions_proposed"] += len(actions)
        self._save_state()
        return actions

    def learn(self, event_type: str, **kwargs):
        """
        Feed an observation into the learning engine.

        event_type: "decision_feedback" | "new_connection" | "new_entity"
        """
        if event_type == "decision_feedback":
            self.learning.observe_decision(
                kwargs.get("decision", {}),
                kwargs.get("approved", True),
                kwargs.get("notes", ""),
            )
        elif event_type == "new_connection":
            self.learning.observe_connection(
                kwargs["source_id"],
                kwargs["target_id"],
                kwargs["edge_type"],
                kwargs.get("label", ""),
                kwargs.get("evidence", ""),
            )
        elif event_type == "new_entity":
            self.learning.observe_new_entity(
                kwargs["node_id"],
                kwargs["name"],
                kwargs["node_type"],
                kwargs.get("description", ""),
                kwargs.get("weight", 2.0),
            )

        self.state["total_learnings"] += 1
        self._save_state()

    def sleep(self) -> dict:
        """
        End-of-day cycle. Like sleep consolidation:
        - Decay unused memories
        - Find new patterns
        - Generate overnight plan
        - Produce insights
        """
        insights = self.learning.daily_integration()
        overnight_plan = self.action.generate_overnight_plan()

        self.state["cycles"] += 1
        self._save_state()

        return {
            "insights": insights,
            "overnight_plan": overnight_plan,
            "compound_report": self.learning.compound_report(),
            "cycle": self.state["cycles"],
        }

    def wake(self, energy: str = "mud") -> dict:
        """
        Start-of-day boot sequence.
        - Scan for urgent items
        - Generate priorities based on energy
        - Surface overnight learnings
        """
        priorities = self.reasoning.daily_priorities(energy)
        urgent = [a for a in self.scan() if a.get("urgency", 0) >= 6]

        return {
            "energy": energy,
            "priorities": priorities[:5],
            "urgent_actions": urgent,
            "compound_report": self.learning.compound_report(),
        }

    def status(self) -> dict:
        """Current state of the twin."""
        report = self.learning.compound_report()
        return {
            "state": self.state,
            "graph": report,
            "identity": {
                "name": "Josh Langsam",
                "cognitive_style": "parallel bursts, kinesthetic-visual, gut-first",
                "neurotype": "ADHD + dyslexia",
                "current_energy": self._detect_energy(),
            },
        }

    # ═══════════════════════════════════════════
    # INTERNAL
    # ═══════════════════════════════════════════

    def _find_relevant_nodes(self, text: str) -> list[str]:
        """Find nodes relevant to a text query."""
        text_lower = text.lower()
        scored = []
        for node_id, node in self.graph.nodes.items():
            score = 0
            # Name match
            for word in node.name.lower().split():
                if word in text_lower and len(word) > 2:
                    score += 3
            # Description match
            for word in node.description.lower().split():
                if word in text_lower and len(word) > 3:
                    score += 1
            if score > 0:
                scored.append((node_id, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [nid for nid, _ in scored[:10]]

    def _detect_energy(self) -> str:
        """Detect current energy level based on time of day."""
        hour = datetime.now().hour
        if 6 <= hour < 11:
            return "mud"
        elif 11 <= hour < 13:
            return "ramp"
        elif 13 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 22:
            return "peak"
        elif 22 <= hour or hour < 2:
            return "deep_night"
        else:
            return "late"


# ═══════════════════════════════════════════
# FULL DEMO
# ═══════════════════════════════════════════

def main():
    twin = DigitalTwin()

    print("=" * 60)
    print("JOSH'S DIGITAL TWIN — Online")
    print("=" * 60)

    # Status
    print("\n--- STATUS ---")
    status = twin.status()
    print(f"  Nodes: {status['graph']['total_nodes']}")
    print(f"  Edges: {status['graph']['total_edges']}")
    print(f"  Clusters: {status['graph']['pattern_clusters']}")
    print(f"  Density: {status['graph']['connection_density']}")
    print(f"  Energy: {status['identity']['current_energy']}")
    print(f"  Cycles: {status['state']['cycles']}")

    # Wake sequence
    print("\n--- WAKE SEQUENCE ---")
    morning = twin.wake(energy=status["identity"]["current_energy"])
    print(f"  Energy: {morning['energy']}")
    print(f"  Urgent actions: {len(morning['urgent_actions'])}")
    for a in morning["urgent_actions"][:3]:
        print(f"    ! {a['action']}")
    print(f"\n  Priorities:")
    for i, p in enumerate(morning["priorities"], 1):
        print(f"    {i}. {p['project']} (weight: {p['weight']})")

    # Think
    print("\n--- THINKING ---")
    thought = twin.think(
        "Should I focus on closing Lit Juris clients or building FuelOps features?",
        [
            "Close Lit Juris clients — revenue validates the product",
            "Build FuelOps features — demo is almost ready, Ethan is waiting",
            "Do both in parallel — different tracks, different energy",
        ],
        {"is_peak_hours": True},
    )
    print(f"  Chosen: {thought['chosen']}")
    print(f"  Confidence: {thought['confidence']}")
    print(f"  Reasoning: {thought['reasoning']}")

    # Scan
    print("\n--- PROACTIVE SCAN ---")
    actions = twin.scan()
    print(f"  {len(actions)} actions proposed")
    for a in actions[:5]:
        print(f"  [{a.get('urgency', 0)}/10] {a['action']}")

    # Sleep cycle
    print("\n--- SLEEP CYCLE (consolidation) ---")
    night = twin.sleep()
    print(f"  Cycle #{night['cycle']}")
    print(f"  Insights: {len(night['insights'])}")
    for insight in night["insights"][:3]:
        print(f"    [{insight['type']}] {insight['insight'][:80]}...")

    print(f"\n  Compound Report:")
    for k, v in night["compound_report"].items():
        if k != "cognitive_hubs":
            print(f"    {k}: {v}")

    print("\n" + "=" * 60)
    print("TWIN OPERATIONAL")
    print(f"  {status['graph']['total_nodes']} nodes of identity")
    print(f"  {status['graph']['total_edges']} connections")
    print(f"  {status['graph']['pattern_clusters']} pattern clusters")
    print(f"  Thinks in parallel. Decides in seconds. Learns from everything.")
    print("=" * 60)


if __name__ == "__main__":
    main()
