#!/usr/bin/env python3
"""
FEEDBACK LOOP — Phase 5

The twin gets smarter from Josh's yes/no.

Every time Josh approves or rejects a twin suggestion,
this adjusts the weights in the identity graph.

Over time, the scoring model converges on Josh's actual judgment.
This is how the twin goes from "rule-based" to "Josh-like."
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Edge
from engines.learning import LearningEngine


class FeedbackLoop:
    """
    Processes Josh's feedback and adjusts the twin's intelligence.
    """

    def __init__(self):
        self.graph = IdentityGraph()
        self.learning = LearningEngine(self.graph)
        self.feedback_path = Path("~/digital-twin/data/feedback.jsonl").expanduser()

    def approve(self, action_description: str, notes: str = ""):
        """Josh approved a twin suggestion. Reinforce."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action_description,
            "approved": True,
            "notes": notes,
        }
        self._save(entry)

        # Reinforce related nodes
        for node in self.graph.nodes.values():
            if any(word in action_description.lower() for word in node.name.lower().split() if len(word) > 3):
                self.graph.reinforce(node.id, 0.15)
                print(f"  Reinforced: {node.name} (+0.15 → {node.weight:.2f})")

        self.graph.save()
        print(f"✓ Approved: {action_description}")

    def reject(self, action_description: str, reason: str = ""):
        """Josh rejected a twin suggestion. Weaken."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action_description,
            "approved": False,
            "reason": reason,
        }
        self._save(entry)

        # Weaken related nodes
        for node in self.graph.nodes.values():
            if any(word in action_description.lower() for word in node.name.lower().split() if len(word) > 3):
                node.weight = max(0.1, node.weight - 0.1)
                print(f"  Weakened: {node.name} (-0.1 → {node.weight:.2f})")

        self.graph.save()
        print(f"✗ Rejected: {action_description} — {reason}")

    def connect(self, source: str, target: str, relationship: str, evidence: str = ""):
        """Josh sees a connection the twin missed. Add it."""
        # Find node IDs by name
        src_id = self._find_node(source)
        tgt_id = self._find_node(target)

        if not src_id:
            print(f"Node not found: {source}")
            return
        if not tgt_id:
            print(f"Node not found: {target}")
            return

        edge = Edge(src_id, tgt_id, relationship, weight=3.0, evidence=evidence)
        self.graph.add_edge(edge)
        self.graph.save()

        src_name = self.graph.nodes[src_id].name
        tgt_name = self.graph.nodes[tgt_id].name
        print(f"↔ Connected: {src_name} --[{relationship}]--> {tgt_name}")

    def status(self):
        """Show feedback stats."""
        if not self.feedback_path.exists():
            print("No feedback yet.")
            return

        approvals = 0
        rejections = 0
        with open(self.feedback_path) as f:
            for line in f:
                entry = json.loads(line)
                if entry.get("approved"):
                    approvals += 1
                else:
                    rejections += 1

        total = approvals + rejections
        accuracy = approvals / max(total, 1) * 100

        print(f"Feedback Loop Status:")
        print(f"  Total feedback: {total}")
        print(f"  Approved: {approvals} ({accuracy:.0f}%)")
        print(f"  Rejected: {rejections}")
        print(f"  Graph: {len(self.graph.nodes)} nodes, {len(self.graph.edges)} edges")
        print(f"  Avg weight: {sum(n.weight for n in self.graph.nodes.values()) / max(len(self.graph.nodes), 1):.2f}")

    def _find_node(self, name: str) -> str | None:
        name_lower = name.lower()
        for node_id, node in self.graph.nodes.items():
            if node.name.lower() == name_lower or node_id == name_lower:
                return node_id
        # Fuzzy
        for node_id, node in self.graph.nodes.items():
            if name_lower in node.name.lower():
                return node_id
        return None

    def _save(self, entry: dict):
        with open(self.feedback_path, "a") as f:
            f.write(json.dumps(entry) + "\n")


# CLI interface
if __name__ == "__main__":
    fb = FeedbackLoop()

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python feedback.py approve 'description' ['notes']")
        print("  python feedback.py reject 'description' ['reason']")
        print("  python feedback.py connect 'source' 'target' 'relationship' ['evidence']")
        print("  python feedback.py status")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "approve" and len(sys.argv) >= 3:
        fb.approve(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
    elif cmd == "reject" and len(sys.argv) >= 3:
        fb.reject(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
    elif cmd == "connect" and len(sys.argv) >= 5:
        fb.connect(sys.argv[2], sys.argv[3], sys.argv[4],
                  sys.argv[5] if len(sys.argv) > 5 else "")
    elif cmd == "status":
        fb.status()
    else:
        print(f"Unknown command: {cmd}")
