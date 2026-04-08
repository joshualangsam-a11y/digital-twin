#!/usr/bin/env python3
"""
OVERNIGHT TWIN — Runs while Josh sleeps

Autonomous nightly cycle:
1. Re-ingest any new/changed memory files into the graph
2. Run decay (memories fade if not accessed)
3. Detect new pattern clusters
4. Scan for urgent actions (stale leads, unlinked goals)
5. Generate morning briefing data
6. Save everything

Designed to run via cron at 3 AM.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph
from engines.learning import LearningEngine
from engines.action import ActionEngine


def run_overnight():
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[{timestamp}] OVERNIGHT TWIN — Starting cycle")
    print("=" * 60)

    results = {
        "timestamp": timestamp,
        "phases": {},
    }

    # Phase 1: Load graph
    print("\n[1/6] Loading identity graph...")
    graph = IdentityGraph()
    results["phases"]["load"] = {
        "nodes": len(graph.nodes),
        "edges": len(graph.edges),
    }
    print(f"  {len(graph.nodes)} nodes, {len(graph.edges)} edges")

    # Phase 2: Re-ingest memories (check for new/changed files)
    print("\n[2/6] Checking for new memory files...")
    from scripts.ingest_memories import read_all_memories
    memories = read_all_memories()
    new_count = 0
    for mem in memories:
        # Check if this file is already represented in the graph
        filename = mem["filename"]
        exists = any(
            n.source_file == filename
            for n in graph.nodes.values()
        )
        if not exists and mem["type"] in ("project", "contact", "reference"):
            new_count += 1
    results["phases"]["ingest"] = {
        "total_memories": len(memories),
        "new_uningested": new_count,
    }
    print(f"  {len(memories)} total, {new_count} new/uningested")

    # Phase 3: Learning cycle (decay + consolidation)
    print("\n[3/6] Running learning cycle (decay + consolidation)...")
    learning = LearningEngine(graph)
    insights = learning.daily_integration()
    results["phases"]["learning"] = {
        "insights": len(insights),
        "types": [i["type"] for i in insights],
    }
    print(f"  {len(insights)} insights generated")
    for insight in insights:
        print(f"    [{insight['type']}] {insight['insight'][:80]}")

    # Phase 4: Proactive scan
    print("\n[4/6] Running proactive scan...")
    action = ActionEngine(graph)
    actions = action.scan_all()
    urgent = [a for a in actions if a.get("urgency", 0) >= 6]
    results["phases"]["scan"] = {
        "total_actions": len(actions),
        "urgent": len(urgent),
    }
    print(f"  {len(actions)} actions found, {len(urgent)} urgent")
    for a in urgent[:5]:
        print(f"    [{a['urgency']}/10] {a['action']}")

    # Phase 5: Generate overnight plan
    print("\n[5/6] Generating morning briefing data...")
    plan = action.generate_overnight_plan()
    results["phases"]["plan"] = plan

    # Phase 6: Compound metrics
    print("\n[6/6] Computing compound metrics...")
    compound = learning.compound_report()
    results["phases"]["compound"] = compound
    print(f"  Nodes: {compound['total_nodes']}")
    print(f"  Edges: {compound['total_edges']}")
    print(f"  Pattern clusters: {compound['pattern_clusters']}")
    print(f"  Avg weight: {compound['avg_node_weight']}")
    print(f"  Density: {compound['connection_density']}")

    # Save results
    output_dir = Path(os.path.expanduser("~/digital-twin/data/overnight"))
    output_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = output_dir / f"overnight_{date_str}.json"

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    # Also save as latest for morning briefing
    latest_path = output_dir / "latest.json"
    with open(latest_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"OVERNIGHT COMPLETE")
    print(f"  Results: {output_path}")
    print(f"  Insights: {len(insights)}")
    print(f"  Urgent: {len(urgent)}")
    print(f"  Graph: {compound['total_nodes']} nodes, {compound['total_edges']} edges")
    print(f"{'=' * 60}")

    return results


if __name__ == "__main__":
    run_overnight()
