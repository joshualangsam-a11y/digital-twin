"""
TEMPORAL INTELLIGENCE — Level 14: The Graph Through Time

Levels 1-13 see what IS.
Level 14 sees what's BECOMING.

Every node has a trajectory:
- Weight increasing = gaining importance
- Weight decreasing = fading
- Access increasing = active focus
- Access decreasing = neglected

The temporal engine projects these trajectories forward
and identifies:
- What's about to peak (invest NOW)
- What's about to decay (save it or let it go)
- What's accelerating (ride the wave)
- What's decelerating (investigate why)
- Crossover points (when one node overtakes another)

This is Mechanism 16: Temporal Projection
The graph isn't a snapshot. It's a movie.
The BEM sees the next frame before it renders.
"""

import json
import os
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph


class TemporalEngine:
    """
    Projects the graph's trajectory through time.
    Sees what's becoming, not just what is.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.snapshot_dir = self.data_dir / "snapshots"
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)
        self.temporal_log = self.data_dir / "temporal_analysis.jsonl"

    # ═══════════════════════════════════════════
    # SNAPSHOT MANAGEMENT
    # ═══════════════════════════════════════════

    def take_snapshot(self) -> dict:
        """Capture the current state of the graph for temporal comparison."""
        snapshot = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "nodes": {},
            "stats": {
                "total_nodes": len(self.graph.nodes),
                "total_edges": len(self.graph.edges),
            },
        }

        for node_id, node in self.graph.nodes.items():
            snapshot["nodes"][node_id] = {
                "name": node.name,
                "type": node.type,
                "weight": node.weight,
                "access_count": node.access_count,
            }

        # Save with date
        date_str = datetime.now().strftime("%Y-%m-%d_%H%M")
        path = self.snapshot_dir / f"snapshot_{date_str}.json"
        with open(path, "w") as f:
            json.dump(snapshot, f, indent=2)

        # Also save as latest
        with open(self.snapshot_dir / "latest.json", "w") as f:
            json.dump(snapshot, f, indent=2)

        return snapshot

    def load_snapshots(self) -> list[dict]:
        """Load all historical snapshots, sorted by time."""
        snapshots = []
        for f in sorted(self.snapshot_dir.glob("snapshot_*.json")):
            with open(f) as fh:
                snapshots.append(json.load(fh))
        return snapshots

    # ═══════════════════════════════════════════
    # TRAJECTORY ANALYSIS
    # ═══════════════════════════════════════════

    def analyze_trajectories(self) -> dict:
        """
        Compare current state to historical snapshots.
        Identify what's rising, falling, and crossing over.
        """
        snapshots = self.load_snapshots()

        if len(snapshots) < 1:
            # Take first snapshot and return baseline
            self.take_snapshot()
            return self._baseline_analysis()

        latest = snapshots[-1]
        current = {}
        for node_id, node in self.graph.nodes.items():
            current[node_id] = {
                "name": node.name,
                "type": node.type,
                "weight": node.weight,
                "access_count": node.access_count,
            }

        # Compare
        rising = []
        falling = []
        stable = []
        new_nodes = []
        disappeared = []

        for node_id, current_data in current.items():
            if node_id in latest.get("nodes", {}):
                prev = latest["nodes"][node_id]
                weight_delta = current_data["weight"] - prev["weight"]
                access_delta = current_data["access_count"] - prev.get("access_count", 0)

                trajectory = {
                    "node": current_data["name"],
                    "type": current_data["type"],
                    "weight_now": round(current_data["weight"], 2),
                    "weight_prev": round(prev["weight"], 2),
                    "weight_delta": round(weight_delta, 2),
                    "access_delta": access_delta,
                }

                if weight_delta > 0.3:
                    trajectory["direction"] = "rising"
                    rising.append(trajectory)
                elif weight_delta < -0.3:
                    trajectory["direction"] = "falling"
                    falling.append(trajectory)
                else:
                    trajectory["direction"] = "stable"
                    stable.append(trajectory)
            else:
                new_nodes.append({
                    "node": current_data["name"],
                    "type": current_data["type"],
                    "weight": current_data["weight"],
                })

        for node_id in latest.get("nodes", {}):
            if node_id not in current:
                disappeared.append(latest["nodes"][node_id]["name"])

        # Take new snapshot for next comparison
        self.take_snapshot()

        return {
            "snapshots_analyzed": len(snapshots),
            "rising": sorted(rising, key=lambda x: -x["weight_delta"]),
            "falling": sorted(falling, key=lambda x: x["weight_delta"]),
            "stable": stable,
            "new_nodes": new_nodes,
            "disappeared": disappeared,
            "graph_growth": {
                "nodes_now": len(current),
                "nodes_prev": latest["stats"]["total_nodes"],
                "node_delta": len(current) - latest["stats"]["total_nodes"],
                "edges_now": len(self.graph.edges),
                "edges_prev": latest["stats"]["total_edges"],
                "edge_delta": len(self.graph.edges) - latest["stats"]["total_edges"],
            },
        }

    def _baseline_analysis(self) -> dict:
        """First snapshot — no comparison possible yet."""
        projects = sorted(
            [n for n in self.graph.nodes.values() if n.type == "project"],
            key=lambda x: -x.weight,
        )

        return {
            "snapshots_analyzed": 0,
            "message": "First snapshot taken. Run again later for trajectory analysis.",
            "current_weights": {
                n.name: round(n.weight, 2) for n in projects
            },
            "rising": [],
            "falling": [],
            "new_nodes": [],
        }

    # ═══════════════════════════════════════════
    # PROJECTION — Where is each node heading?
    # ═══════════════════════════════════════════

    def project_futures(self, days: int = 30) -> list[dict]:
        """
        Project where each node will be in N days based on current trajectory.
        Uses weight, access patterns, and decay rates.
        """
        projections = []

        for node in self.graph.nodes.values():
            if node.id == "josh":
                continue

            # Current state
            weight = node.weight
            access = node.access_count

            # Decay factor (30-day half-life)
            last_accessed = datetime.fromisoformat(node.last_accessed) if hasattr(node, 'last_accessed') else datetime.now(timezone.utc)
            if isinstance(last_accessed, str):
                last_accessed = datetime.fromisoformat(last_accessed)
            if last_accessed.tzinfo is None:
                last_accessed = last_accessed.replace(tzinfo=timezone.utc)

            days_since_access = (datetime.now(timezone.utc) - last_accessed).days
            projected_days_at_end = days_since_access + days

            # Project weight using decay
            decay_factor = 0.5 ** (projected_days_at_end / 30)
            projected_weight = max(0.1, weight * decay_factor)

            # Classify trajectory
            if projected_weight > weight * 0.8:
                trajectory = "stable"
            elif projected_weight > weight * 0.5:
                trajectory = "declining"
            elif projected_weight > weight * 0.2:
                trajectory = "fading"
            else:
                trajectory = "near_death"

            projections.append({
                "node": node.name,
                "type": node.type,
                "weight_now": round(weight, 2),
                "weight_projected": round(projected_weight, 2),
                "days_since_access": days_since_access,
                "trajectory": trajectory,
                "action_needed": trajectory in ("fading", "near_death"),
                "prescription": {
                    "stable": "On track. No action needed.",
                    "declining": f"Declining — will be {projected_weight:.1f} in {days}d. Reinforce or let go.",
                    "fading": f"FADING — will be {projected_weight:.1f} in {days}d. Decide: reinforce or archive.",
                    "near_death": f"NEAR DEATH — will effectively disappear in {days}d. Save it or let it go.",
                }.get(trajectory, ""),
            })

        projections.sort(key=lambda x: x["weight_projected"])
        return projections

    # ═══════════════════════════════════════════
    # CROSSOVER DETECTION
    # ═══════════════════════════════════════════

    def find_crossovers(self, days: int = 30) -> list[dict]:
        """
        Find nodes whose trajectories will CROSS — when a rising
        node overtakes a falling one. These are priority shifts
        that haven't happened yet but are about to.
        """
        projections = {p["node"]: p for p in self.project_futures(days)}
        crossovers = []

        # Compare projects specifically
        projects = [n for n in self.graph.nodes.values() if n.type == "project"]

        for i, p1 in enumerate(projects):
            for p2 in projects[i+1:]:
                proj1 = projections.get(p1.name)
                proj2 = projections.get(p2.name)
                if not proj1 or not proj2:
                    continue

                # Check if they'll cross
                now_higher = p1.weight > p2.weight
                will_higher = proj1["weight_projected"] > proj2["weight_projected"]

                if now_higher != will_higher:
                    crossovers.append({
                        "rising": p2.name if will_higher else p1.name,
                        "falling": p1.name if will_higher else p2.name,
                        "current_weights": f"{p1.name}: {p1.weight:.1f}, {p2.name}: {p2.weight:.1f}",
                        "projected_weights": f"{proj1['node']}: {proj1['weight_projected']:.1f}, {proj2['node']}: {proj2['weight_projected']:.1f}",
                        "insight": (
                            f"CROSSOVER: '{p2.name if will_higher else p1.name}' will overtake "
                            f"'{p1.name if will_higher else p2.name}' within {days} days. "
                            f"Priority shift incoming."
                        ),
                    })

        return crossovers

    # ═══════════════════════════════════════════
    # FULL TEMPORAL REPORT
    # ═══════════════════════════════════════════

    def full_report(self, projection_days: int = 30) -> dict:
        trajectories = self.analyze_trajectories()
        futures = self.project_futures(projection_days)
        crossovers = self.find_crossovers(projection_days)

        # Highlight critical items
        at_risk = [f for f in futures if f["action_needed"]]
        thriving = [f for f in futures if f["trajectory"] == "stable" and f["weight_now"] >= 3]

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "projection_days": projection_days,
            "trajectories": trajectories,
            "at_risk": at_risk[:10],
            "thriving": thriving[:10],
            "crossovers": crossovers,
            "mechanism_16": {
                "name": "Temporal Projection",
                "description": (
                    "The graph is not a snapshot — it's a movie. "
                    "Weights decay, access patterns shift, priorities cross over. "
                    "The BEM sees the NEXT frame: what's about to peak, "
                    "what's about to fade, and where priorities will shift. "
                    "For ADHD brains that lose track of long-term trajectories, "
                    "this is the first system that holds the timeline for you."
                ),
            },
        }

        self._log(report)
        return report

    def _log(self, entry: dict):
        with open(self.temporal_log, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = TemporalEngine(graph)

    print("=" * 60)
    print("TEMPORAL ENGINE — Level 14: The Graph Through Time")
    print("What's becoming, not just what is.")
    print("=" * 60)

    report = engine.full_report(30)

    # Trajectories
    print(f"\n--- TRAJECTORY ANALYSIS ---")
    traj = report["trajectories"]
    if traj.get("message"):
        print(f"  {traj['message']}")
    else:
        print(f"  Rising: {len(traj.get('rising', []))}")
        print(f"  Falling: {len(traj.get('falling', []))}")
        print(f"  New: {len(traj.get('new_nodes', []))}")
        if traj.get("graph_growth"):
            g = traj["graph_growth"]
            print(f"  Graph: {g['nodes_prev']}→{g['nodes_now']} nodes (+{g['node_delta']}), "
                  f"{g['edges_prev']}→{g['edges_now']} edges (+{g['edge_delta']})")

    # At risk
    print(f"\n--- AT RISK (30-day projection) ---")
    for f in report["at_risk"][:7]:
        print(f"  ⚠ {f['node']} ({f['type']}): {f['weight_now']} → {f['weight_projected']} — {f['trajectory']}")
        print(f"    {f['prescription']}")

    # Thriving
    print(f"\n--- THRIVING ---")
    for f in report["thriving"][:5]:
        print(f"  ✓ {f['node']} ({f['type']}): {f['weight_now']} — stable")

    # Crossovers
    print(f"\n--- PRIORITY CROSSOVERS (30 days) ---")
    for c in report["crossovers"]:
        print(f"  🔀 {c['insight']}")

    if not report["crossovers"]:
        print("  No crossovers predicted — current priority order is stable")

    # Meta
    print(f"\n--- MECHANISM 16: TEMPORAL PROJECTION ---")
    print(f"  {report['mechanism_16']['description'][:150]}...")

    print(f"\n{'=' * 60}")
    print("The BEM sees the timeline.")
    print("What's about to peak. What's about to fade.")
    print("Where priorities will shift before they shift.")
    print("For the first time, an ADHD brain can see its own future.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
