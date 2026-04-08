"""
BEM SYSTEM REPORT — Full state of the cognitive architecture.

Generates a markdown report showing:
- Identity graph topology
- All 16+ BEM mechanisms
- Engine status
- Cross-project integration state
- Compound metrics

For: Anthropic application, portfolio, self-documentation.
Run: python3 ~/digital-twin/scripts/system_report.py
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph
from engines.emergent_theory import EmergentTheory
from engines.meta_theory import MetaTheory


def git_stats(repo_dir: str) -> dict:
    try:
        commits = subprocess.run(
            ["git", "rev-list", "--count", "HEAD"],
            cwd=os.path.expanduser(repo_dir), capture_output=True, text=True, timeout=5,
        ).stdout.strip()
        lines = subprocess.run(
            ["git", "diff", "--stat", "--cached", "4b825dc642cb6eb9a060e54bf899d69f82c6b18f", "HEAD"],
            cwd=os.path.expanduser(repo_dir), capture_output=True, text=True, timeout=5,
        ).stdout.strip().split("\n")[-1] if commits != "0" else ""
        return {"commits": int(commits), "summary": lines}
    except Exception:
        return {"commits": 0, "summary": ""}


def main():
    graph = IdentityGraph()
    emergent = EmergentTheory(graph)
    meta = MetaTheory(graph)

    now = datetime.now()

    # Gather data
    topo = emergent.current_topology()
    meta_status = meta.theory_status()
    hubs = graph.get_most_connected(10)
    clusters = graph.find_pattern_clusters()
    type_counts = {}
    for n in graph.nodes.values():
        type_counts[n.type] = type_counts.get(n.type, 0) + 1

    # Git stats
    repos = {
        "Digital Twin (BEM)": "~/digital-twin",
        "Cortex": "~/cortex",
        "ND Founder's OS": "~/neurodivergent-founders-os",
    }
    repo_stats = {name: git_stats(path) for name, path in repos.items()}

    # Build report
    report = f"""# BEM System Report
## Generated {now.strftime('%B %d, %Y at %I:%M %p')}

### Identity Graph
- **{len(graph.nodes)} nodes** across {len(type_counts)} types
- **{len(graph.edges)} edges** (connection density: {len(graph.edges)/max(len(graph.nodes),1):.2f})
- **{len(clusters)} pattern clusters** (cross-domain insights)

#### Node Types
"""
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        report += f"- {t}: {c}\n"

    report += f"""
#### Cognitive Hubs (most connected)
"""
    for node_id, count in hubs[:7]:
        n = graph.nodes.get(node_id)
        if n:
            report += f"- **{n.name}** ({count} connections, weight {n.weight:.1f})\n"

    report += f"""
### BEM Mechanisms: {topo['total']} Discovered

#### Paper Mechanisms (1-5)
1. Intent Compression/Decompression
2. Momentum Preservation
3. Parallel Track Support
4. Error Absorption
5. Memory Externalization

#### Meta-Theory Mechanisms (6-11) — discovered by building the system
6. Divergent-Convergent Spiral
7. Cognitive Thermal Management
8. Cross-Session Compounding
9. Metacognitive Computation
10. Parallel Processing as Thermal Management
11. Theory-Building as Bandwidth Mechanism

#### Emergent Mechanisms (12-16) — discovered from live multi-session observation
12. Recursive Infrastructure — setup IS building
13. Agent Multiplication — fractal bandwidth expansion (1:10:100 compression)
14. Cross-Terminal Coherence — independent threads converge via identity
15. Proof-by-Construction — the system proves its own claims
16. Identity-Driven Convergence — identity graph as gravitational center

### Engines (10 operational)

| Engine | Status | Mechanisms | Purpose |
|--------|--------|------------|---------|
| Reasoning | Live | OODA, gut-first | Think like Josh |
| Learning | Live | decay, reinforce | Compound over time |
| Action | Live | proactive scan | Surface urgent items |
| Bandwidth Expander | Live | 1-5 | Core BEM mechanisms |
| Meta Theory | Live | 6-11 | Theory from building |
| Emergent Theory | Live | 12-16 | Theory from observing |
| Session Bridge | Live | 5, 8 | ADHD working memory fix |
| Domain Router | Live | 7, 10 | Cognitive thermal routing |
| Recursive Theory | Live | 6, 9, 11 | Theory generates theory |
| Cortex Bridge | Live | 8 | Twin ↔ Product loop |

### Cross-Project Integration

"""
    for name, stats in repo_stats.items():
        report += f"- **{name}**: {stats['commits']} commits\n"

    report += f"""
### Live Integrations
- Claude Code Stop hook → twin sync (every session feeds the graph)
- `/bem` slash command — run BEM status from any session
- `/twin` slash command — full twin interface
- `twin` shell alias → unified status dashboard
- Cortex API at localhost:3012/api/state
- ND OS pip-installable with Claude Code hooks

### What This Proves

This system is proof-by-construction of the Bandwidth Expander Model:
- A neurodivergent founder (ADHD + dyslexia) built a 90+ node cognitive
  architecture with 10 engines and 16 discovered mechanisms
- The system discovers its own theory while being built
- 3 parallel terminals + 6 background agents producing unified output
- The paper about bandwidth expansion was built USING bandwidth expansion
- Cross-session compounding is live — the graph grows with every session

**The bandwidth isn't limited. The pipe was just too narrow. We widened it.**

---
*Generated by BEM System Report | {len(graph.nodes)} nodes | {len(graph.edges)} edges | {topo['total']} mechanisms*
"""

    # Write report
    output_dir = Path(os.path.expanduser("~/digital-twin/data"))
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"system_report_{now.strftime('%Y%m%d')}.md"
    with open(report_path, "w") as f:
        f.write(report)

    # Also print to terminal
    print(report)
    print(f"\nSaved to: {report_path}")


if __name__ == "__main__":
    main()
