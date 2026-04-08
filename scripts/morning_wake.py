#!/usr/bin/env python3
"""
MORNING WAKE — Twin boots up for the day

Reads overnight results + wakes with current energy level:
1. Run twin.wake() with energy detection
2. Load last night's overnight report
3. Run session bridge to restore yesterday's context
4. Show top 3 priorities from reasoning
5. Show urgent actions from proactive scan
6. Show compound metrics (graph growth, new patterns)

Output formatted for terminal + can pipe to /morning-briefing.
"""

import json
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.twin import BEM
from engines.session_bridge import SessionBridge


def detect_energy_label(energy: str) -> str:
    """Convert energy code to descriptive label."""
    labels = {
        "mud": "🌙 MUD HOURS — light tasks only",
        "ramp": "📈 RAMP UP — brain coming online",
        "afternoon": "⚙️ AFTERNOON — hemp route + building",
        "peak": "🔥 PEAK — deep work, protect momentum",
        "deep_night": "🌌 DEEP NIGHT — creative peak",
    }
    return labels.get(energy, f"❓ UNKNOWN ({energy})")


def wake():
    """Boot sequence with context restoration and priorities."""
    print(f"\n{'=' * 60}")
    print(f"DIGITAL TWIN WAKE — {datetime.now().strftime('%A, %I:%M %p')}")
    print(f"{'=' * 60}")

    try:
        # Initialize twin and get wake data
        twin = BEM()
        current_energy = twin._detect_energy()
        wake_result = twin.wake(energy=current_energy)

        # Display energy
        energy_label = detect_energy_label(current_energy)
        print(f"\n{energy_label}")

        # Load overnight report
        overnight_path = Path(os.path.expanduser("~/digital-twin/data/overnight_reports/latest.json"))
        overnight = {}
        if overnight_path.exists():
            try:
                with open(overnight_path) as f:
                    overnight = json.load(f)
                print(f"\nOvernight report: {overnight.get('date', 'unknown')}")
                if overnight.get('success'):
                    print(f"  ✓ Consolidation successful")
                else:
                    print(f"  ⚠ Consolidation had errors")
            except Exception as e:
                print(f"  ⚠ Could not load overnight report: {str(e)}")

        # Session bridge context
        print(f"\nSession context:")
        try:
            bridge = SessionBridge(twin.graph)
            session_start = bridge.start_session(session_type="work")
            restored = session_start.get("restored", {})
            print(f"  Restored from previous session:")
            print(f"    • Unfinished thoughts: {len(restored.get('unfinished_thoughts', []))}")
            print(f"    • Aha moments: {len(restored.get('aha_moments', []))}")
            print(f"    • Context nodes: {len(restored.get('context_nodes', []))}")
        except Exception as e:
            print(f"  ⚠ Session bridge error: {str(e)}")

        # Top 3 priorities
        print(f"\n⭐ TOP 3 PRIORITIES ({current_energy} energy):")
        priorities = wake_result.get("priorities", [])
        for i, p in enumerate(priorities[:3], 1):
            weight = p.get("weight", 0)
            project = p.get("project", "?")
            feeds = p.get("feeds_goals", [])
            goal_str = " → " + ", ".join(feeds) if feeds else ""
            print(f"  {i}. {project} (weight: {weight}){goal_str}")

        # Urgent actions
        urgent_actions = wake_result.get("urgent_actions", [])
        if urgent_actions:
            print(f"\n🚨 URGENT ACTIONS ({len(urgent_actions)}):")
            for a in urgent_actions[:5]:
                urgency = a.get("urgency", 0)
                action_text = a.get("action", "?")
                print(f"  [{urgency}/10] {action_text}")
        else:
            print(f"\n✓ No urgent actions")

        # Compound metrics
        compound = wake_result.get("compound_report", {})
        if compound:
            nodes = compound.get("total_nodes", 0)
            edges = compound.get("total_edges", 0)
            density = compound.get("connection_density", 0)
            print(f"\n📊 COMPOUND METRICS:")
            print(f"  Graph: {nodes} nodes, {edges} edges")
            print(f"  Density: {density:.2f}")
            print(f"  Clusters: {compound.get('pattern_clusters', 0)}")

            # What grew?
            hubs = compound.get("cognitive_hubs", [])
            if hubs:
                print(f"  Top hub: {hubs[0].get('name', '?')} "
                      f"({hubs[0].get('connections', 0)} connections)")

        # Parallel tracks suggestion
        if current_energy in ("peak", "deep_night", "ramp"):
            print(f"\n🔀 PARALLEL TRACKS (load 3+):")
            for p in priorities[:3]:
                print(f"  → {p.get('project', '?')}")

        print(f"\n{'=' * 60}")
        print(f"Twin awake. Energy: {current_energy}. Go build.")
        print(f"{'=' * 60}\n")

    except Exception as e:
        print(f"\n✗ ERROR in wake sequence: {str(e)}")
        traceback.print_exc()
        print(f"\n{'=' * 60}\n")


if __name__ == "__main__":
    wake()
