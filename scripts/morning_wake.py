#!/usr/bin/env python3
"""
MORNING WAKE — Twin boots up for the day

Reads overnight results + current state → generates morning briefing.
Integrates with Claude Code's /morning-briefing skill.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph
from engines.reasoning import ReasoningEngine


def wake():
    print("=" * 60)
    print(f"DIGITAL TWIN — Morning Wake ({datetime.now().strftime('%I:%M %p')})")
    print("=" * 60)

    graph = IdentityGraph()
    reasoning = ReasoningEngine(graph)

    # Detect energy
    hour = datetime.now().hour
    if hour < 11:
        energy = "mud"
        energy_label = "MUD HOURS — light tasks only"
    elif hour < 13:
        energy = "ramp"
        energy_label = "RAMP UP — brain coming online"
    elif hour < 17:
        energy = "afternoon"
        energy_label = "AFTERNOON — hemp route + building"
    elif hour < 22:
        energy = "peak"
        energy_label = "PEAK — deep work, protect momentum"
    else:
        energy = "deep_night"
        energy_label = "DEEP NIGHT — creative peak"

    print(f"\nEnergy: {energy_label}")

    # Load overnight results if available
    overnight_path = Path(os.path.expanduser("~/digital-twin/data/overnight/latest.json"))
    if overnight_path.exists():
        with open(overnight_path) as f:
            overnight = json.load(f)

        print(f"\nOvernight cycle: {overnight['timestamp'][:10]}")

        scan = overnight.get("phases", {}).get("scan", {})
        if scan.get("urgent", 0) > 0:
            print(f"\n⚡ {scan['urgent']} URGENT ACTIONS:")
            # Load full scan from action engine
            from engines.action import ActionEngine
            action = ActionEngine(graph)
            actions = action.scan_all()
            for a in sorted(actions, key=lambda x: -x.get("urgency", 0))[:5]:
                if a.get("urgency", 0) >= 6:
                    print(f"  [{a['urgency']}/10] {a['action']}")

        compound = overnight.get("phases", {}).get("compound", {})
        if compound:
            print(f"\nGraph health: {compound.get('total_nodes', '?')} nodes, "
                  f"{compound.get('total_edges', '?')} edges, "
                  f"density {compound.get('connection_density', '?')}")

    # Generate priorities
    print(f"\nPriorities for {energy} energy:")
    priorities = reasoning.daily_priorities(energy)
    for i, p in enumerate(priorities[:5], 1):
        goals = ", ".join(p["feeds_goals"]) if p["feeds_goals"] else "—"
        match = "★" if p["energy_match"] > 1.0 else " "
        print(f"  {match} {i}. {p['project']} (weight: {p['weight']}) → {goals}")

    # Parallel tracks suggestion
    if energy in ("peak", "deep_night", "ramp"):
        print(f"\nParallel tracks (load 3+):")
        top = priorities[:3]
        for p in top:
            print(f"  → {p['project']}")

    print(f"\n{'=' * 60}")
    print("Twin awake. Go build.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    wake()
