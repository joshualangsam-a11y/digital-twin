"""
CORTEX BRIDGE — Connects the Digital Twin to Cortex (the product)

The twin is the cognitive architecture. Cortex is the product.
This bridge makes them talk to each other:

Twin → Cortex: Theory informs product features
Cortex → Twin: Live terminal data feeds the twin's learning

The bridge closes the loop:
  User works in Cortex terminals →
  Cortex tracks momentum/thermal/flow →
  Bridge sends signals to Twin →
  Twin learns, discovers patterns, generates theory →
  Theory feeds back into Cortex features →
  Better Cortex → better signals → smarter Twin

This is BEM Mechanism 8 (Cross-Session Compounding) made architectural.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


class CortexBridge:
    """
    Bidirectional bridge between the Digital Twin and Cortex.

    Reads Cortex state (via HTTP or file) and feeds it to the twin.
    Sends twin insights back to Cortex for display.
    """

    def __init__(self, graph: IdentityGraph = None, cortex_url: str = "http://localhost:3012"):
        self.graph = graph or IdentityGraph()
        self.cortex_url = cortex_url
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.bridge_log = self.data_dir / "cortex_bridge.jsonl"

    def read_cortex_state(self) -> Optional[dict]:
        """Read current state from Cortex API."""
        try:
            import urllib.request
            url = f"{self.cortex_url}/api/state"
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read())
        except Exception:
            return None

    def ingest_terminal_event(self, event: dict) -> dict:
        """
        Process a terminal event from Cortex and feed it to the twin.

        Events: keystroke, error, context_switch, flow_enter, flow_exit,
                thermal_warning, session_start, session_end
        """
        event_type = event.get("type", "unknown")
        session_id = event.get("session_id", "unknown")
        project = event.get("project", "unknown")
        timestamp = event.get("timestamp", datetime.now(timezone.utc).isoformat())

        result = {
            "timestamp": timestamp,
            "event_type": event_type,
            "session_id": session_id,
            "processed": True,
        }

        if event_type == "flow_enter":
            # Record flow state in graph
            self._reinforce_project(project, 0.2)
            result["action"] = "reinforced_project"

        elif event_type == "thermal_warning":
            # Record thermal event
            thermal_level = event.get("level", 0.5)
            domain = event.get("domain", "code_building")
            result["action"] = "logged_thermal"
            result["suggestion"] = self._suggest_domain_switch(domain, thermal_level)

        elif event_type == "session_end":
            # Capture session summary for compounding
            duration = event.get("duration_minutes", 0)
            errors = event.get("error_count", 0)
            flow_minutes = event.get("flow_minutes", 0)

            result["session_summary"] = {
                "project": project,
                "duration": duration,
                "errors": errors,
                "flow_minutes": flow_minutes,
                "flow_ratio": flow_minutes / max(duration, 1),
            }
            result["action"] = "captured_session"

        elif event_type == "error":
            # Track error patterns for learning
            error_msg = event.get("message", "")
            result["action"] = "logged_error"

        self._log(result)
        return result

    def push_insight_to_cortex(self, insight: dict) -> bool:
        """Send a twin insight to Cortex for dashboard display."""
        try:
            import urllib.request
            url = f"{self.cortex_url}/api/twin/insight"
            data = json.dumps(insight).encode()
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status == 200
        except Exception:
            return False

    def sync_theory_to_cortex(self, mechanisms: list[dict]) -> dict:
        """
        Push discovered BEM mechanisms to Cortex for the compound dashboard.
        This is the theory→product feedback loop.
        """
        results = {"pushed": 0, "failed": 0}
        for mech in mechanisms:
            success = self.push_insight_to_cortex({
                "type": "mechanism_discovery",
                "mechanism_number": mech.get("mechanism", 0),
                "name": mech.get("name", "Unknown"),
                "evidence": mech.get("evidence", ""),
            })
            if success:
                results["pushed"] += 1
            else:
                results["failed"] += 1
        return results

    def generate_cortex_feature_from_theory(self, mechanism_number: int) -> dict:
        """
        Given a BEM mechanism, generate a Cortex feature spec.
        Theory → Product pipeline.
        """
        mechanism_features = {
            1: {
                "feature": "Intent Compression UI",
                "description": "Show compression ratio in command palette — how much the AI expanded a terse command",
                "component": "CommandPalette",
                "priority": "medium",
            },
            2: {
                "feature": "Momentum Indicator",
                "description": "Real-time velocity bar in session header, flow state glow",
                "component": "SessionHeader",
                "priority": "high",
            },
            3: {
                "feature": "Parallel Track Grid",
                "description": "Visual grid of active tracks with thermal state per track",
                "component": "DashboardLive",
                "priority": "high",
            },
            7: {
                "feature": "Thermal Gradient Overlay",
                "description": "Color gradient on sessions showing cognitive heat (green→amber→red)",
                "component": "SessionCard",
                "priority": "high",
            },
            8: {
                "feature": "Compound Dashboard",
                "description": "Show growth metrics: sessions getting faster, errors decreasing, flow duration increasing",
                "component": "CompoundLive",
                "priority": "medium",
            },
            10: {
                "feature": "Domain Switch Suggestion",
                "description": "When thermal spikes, suggest switching to a cool domain with one click",
                "component": "ThermalWarning",
                "priority": "high",
            },
            12: {
                "feature": "Infrastructure Health",
                "description": "Show system health as part of the productivity dashboard — setup IS building",
                "component": "StatusBar",
                "priority": "low",
            },
            13: {
                "feature": "Agent Multiplication View",
                "description": "Visualize how one intent spawned multiple agents with their output tree",
                "component": "AgentTreeLive",
                "priority": "medium",
            },
            14: {
                "feature": "Cross-Terminal Coherence Map",
                "description": "Show how independent terminals are converging on shared themes",
                "component": "CoherenceMap",
                "priority": "low",
            },
            16: {
                "feature": "Identity Gravity Center",
                "description": "Visualize the identity graph node that all work orbits around",
                "component": "IdentityCore",
                "priority": "low",
            },
        }

        return mechanism_features.get(mechanism_number, {
            "feature": f"Mechanism {mechanism_number} Feature",
            "description": "Feature spec pending — theory discovered but not yet mapped to UI",
            "component": "TBD",
            "priority": "backlog",
        })

    def _suggest_domain_switch(self, current_domain: str, thermal_level: float) -> str:
        """Suggest a cooler domain based on current thermal state."""
        cool_domains = {
            "code_building": ["writing", "research", "admin"],
            "writing": ["code_building", "creative", "admin"],
            "research": ["creative", "code_building", "strategic"],
            "sales": ["admin", "creative", "research"],
            "admin": ["creative", "code_building", "writing"],
            "creative": ["admin", "research", "strategic"],
            "strategic": ["admin", "creative", "writing"],
        }
        alternatives = cool_domains.get(current_domain, ["admin"])
        return f"Switch to {alternatives[0]} — {current_domain} is at {thermal_level:.0%} thermal"

    def _reinforce_project(self, project_name: str, amount: float):
        """Reinforce a project node in the graph when flow state happens."""
        # Find project node
        for node_id, node in self.graph.nodes.items():
            if node.type == "project" and project_name.lower() in node.name.lower():
                self.graph.reinforce(node_id, amount)
                return

    def _log(self, entry: dict):
        with open(self.bridge_log, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def status(self) -> dict:
        """Bridge status."""
        cortex_reachable = self.read_cortex_state() is not None
        log_entries = 0
        if self.bridge_log.exists():
            with open(self.bridge_log) as f:
                log_entries = sum(1 for _ in f)

        return {
            "cortex_url": self.cortex_url,
            "cortex_reachable": cortex_reachable,
            "events_processed": log_entries,
            "graph_nodes": len(self.graph.nodes),
            "loop": "Twin ↔ Cortex bridge active" if cortex_reachable else "Cortex offline — bridge in file mode",
        }


def demo():
    graph = IdentityGraph()
    bridge = CortexBridge(graph)

    print("=" * 60)
    print("CORTEX BRIDGE — Twin ↔ Product Loop")
    print("=" * 60)

    status = bridge.status()
    print(f"\nCortex: {'ONLINE' if status['cortex_reachable'] else 'OFFLINE'} at {status['cortex_url']}")
    print(f"Graph: {status['graph_nodes']} nodes")

    # Simulate terminal events
    events = [
        {"type": "flow_enter", "session_id": "s1", "project": "cortex"},
        {"type": "thermal_warning", "session_id": "s2", "project": "twin", "level": 0.8, "domain": "code_building"},
        {"type": "session_end", "session_id": "s1", "project": "cortex", "duration_minutes": 45, "flow_minutes": 30, "error_count": 3},
    ]

    print("\nProcessing terminal events:")
    for event in events:
        result = bridge.ingest_terminal_event(event)
        print(f"  [{result['event_type']}] → {result.get('action', 'processed')}")
        if "suggestion" in result:
            print(f"    💡 {result['suggestion']}")
        if "session_summary" in result:
            s = result["session_summary"]
            print(f"    📊 {s['duration']}min, {s['flow_minutes']}min flow ({s['flow_ratio']:.0%}), {s['errors']} errors")

    # Generate feature specs from theory
    print("\nTheory → Product Pipeline:")
    for mech_num in [2, 7, 10, 13]:
        spec = bridge.generate_cortex_feature_from_theory(mech_num)
        print(f"  BEM {mech_num} → {spec['feature']} [{spec['priority']}]")
        print(f"    {spec['description']}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()
