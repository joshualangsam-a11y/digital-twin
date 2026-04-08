"""
UNIFIED STATUS — All systems in one view.

Twin + Cortex + ND OS + Theory state.
Run: python3 ~/digital-twin/scripts/unified_status.py
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, os.path.expanduser("~/neurodivergent-founders-os"))

from core.identity_graph import IdentityGraph
from engines.emergent_theory import EmergentTheory


def check_cortex() -> dict:
    """Check if Cortex is running."""
    try:
        import urllib.request
        with urllib.request.urlopen("http://localhost:3012/api/state", timeout=2) as r:
            return {"status": "online", "data": json.loads(r.read())}
    except Exception:
        return {"status": "offline"}


def check_nd_os() -> dict:
    """Check ND OS state."""
    try:
        from nd_os.energy import EnergyMapper
        from nd_os.profile import NDProfile
        profile = NDProfile.from_preset("adhd_parallel")
        energy = EnergyMapper(profile)
        snapshot = energy.current_state()
        phase = snapshot.state.value if hasattr(snapshot.state, 'value') else str(snapshot.state)
        return {"status": "loaded", "energy_phase": phase}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_git_status(project_dir: str) -> dict:
    """Quick git status for a project."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=os.path.expanduser(project_dir),
            capture_output=True, text=True, timeout=5,
        )
        changes = len([l for l in result.stdout.strip().split("\n") if l])
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            cwd=os.path.expanduser(project_dir),
            capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        return {"changes": changes, "branch": branch}
    except Exception:
        return {"changes": 0, "branch": "unknown"}


def main():
    print("=" * 60)
    print(f"  UNIFIED STATUS — {datetime.now().strftime('%I:%M %p %b %d')}")
    print("=" * 60)

    # Identity Graph
    graph = IdentityGraph()
    print(f"\n  Identity Graph: {len(graph.nodes)} nodes, {len(graph.edges)} edges")

    # Theory State
    engine = EmergentTheory(graph)
    topo = engine.current_topology()
    print(f"  BEM Mechanisms: {topo['total']} (paper:5 + meta:6 + emergent:{len(topo['emergent_mechanisms'])})")

    # Cortex
    cortex = check_cortex()
    print(f"\n  Cortex: {cortex['status'].upper()}", end="")
    if cortex["status"] == "online":
        print(f" — localhost:3012")
    else:
        print()

    # ND OS
    nd = check_nd_os()
    print(f"  ND OS: {nd['status'].upper()}", end="")
    if "energy_phase" in nd:
        print(f" — energy: {nd['energy_phase']}")
    else:
        print()

    # Projects
    projects = {
        "cortex": "~/cortex",
        "digital-twin": "~/digital-twin",
        "nd-founders-os": "~/neurodivergent-founders-os",
    }

    print(f"\n  Git Status:")
    for name, path in projects.items():
        git = check_git_status(path)
        marker = "●" if git["changes"] > 0 else "○"
        print(f"    {marker} {name}: {git['changes']} changes [{git['branch']}]")

    # Active processes
    try:
        result = subprocess.run(
            ["pgrep", "-c", "claude"],
            capture_output=True, text=True, timeout=5,
        )
        claude_count = int(result.stdout.strip())
    except Exception:
        claude_count = 0

    print(f"\n  Claude instances: {claude_count}")
    print(f"  Parallel tracks: {claude_count + 1}")  # +1 for this script

    print("\n" + "=" * 60)
    print(f"  {topo['status']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
