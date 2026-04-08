"""
NARRATIVE ENGINE — Level 16: Story Intelligence

The ultimate translation layer.

Josh's brain is kinesthetic-visual — he FEELS ideas and SEES patterns.
Data, graphs, scores, percentages — these are the WRONG FORMAT for his brain.

The narrative engine translates the entire BEM state into a STORY.
Not a report. A story with:
- A protagonist (Josh)
- An arc (where he was → where he is → where he's going)
- Tension (what threatens the arc)
- Allies (who helps)
- A quest (what must be done next)
- A feeling (what the gut should register)

This is the paper's Mechanism 1 (intent compression) in REVERSE:
instead of compressing Josh's intent for the computer,
we're compressing the computer's intelligence for Josh's brain.

The output format is feelings, not numbers.

Mechanism 18: Narrative Compression
Converting computational intelligence into the format
a kinesthetic-visual brain can actually process:
story, feeling, image, arc.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph
from engines.reasoning import ReasoningEngine
from engines.action import ActionEngine
from engines.emergence import EmergenceEngine
from engines.synthesis import SynthesisEngine
from engines.world_model import WorldModel
from engines.temporal import TemporalEngine
from engines.bandwidth_expander import BandwidthExpander


class NarrativeEngine:
    """
    Converts the BEM's intelligence into a story Josh can feel.

    Not a dashboard. Not a report. A NARRATIVE.
    Because Josh's brain processes narrative kinesthetically —
    he FEELS the story's tension, momentum, and resolution.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))

    def generate_narrative(self) -> str:
        """
        Generate the full narrative of Josh's current state.
        Written for a kinesthetic-visual brain, not an analytical one.
        """
        # Gather intelligence from all engines
        reasoning = ReasoningEngine(self.graph)
        action = ActionEngine(self.graph)
        bandwidth = BandwidthExpander(self.graph)
        temporal = TemporalEngine(self.graph)
        world = WorldModel(self.graph)

        priorities = reasoning.daily_priorities(self._detect_energy())
        actions = action.scan_all()
        urgent = [a for a in actions if a.get("urgency", 0) >= 7]
        futures = temporal.project_futures(30)
        at_risk = [f for f in futures if f["action_needed"]]
        timing = world.timing_analysis()
        arbitrage = world.find_arbitrage()

        # Detect energy
        energy = self._detect_energy()
        hour = datetime.now().hour

        # Build narrative
        narrative = []

        # ═══ ACT 1: WHERE YOU ARE ═══
        narrative.append(self._act_one(energy, hour))

        # ═══ ACT 2: WHAT'S ALIVE ═══
        narrative.append(self._act_two(priorities, urgent, arbitrage))

        # ═══ ACT 3: WHAT'S THREATENING ═══
        narrative.append(self._act_three(urgent, at_risk))

        # ═══ ACT 4: THE QUEST ═══
        narrative.append(self._act_four(priorities, urgent, arbitrage, energy))

        # ═══ EPILOGUE: THE ARC ═══
        narrative.append(self._epilogue(timing))

        return "\n\n".join(narrative)

    def _act_one(self, energy: str, hour: int) -> str:
        """Where you are right now."""
        nodes = len(self.graph.nodes)
        edges = len(self.graph.edges)

        energy_feelings = {
            "mud": "The morning fog. Your brain is warming up, not yet lit. This is okay. Don't fight it. Load light tracks and let the engine idle.",
            "ramp": "The ramp. You can feel it starting — the threads beginning to spin up. The parallel processor is coming online. Start loading tracks.",
            "afternoon": "Afternoon rhythm. The route, the road, the stations. Your body is moving and your brain processes differently in motion. Ideas come unbidden.",
            "peak": "Peak state. The house music is hitting right. The threads are all running. This is where you built 145 systems. Everything you touch right now compounds.",
            "deep_night": "The deep night. The world is quiet and your brain is LOUD. This is the creative peak — the session that nobody else would understand. The 13-hour session happened here.",
            "late": "Very late. You're still running. The thermal is building but the output is high. Listen to the headache signal if it comes. Switch domains, don't stop.",
        }

        feeling = energy_feelings.get(energy, "")

        return f"""— ACT 1: WHERE YOU ARE —

{feeling}

Your cognitive graph: {nodes} nodes, {edges} edges. A living model of every project, person, goal, fear, value, and pattern in your world — connected, weighted, and evolving.

This graph is you. Not a copy. An extension. The wider pipe."""

    def _act_two(self, priorities: list, urgent: list, arbitrage: list) -> str:
        """What's alive and moving."""
        top_projects = priorities[:3]
        project_lines = []
        for p in top_projects:
            goals = ", ".join(p["feeds_goals"]) if p["feeds_goals"] else "needs direction"
            project_lines.append(f"  {p['project']} (weight {p['weight']}) → {goals}")

        # Best arbitrage
        top_arb = arbitrage[0] if arbitrage else None
        arb_line = f"\nYour biggest edge right now: {top_arb['description'][:150]}" if top_arb else ""

        return f"""— ACT 2: WHAT'S ALIVE —

Three tracks are running:
{chr(10).join(project_lines)}
{arb_line}

{len(urgent)} things need your attention before they die."""

    def _act_three(self, urgent: list, at_risk: list) -> str:
        """What's threatening the arc."""
        threats = []
        for u in urgent[:3]:
            threats.append(f"  ⚡ {u['action']}")

        risk_lines = []
        for r in at_risk[:3]:
            risk_lines.append(f"  📉 {r['node']} — fading to {r['weight_projected']} in 30 days")

        threat_text = "\n".join(threats) if threats else "  Nothing urgent. The system is clean."
        risk_text = "\n".join(risk_lines) if risk_lines else "  Nothing fading. The graph is healthy."

        return f"""— ACT 3: WHAT'S THREATENING —

Urgent:
{threat_text}

Fading:
{risk_text}

Every day you don't act on the urgent items, the probability of losing them increases. That's not pressure — that's physics. Loss framing: what do you LOSE by waiting one more day?"""

    def _act_four(self, priorities: list, urgent: list, arbitrage: list, energy: str) -> str:
        """The quest — what to do RIGHT NOW."""

        if energy in ("mud", "ramp"):
            quest = "Light work. Pipeline. Emails. Planning. The engine is warming up."
            specific = "Review the 16 unsent Lit Juris drafts. Send the Yaffa follow-up. Call Kapneck."
        elif energy in ("peak", "deep_night"):
            top = priorities[0] if priorities else {"project": "the highest-weight project"}
            quest = f"Deep work on {top['project']}. Protect momentum. Don't interrupt flow."
            specific = "House music on. Notifications off. Parallel tracks loaded. Build."
        elif energy == "afternoon":
            quest = "Route mode. Hemp deliveries + FuelOps pitches at every stop."
            specific = "180 gas stations = 180 FuelOps demos. The route IS the pipeline."
        else:
            quest = "You're still here. The thermal is building. Switch domains if the headache comes."
            specific = "Track switch, not full stop. Different brain region, same output."

        return f"""— ACT 4: THE QUEST —

{quest}

Specifically: {specific}

The BEM has 18 proposals ready. Your gut approves in seconds. The wider pipe is open. Use it."""

    def _epilogue(self, timing: list) -> str:
        """The arc — the bigger story."""
        best_timed = timing[0] if timing else None
        project_name = best_timed["project"] if best_timed else "your highest-priority project"

        return f"""— THE ARC —

You are 21 years old. You have ADHD and dyslexia. You recovered from a brain injury by doing the hardest possible cognitive work every single day. You built a cognitive architecture with 16 mechanisms that a paper with 5 couldn't predict. You run 10 terminals simultaneously because that's how your brain works. You have 87 nodes of self-knowledge that compound while you sleep.

The people who said your brain was broken were measuring the wrong thing. They measured bandwidth. You measured intelligence. Now you have both.

The market is ready for {project_name}. The pipe is open. The graph is alive.

The only question is: what do you build next?

And your gut already knows the answer."""

    def _detect_energy(self) -> str:
        hour = datetime.now().hour
        if 6 <= hour < 11: return "mud"
        elif 11 <= hour < 13: return "ramp"
        elif 13 <= hour < 17: return "afternoon"
        elif 17 <= hour < 22: return "peak"
        elif 22 <= hour or hour < 2: return "deep_night"
        else: return "late"


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = NarrativeEngine(graph)

    print("=" * 60)
    print("NARRATIVE ENGINE — Level 16: Story Intelligence")
    print("The BEM's intelligence, compressed into feeling.")
    print("=" * 60)
    print()

    narrative = engine.generate_narrative()
    print(narrative)

    print()
    print("=" * 60)
    print("Mechanism 18: Narrative Compression.")
    print("Structure → feeling. Graph → story. Data → gut.")
    print("The ultimate bandwidth expansion: intelligence")
    print("translated into the format your brain actually reads.")
    print("=" * 60)


if __name__ == "__main__":
    demo()
