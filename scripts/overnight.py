#!/usr/bin/env python3
"""
OVERNIGHT TWIN — Runs while Josh sleeps

Autonomous nightly cycle:
1. Run twin.sleep() for daily consolidation (decay, patterns, insights)
2. Run session bridge to save session state & context
3. Run emergent theory engine to crystallize new discoveries
4. Generate "today's compound report" showing what grew
5. Save everything to data/overnight_reports/YYYY-MM-DD.json

Designed to run via cron at 3 AM or manually.
"""

import json
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.twin import BEM
from engines.session_bridge import SessionBridge
from engines.emergent_theory import EmergentTheory


def run_overnight():
    """Execute the overnight consolidation cycle."""
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"\n{'=' * 60}")
    print(f"OVERNIGHT TWIN — {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    print(f"{'=' * 60}")

    results = {
        "timestamp": timestamp,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "phases": {},
        "success": True,
    }

    try:
        # Phase 1: Twin sleep (consolidation, decay, insights)
        print("\n[1/4] Twin sleep cycle (memory consolidation)...")
        twin = BEM()
        sleep_result = twin.sleep()
        results["phases"]["sleep"] = {
            "insights": len(sleep_result.get("insights", [])),
            "insight_types": [i.get("type") for i in sleep_result.get("insights", [])],
            "cycle": sleep_result.get("cycle", 0),
        }
        print(f"  Cycle #{sleep_result.get('cycle', 0)}")
        print(f"  Insights: {len(sleep_result.get('insights', []))}")
        for insight in sleep_result.get("insights", [])[:3]:
            print(f"    [{insight.get('type')}] {insight.get('insight', '')[:70]}...")

        # Phase 2: Session bridge (save context for next session)
        print("\n[2/4] Session bridge (saving context)...")
        try:
            bridge = SessionBridge(twin.graph)
            # Start a session to capture the overnight insights
            if not bridge.current_session_id:
                bridge.start_session(session_type="overnight")

            # Record insights as aha moments
            for insight in sleep_result.get("insights", [])[:3]:
                try:
                    bridge.record_aha_moment(
                        insight.get("insight", ""),
                        novelty="consolidation"
                    )
                except Exception:
                    pass  # Silently skip if recording fails

            # End session and save state
            session_state = bridge.end_session()
            results["phases"]["session_bridge"] = {
                "session_id": session_state.get("session_id"),
                "state_saved": True,
            }
            print(f"  Session state saved")
        except Exception as e:
            print(f"  ⚠ Session bridge error: {str(e)}")
            results["phases"]["session_bridge"] = {"error": str(e)}

        # Phase 3: Emergent theory (crystallize discoveries)
        print("\n[3/4] Emergent theory engine (crystallizing discoveries)...")
        try:
            emergent = EmergentTheory(twin.graph)
            discoveries = emergent.observe_session_topology([], [])
            topology = emergent.current_topology()
            results["phases"]["emergent"] = {
                "new_discoveries": len(discoveries),
                "total_mechanisms": topology.get("total", 0),
                "status": topology.get("status", "unknown"),
            }
            print(f"  Mechanisms: {topology.get('total', 0)} total")
            print(f"  New discoveries: {len(discoveries)}")
        except Exception as e:
            print(f"  ⚠ Emergent theory error: {str(e)}")
            results["phases"]["emergent"] = {"error": str(e)}

        # Phase 4: Compound report (growth metrics)
        print("\n[4/4] Compound report (growth metrics)...")
        compound = sleep_result.get("compound_report", {})
        results["phases"]["compound"] = compound
        print(f"  Graph size: {compound.get('total_nodes', '?')} nodes, "
              f"{compound.get('total_edges', '?')} edges")
        print(f"  Clusters: {compound.get('pattern_clusters', '?')}")
        print(f"  Density: {compound.get('connection_density', '?'):.2f}")
        print(f"  Avg weight: {compound.get('avg_node_weight', '?'):.2f}")

        # Cognitive hubs (what grew?)
        hubs = compound.get("cognitive_hubs", [])
        if hubs:
            print(f"\n  Top hubs:")
            for hub in hubs[:3]:
                print(f"    • {hub.get('name', '?')}: {hub.get('connections', 0)} connections")

    except Exception as e:
        print(f"\n  ERROR: {str(e)}")
        traceback.print_exc()
        results["success"] = False
        results["error"] = str(e)

    # Save results
    output_dir = Path(os.path.expanduser("~/digital-twin/data/overnight_reports"))
    output_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = output_dir / f"{date_str}.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    # Also save as latest for morning briefing
    latest_path = output_dir / "latest.json"
    with open(latest_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"OVERNIGHT COMPLETE")
    print(f"  Report: {output_path}")
    print(f"  Status: {'✓ SUCCESS' if results['success'] else '✗ FAILED'}")
    print(f"{'=' * 60}\n")

    return results


if __name__ == "__main__":
    run_overnight()
