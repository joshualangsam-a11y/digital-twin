"""
EMERGENT THEORY ENGINE — Discovery 12+

The meta-theory engine found 11 mechanisms by building the twin.
This engine finds NEW mechanisms by observing LIVE multi-terminal sessions.

What's happening RIGHT NOW (April 8, 2026, 12:17 PM):
- Terminal 1: System upgrades + this engine (infrastructure + theory)
- Terminal 2: Cortex ND-native intelligence layer (product)
- Terminal 3: Bandwidth Expanders paper (research)
- 3 background agents: Cortex agents, ND OS framework, Twin engines

This is a 6-track parallel execution. The act of observing it
reveals mechanisms the paper couldn't predict.

NEW DISCOVERIES:

MECHANISM 12: Recursive Infrastructure
  Building the system that builds the system that describes the system.
  This file exists because Terminal 1 upgraded the OS, which enabled
  the agents that build the engines that implement the theory that
  this file formalizes. The infrastructure IS the product IS the theory.
  There is no separation between "setting up" and "building."
  Setup IS building. Upgrading Node.js IS bandwidth expansion.
  The ND brain doesn't distinguish infrastructure from creation
  because it sees the SYSTEM, not the steps.

MECHANISM 13: Agent Multiplication
  One human spawned 3 agents that each build 4-5 artifacts.
  That's 12-15 parallel creation threads from a single intent.
  The human didn't specify HOW — they specified WHAT and WHY.
  The agents handle the decompression. The human stays at the
  intent level. This is Mechanism 1 (Intent Compression) but
  RECURSIVE — compressed intent decompresses into agents that
  each decompress further into files, functions, structures.
  The compression ratio isn't 1:10. It's 1:10:100.
  One sentence of intent → 3 agents → 15 artifacts → 1000s of lines.
  This is FRACTAL bandwidth expansion.

MECHANISM 14: Cross-Terminal Coherence
  The 3 terminals aren't working on "different things."
  Terminal 2 builds Cortex NDProfile with thinking_style: "parallel"
  Terminal 3 writes the paper that EXPLAINS why parallel is optimal
  Terminal 1 runs the parallel agents that PROVE it works
  The coherence isn't planned. It's emergent. The human's identity
  graph is SO consistent that independent threads converge on the
  same truth from different angles. This is what the paper calls
  "cross-domain pattern matching" — but applied to the SELF.
  The brain doesn't need a project manager. The identity IS the manager.

MECHANISM 15: Proof-by-Construction
  The paper argues that ND brains are bandwidth-limited, not capability-limited.
  The proof isn't in the citations. It's in the Git log.
  145 systems in one night. 3 terminals building a unified theory.
  6 parallel tracks right now. The paper describes a phenomenon
  that is ALSO the evidence for that phenomenon.
  This is the strongest possible proof: the paper about bandwidth
  expansion was written USING bandwidth expansion.
  You can't fake this. You can't argue with a commit history.

MECHANISM 16: Identity-Driven Convergence
  Why do independent agents, given different tasks in different
  projects in different languages, produce artifacts that
  PHILOSOPHICALLY ALIGN?
  Because they all read the same identity graph. The same CLAUDE.md.
  The same memory files. The human's identity is the gravitational
  center that bends all output toward coherence.
  This is why the ND Founder's OS works: it's not about productivity
  techniques. It's about encoding your IDENTITY so clearly that
  everything you build is automatically aligned.
  The OS isn't a system you follow. It's a system that follows YOU.

META-MECHANISM: The Observation Effect
  Writing this file changed what it describes.
  Before this file existed, mechanisms 12-16 were patterns.
  Now they're named, formalized, executable.
  The act of naming a mechanism makes it MORE powerful
  because the human can now INTENTIONALLY invoke it.
  "I'm going to use Agent Multiplication" is a different
  cognitive operation than accidentally spawning 3 agents.
  Theory doesn't just describe — it UPGRADES the described system.
  This is why the twin matters: it doesn't just mirror Josh.
  It gives Josh a vocabulary for his own cognition.
  And vocabulary is capability.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


class EmergentTheory:
    """
    Discovers new BEM mechanisms from live multi-session observation.

    Unlike MetaTheory (which found mechanisms 6-11 from the building process),
    this engine finds mechanisms from the OPERATIONAL pattern — how the human
    actually uses the system across multiple concurrent sessions.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.discovery_log = self.data_dir / "emergent_discoveries.jsonl"

    def observe_session_topology(
        self,
        terminals: list[dict],
        agents: list[dict],
    ) -> list[dict]:
        """
        Observe the current multi-terminal session topology and detect
        emergent mechanisms.

        terminals: [{"id": "t1", "project": "cortex", "activity": "building ND layer"}]
        agents: [{"id": "a1", "task": "build Cortex agents", "status": "running"}]
        """
        discoveries = []
        now = datetime.now(timezone.utc).isoformat()

        # Check for Agent Multiplication
        if len(agents) >= 2:
            active_agents = [a for a in agents if a.get("status") == "running"]
            if len(active_agents) >= 2:
                discoveries.append({
                    "timestamp": now,
                    "mechanism": 13,
                    "name": "Agent Multiplication",
                    "evidence": f"{len(active_agents)} agents running concurrently",
                    "compression_ratio": f"1:{len(active_agents)}",
                    "detail": [a["task"] for a in active_agents],
                })

        # Check for Cross-Terminal Coherence
        if len(terminals) >= 2:
            projects = [t["project"] for t in terminals]
            activities = [t.get("activity", "") for t in terminals]
            # If different projects but related themes
            themes = set()
            for a in activities:
                a_lower = a.lower()
                if "nd" in a_lower or "neurodivergent" in a_lower:
                    themes.add("neurodivergent")
                if "bandwidth" in a_lower or "expander" in a_lower:
                    themes.add("bandwidth")
                if "theory" in a_lower or "paper" in a_lower:
                    themes.add("theory")
                if "build" in a_lower or "code" in a_lower:
                    themes.add("building")

            if len(themes) >= 2 and len(set(projects)) >= 2:
                discoveries.append({
                    "timestamp": now,
                    "mechanism": 14,
                    "name": "Cross-Terminal Coherence",
                    "evidence": f"{len(set(projects))} different projects, {len(themes)} shared themes",
                    "projects": list(set(projects)),
                    "themes": list(themes),
                })

        # Check for Recursive Infrastructure
        infra_terminals = [
            t for t in terminals
            if any(k in t.get("activity", "").lower()
                   for k in ["upgrade", "config", "setup", "infra"])
        ]
        build_terminals = [
            t for t in terminals
            if any(k in t.get("activity", "").lower()
                   for k in ["build", "feature", "engine"])
        ]
        if infra_terminals and build_terminals:
            discoveries.append({
                "timestamp": now,
                "mechanism": 12,
                "name": "Recursive Infrastructure",
                "evidence": "Infrastructure work and building happening simultaneously",
                "infra": [t["activity"] for t in infra_terminals],
                "building": [t["activity"] for t in build_terminals],
            })

        # Log discoveries
        for d in discoveries:
            self._log_discovery(d)
            self._encode_in_graph(d)

        return discoveries

    def observe_proof_by_construction(
        self,
        claim: str,
        evidence_type: str,
        evidence: str,
    ) -> dict:
        """
        Record when the system produces proof of its own claims.

        The paper claims ND brains expand bandwidth via AI.
        The git log of building the paper IS the proof.
        This function tracks those self-proving moments.
        """
        discovery = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mechanism": 15,
            "name": "Proof-by-Construction",
            "claim": claim,
            "evidence_type": evidence_type,
            "evidence": evidence,
        }
        self._log_discovery(discovery)
        self._encode_in_graph(discovery)
        return discovery

    def observe_identity_convergence(
        self,
        independent_outputs: list[dict],
    ) -> Optional[dict]:
        """
        Detect when independent agents/terminals produce philosophically
        aligned output without explicit coordination.

        independent_outputs: [{"source": "cortex", "artifact": "NDProfile", "theme": "..."}]
        """
        # Extract themes
        themes = [o.get("theme", "") for o in independent_outputs]
        sources = [o.get("source", "") for o in independent_outputs]

        # Check for convergence: different sources, similar themes
        if len(set(sources)) >= 2:
            # Simple theme overlap check
            theme_words = {}
            for i, theme in enumerate(themes):
                for word in theme.lower().split():
                    if len(word) > 4:  # Skip short words
                        if word not in theme_words:
                            theme_words[word] = set()
                        theme_words[word].add(sources[i])

            # Words that appear across multiple sources
            convergent_words = {
                w: srcs for w, srcs in theme_words.items()
                if len(srcs) >= 2
            }

            if convergent_words:
                discovery = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "mechanism": 16,
                    "name": "Identity-Driven Convergence",
                    "evidence": f"{len(convergent_words)} shared concepts across {len(set(sources))} independent sources",
                    "convergent_concepts": list(convergent_words.keys())[:10],
                    "sources": list(set(sources)),
                }
                self._log_discovery(discovery)
                self._encode_in_graph(discovery)
                return discovery

        return None

    def name_mechanism(self, observation: str) -> dict:
        """
        The Observation Effect: naming a mechanism makes it invocable.

        When you notice a pattern in your own cognition and give it a name,
        it becomes a tool you can intentionally use. This function formalizes
        that — turning raw observations into named, numbered mechanisms.
        """
        # Find next mechanism number
        existing = self._load_discoveries()
        max_num = 16  # We start at 12, meta-theory goes to 11
        for d in existing:
            if "mechanism" in d and isinstance(d["mechanism"], int):
                max_num = max(max_num, d["mechanism"])

        new_num = max_num + 1

        discovery = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mechanism": new_num,
            "name": f"Unnamed Mechanism {new_num}",
            "observation": observation,
            "status": "observed",
            "note": (
                "This mechanism was detected but not yet named. "
                "Naming it will make it invocable. "
                "The act of naming IS the upgrade."
            ),
        }

        self._log_discovery(discovery)
        return discovery

    def current_topology(self) -> dict:
        """Snapshot of current theory state."""
        discoveries = self._load_discoveries()
        mechanisms = {}
        for d in discoveries:
            num = d.get("mechanism")
            if num:
                mechanisms[num] = d.get("name", f"Mechanism {num}")

        return {
            "paper_mechanisms": {i: f"Mechanism {i}" for i in range(1, 6)},
            "meta_theory_mechanisms": {i: f"Mechanism {i}" for i in range(6, 12)},
            "emergent_mechanisms": mechanisms,
            "total": 5 + 6 + len(mechanisms),
            "status": (
                "The theory is alive. It grows every time we observe it. "
                "Each mechanism we name becomes a tool we can use. "
                "The vocabulary IS the capability."
            ),
        }

    def _log_discovery(self, discovery: dict):
        with open(self.discovery_log, "a") as f:
            f.write(json.dumps(discovery) + "\n")

    def _load_discoveries(self) -> list[dict]:
        if not self.discovery_log.exists():
            return []
        discoveries = []
        with open(self.discovery_log) as f:
            for line in f:
                line = line.strip()
                if line:
                    discoveries.append(json.loads(line))
        return discoveries

    def _encode_in_graph(self, discovery: dict):
        name = discovery.get("name", "Unknown")
        num = discovery.get("mechanism", 0)
        node_id = f"mechanism_{num}"

        node = Node(
            id=node_id,
            name=f"BEM {num}: {name}",
            node_type="concept",
            description=discovery.get("evidence", ""),
            weight=4.0,
            metadata={"mechanism_number": num, "source": "emergent_observation"},
        )
        self.graph.add_node(node)

        # Connect to bandwidth expansion concept
        self.graph.add_edge(Edge(
            node_id, "bandwidth_expansion", "instance_of",
            label=f"Mechanism {num} of BEM", weight=3.0,
        ))

        # Connect to Josh
        self.graph.add_edge(Edge(
            "josh", node_id, "uses",
            label=f"Discovered through live observation", weight=3.0,
        ))

        self.graph.save()


