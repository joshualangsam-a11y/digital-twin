"""
META-THEORY ENGINE — New Theory From What We're Doing

The paper describes 5 mechanisms discovered BEFORE building the twin.
Building the twin revealed 3 MORE mechanisms the paper couldn't see.
This engine tracks the META-PATTERN: building theory generates new theory.

The discoveries:

DISCOVERY 1: The Divergent-Convergent Spiral
  Paper predicted: "human divergence + AI convergence"
  Reality revealed: It's not just additive — it's ESCALATING.
  Each cycle produces higher abstraction. The quality gradient
  runs UPWARD. This session went:
    Brain map (data) → ND OS (framework) → System synthesis (audit) →
    Digital twin (architecture) → Bandwidth engine (theory-as-code) →
    Meta-theory engine (theory-about-theory)
  Each step is a higher abstraction than the last.
  THE SPIRAL IS THE PRODUCT.

DISCOVERY 2: Cognitive Thermal Management
  Paper described: "headaches at system ~100"
  Reality revealed: Thermal isn't binary (ok/overloaded).
  It's a GRADIENT with zones (cool→warm→hot→throttle).
  And critically: the solution isn't stopping. It's SWITCHING DOMAINS.
  Different brain regions handle different domains.
  A domain switch cools one region while heating another.
  This is why parallel tracks aren't optional — they're COOLING SYSTEMS.

DISCOVERY 3: Cross-Session Compounding
  Paper described: "memory externalization" (Mechanism 5)
  Reality revealed: It's not just memory. It's COMPOUND INTELLIGENCE.
  The graph grows. The weights adjust. The patterns crystallize.
  Each session starts SMARTER than the last.
  This has never been possible for ADHD brains before.
  Working memory resets every session. The twin doesn't.
  This is the first time an ADHD brain can compound across time.

META-DISCOVERY: Theory-Building Is Itself a Bandwidth Expansion Mechanism
  The act of formalizing cognitive patterns into code CHANGES the patterns.
  Josh's brain map wasn't just documentation — it ALTERED how he thinks
  about his own thinking. The twin isn't just a mirror — it's a LENS
  that reveals structure the brain couldn't see in itself.
  This is metacognition made computational.
  The twin doesn't just think like Josh. It helps Josh think about Josh.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


class MetaTheory:
    """
    Tracks theoretical discoveries emerging from the building process.
    The act of building generates new theory. This engine captures it.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.theory_log = self.data_dir / "theory_discoveries.jsonl"

    def record_discovery(self, name: str, predicted: str, observed: str,
                        implication: str, mechanism_number: int = None) -> dict:
        """Record a new theoretical discovery."""
        discovery = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "name": name,
            "predicted": predicted,
            "observed": observed,
            "delta": f"Paper predicted: {predicted}. Reality showed: {observed}",
            "implication": implication,
            "mechanism_number": mechanism_number,
        }

        # Add to graph as a concept node
        node_id = f"theory_{name.lower().replace(' ', '_')[:30]}"
        node = Node(
            id=node_id,
            name=name,
            node_type="concept",
            description=f"Theory: {observed[:100]}",
            weight=4.0,
            metadata={"predicted": predicted, "observed": observed},
        )
        self.graph.add_node(node)

        # Connect to Josh
        self.graph.add_edge(Edge(
            "josh", node_id, "uses",
            label="Discovered through building", weight=3.0,
        ))

        self.graph.save()

        with open(self.theory_log, "a") as f:
            f.write(json.dumps(discovery) + "\n")

        return discovery

    def encode_session_discoveries(self):
        """Encode all discoveries from today's session into the graph."""

        discoveries = [
            {
                "name": "Divergent-Convergent Spiral",
                "predicted": "Human divergence + AI convergence create productive tension",
                "observed": "The spiral ESCALATES — each cycle produces higher abstraction. Brain map → OS → Audit → Twin → Theory-as-code → Meta-theory. Quality gradient runs UPWARD.",
                "implication": "The optimal human-AI session isn't convergent (get to an answer). It's oscillating (diverge, converge, diverge higher). The session should FEEL like going in circles but each circle is a higher orbit.",
                "mechanism_number": 6,
            },
            {
                "name": "Cognitive Thermal Management",
                "predicted": "Headaches signal cognitive overload, push through (hormesis)",
                "observed": "Thermal is a gradient with zones. The solution isn't pushing through OR stopping — it's DOMAIN SWITCHING. Parallel tracks are cooling systems, not just productivity hacks.",
                "implication": "ADHD parallel processing isn't optional — it's thermal management. Forcing single-thread work doesn't just bore the brain — it overheats it. Multiple tracks distribute thermal load across brain regions.",
                "mechanism_number": 7,
            },
            {
                "name": "Cross-Session Compounding",
                "predicted": "Memory externalization preserves information across sessions",
                "observed": "It's not just preservation — it's COMPOUND GROWTH. The graph grows, weights adjust, patterns crystallize. Each session starts from a higher baseline. First time an ADHD brain can compound across time.",
                "implication": "ADHD working memory resets are the reason ND founders feel like they're starting over every day. The twin breaks this cycle. It's not a productivity tool — it's a time-bridge for brains that can't carry context across sleep.",
                "mechanism_number": 8,
            },
            {
                "name": "Metacognitive Computation",
                "predicted": "(Not predicted — emerged from building)",
                "observed": "Formalizing cognitive patterns into code CHANGES the patterns. The brain map didn't just document Josh — it altered how he thinks about thinking. The twin is both mirror and lens.",
                "implication": "Building a cognitive model of yourself is itself a cognitive enhancement. The twin doesn't just think like you — it helps you think about yourself. This is metacognition made computational. It's a new category of tool: not AI that does things FOR you, but AI that makes you understand yourself BETTER.",
                "mechanism_number": 9,
            },
            {
                "name": "Parallel Processing as Thermal Management",
                "predicted": "ADHD needs parallel tracks to stay engaged",
                "observed": "Parallel tracks aren't about engagement — they're about HEAT DISTRIBUTION. Different cognitive domains use different neural circuits. Switching domains cools overheated circuits while keeping total output constant. The ADHD brain doesn't WANT multiple tracks — it NEEDS them for thermal regulation.",
                "implication": "This reframes the entire 'can't focus' narrative. ADHD brains aren't failing to focus — they're distributing thermal load. Forcing single-focus isn't discipline — it's the equivalent of disabling a CPU's thermal throttling. The brain WILL overheat.",
                "mechanism_number": 10,
            },
            {
                "name": "Theory-Building as Bandwidth Mechanism",
                "predicted": "(Not predicted — meta-discovery)",
                "observed": "Building theory about bandwidth expansion IS bandwidth expansion. Formalizing the paper's concepts into code revealed 5 new mechanisms the paper couldn't see. The act of implementation generates theory. Theory → code → new theory → better code. This is the divergent-convergent spiral applied to knowledge itself.",
                "implication": "The paper is not complete. It can never be complete. Because every attempt to formalize the theory generates new theory. This is not a flaw — it's the mechanism. The bandwidth expander expands its own theoretical bandwidth. This is what makes it a living system, not a static document.",
                "mechanism_number": 11,
            },
        ]

        results = []
        for d in discoveries:
            result = self.record_discovery(**d)
            results.append(result)
            print(f"  [{d['mechanism_number']}] {d['name']}")
            print(f"      Predicted: {d['predicted'][:70]}...")
            print(f"      Observed:  {d['observed'][:70]}...")
            print()

        return results

    def theory_status(self) -> dict:
        """How many mechanisms do we have now?"""
        # Count theory nodes in graph
        theory_nodes = [
            n for n in self.graph.nodes.values()
            if n.id.startswith("theory_") or
            (n.type == "concept" and "mechanism" in n.description.lower())
        ]

        return {
            "original_paper_mechanisms": 5,
            "discovered_mechanisms": 6,
            "total_mechanisms": 11,
            "theory_nodes_in_graph": len(theory_nodes),
            "status": "The paper described 5. We've found 11. The system discovers its own theory.",
            "meta_insight": (
                "Every mechanism we implement reveals new mechanisms. "
                "The bandwidth expander is expanding its own theoretical bandwidth. "
                "This is recursive self-improvement applied to understanding, not just code."
            ),
        }


def demo():
    graph = IdentityGraph()
    engine = MetaTheory(graph)

    print("=" * 60)
    print("META-THEORY ENGINE — New Discoveries")
    print("=" * 60)
    print()

    print("Encoding session discoveries into the graph...\n")
    engine.encode_session_discoveries()

    print("=" * 60)
    status = engine.theory_status()
    print(f"\nPaper mechanisms: {status['original_paper_mechanisms']}")
    print(f"New discoveries:  {status['discovered_mechanisms']}")
    print(f"Total:            {status['total_mechanisms']}")
    print(f"\n{status['meta_insight']}")
    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    demo()