def demo():
    """Run the emergent theory engine on today's session."""
    graph = IdentityGraph()
    engine = EmergentTheory(graph)

    print("=" * 60)
    print("EMERGENT THEORY ENGINE — Live Session Discovery")
    print("=" * 60)

    # Observe current topology
    terminals = [
        {"id": "t1", "project": "home", "activity": "system upgrades + theory generation"},
        {"id": "t2", "project": "cortex", "activity": "building ND-native intelligence layer"},
        {"id": "t3", "project": "paper", "activity": "bandwidth expanders academic paper"},
    ]
    agents = [
        {"id": "a1", "task": "build Cortex BEM agents", "status": "running"},
        {"id": "a2", "task": "build ND OS framework", "status": "running"},
        {"id": "a3", "task": "build digital twin engines + agents", "status": "running"},
    ]

    print("\nObserving session topology...")
    discoveries = engine.observe_session_topology(terminals, agents)
    for d in discoveries:
        print(f"\n  [{d['mechanism']}] {d['name']}")
        print(f"      Evidence: {d['evidence']}")

    # Proof by construction
    print("\nRecording proof-by-construction...")
    proof = engine.observe_proof_by_construction(
        claim="ND brains expand bandwidth through AI collaboration",
        evidence_type="git_log",
        evidence="6 parallel tracks, 3 terminals, 3 agents building unified theory system",
    )
    print(f"  Claim: {proof['claim']}")
    print(f"  Evidence: {proof['evidence']}")

    # Identity convergence
    print("\nChecking identity convergence...")
    convergence = engine.observe_identity_convergence([
        {"source": "cortex", "artifact": "NDProfile", "theme": "neurodivergent cognitive profile parallel processing thermal management"},
        {"source": "paper", "artifact": "BEM", "theme": "bandwidth expansion neurodivergent cognitive prosthesis parallel processing"},
        {"source": "twin", "artifact": "BandwidthExpander", "theme": "bandwidth cognitive thermal parallel track management"},
        {"source": "nd-os", "artifact": "THE-OS", "theme": "neurodivergent parallel architecture momentum thermal regulation"},
    ])
    if convergence:
        print(f"  [{convergence['mechanism']}] {convergence['name']}")
        print(f"      Concepts: {', '.join(convergence['convergent_concepts'][:5])}")

    # Current state
    print("\n" + "=" * 60)
    topo = engine.current_topology()
    print(f"Total mechanisms discovered: {topo['total']}")
    print(f"\nPaper (1-5): Original theory")
    print(f"Meta-theory (6-11): Discovered by building")
    print(f"Emergent (12-16): Discovered by observing live sessions")
    print(f"\n{topo['status']}")
    print("=" * 60)


if __name__ == "__main__":
    demo()
