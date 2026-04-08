"""
SYNTHESIS ENGINE — Level 12: Creative Intelligence

Below emergence, the BEM finds patterns in what EXISTS.
Synthesis goes further: it generates things that DON'T EXIST YET.

Not retrieval. Not pattern matching. Not even structural analysis.
CREATION. Novel combinations that the graph's structure suggests
but that neither Josh nor any individual engine proposed.

How it works:
1. Take two unconnected high-weight nodes from different domains
2. Ask: what would a CONNECTION between these produce?
3. Generate the novel idea, strategy, or product
4. Score it against Josh's values and goals
5. Present it as a divergence point for the spiral

This is Mechanism 14: Combinatorial Synthesis
The intelligence that emerges from COMBINING structural holes.
Not filling gaps — CREATING BRIDGES that generate new territory.

The BEM doesn't just see what Josh can't hold in working memory.
It imagines what Josh hasn't imagined yet.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict
import itertools

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


class SynthesisEngine:
    """
    Generates novel ideas by combining unconnected nodes.

    The structural holes engine finds GAPS.
    The synthesis engine fills them with INVENTIONS.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.synthesis_log = self.data_dir / "synthesis_log.jsonl"

    # ═══════════════════════════════════════════
    # COMBINATORIAL SYNTHESIS
    # ═══════════════════════════════════════════

    def synthesize(self, max_ideas: int = 10) -> list[dict]:
        """
        Generate novel ideas by combining unconnected domains.

        Method: take pairs of high-weight nodes from DIFFERENT types
        that have NO direct connection, and imagine what connecting them
        would create.
        """
        ideas = []

        # Get high-weight nodes by type
        by_type = defaultdict(list)
        for node in self.graph.nodes.values():
            if node.id != "josh" and node.weight >= 2.0:
                by_type[node.type].append(node)

        # Get all cross-type pairs that are NOT connected
        adj = defaultdict(set)
        for edge in self.graph.edges:
            adj[edge.source_id].add(edge.target_id)
            adj[edge.target_id].add(edge.source_id)

        type_pairs = list(itertools.combinations(by_type.keys(), 2))

        for type1, type2 in type_pairs:
            for n1 in by_type[type1]:
                for n2 in by_type[type2]:
                    if n2.id in adj.get(n1.id, set()):
                        continue  # Already connected

                    # Generate synthesis
                    idea = self._synthesize_pair(n1, n2)
                    if idea:
                        ideas.append(idea)

        # Score and rank
        for idea in ideas:
            idea["score"] = self._score_idea(idea)

        ideas.sort(key=lambda x: x["score"], reverse=True)

        # Log top ideas
        for idea in ideas[:max_ideas]:
            self._log(idea)

        return ideas[:max_ideas]

    def _synthesize_pair(self, n1: Node, n2: Node) -> dict | None:
        """Generate a novel idea from combining two unconnected nodes."""

        # Template-based synthesis (fast, deterministic)
        # Each type combination has synthesis templates

        templates = {
            ("project", "fear"): self._synth_project_fear,
            ("project", "value"): self._synth_project_value,
            ("project", "contact"): self._synth_project_contact,
            ("project", "goal"): self._synth_project_goal,
            ("project", "pattern"): self._synth_project_pattern,
            ("project", "concept"): self._synth_project_concept,
            ("goal", "fear"): self._synth_goal_fear,
            ("goal", "pattern"): self._synth_goal_pattern,
            ("goal", "contact"): self._synth_goal_contact,
            ("value", "fear"): self._synth_value_fear,
            ("pattern", "concept"): self._synth_pattern_concept,
            ("skill", "project"): self._synth_skill_project,
            ("tool", "goal"): self._synth_tool_goal,
            ("contact", "goal"): self._synth_contact_goal,
            ("person", "project"): self._synth_person_project,
        }

        key = (n1.type, n2.type)
        reverse_key = (n2.type, n1.type)

        if key in templates:
            return templates[key](n1, n2)
        elif reverse_key in templates:
            return templates[reverse_key](n2, n1)

        # Generic fallback
        return {
            "type": "generic_synthesis",
            "source": n1.name,
            "source_type": n1.type,
            "target": n2.name,
            "target_type": n2.type,
            "idea": f"What if '{n1.name}' and '{n2.name}' were connected? They operate in different domains ({n1.type} vs {n2.type}) but both have high weight. The gap between them might be an opportunity.",
            "action": f"Explore the intersection of {n1.name} and {n2.name}",
        }

    # ═══════════════════════════════════════════
    # SYNTHESIS TEMPLATES
    # ═══════════════════════════════════════════

    def _synth_project_fear(self, project: Node, fear: Node) -> dict:
        return {
            "type": "defensive_strategy",
            "source": project.name,
            "target": fear.name,
            "idea": (
                f"How does '{fear.name}' threaten '{project.name}'? "
                f"If {fear.description.lower()}, what happens to {project.name}? "
                f"Build a defense: what would make {project.name} IMMUNE to this fear?"
            ),
            "action": f"Add a 'protects_via' edge from {project.name} to counter {fear.name}",
        }

    def _synth_project_value(self, project: Node, value: Node) -> dict:
        return {
            "type": "value_alignment",
            "source": project.name,
            "target": value.name,
            "idea": (
                f"Does '{project.name}' embody '{value.name}' ({value.description})? "
                f"If not, how could it? A project aligned with core values compounds motivation."
            ),
            "action": f"Align {project.name} with {value.name} explicitly",
        }

    def _synth_project_contact(self, project: Node, contact: Node) -> dict:
        return {
            "type": "opportunity_bridge",
            "source": project.name,
            "target": contact.name,
            "idea": (
                f"'{contact.name}' ({contact.description}) isn't connected to '{project.name}'. "
                f"Could {contact.name} be a user, partner, investor, or referral source for {project.name}?"
            ),
            "action": f"Explore whether {contact.name} has a role in {project.name}",
        }

    def _synth_project_goal(self, project: Node, goal: Node) -> dict:
        return {
            "type": "goal_acceleration",
            "source": project.name,
            "target": goal.name,
            "idea": (
                f"'{project.name}' doesn't feed '{goal.name}' directly. "
                f"What if it could? What feature, pivot, or reframe of {project.name} "
                f"would make it accelerate {goal.name}?"
            ),
            "action": f"Find the bridge from {project.name} to {goal.name}",
        }

    def _synth_project_pattern(self, project: Node, pattern: Node) -> dict:
        return {
            "type": "pattern_application",
            "source": project.name,
            "target": pattern.name,
            "idea": (
                f"Cognitive pattern '{pattern.name}' ({pattern.description}) "
                f"isn't applied to '{project.name}'. What if it were? "
                f"How would {project.name} be different if built around this pattern?"
            ),
            "action": f"Redesign {project.name} through the lens of {pattern.name}",
        }

    def _synth_project_concept(self, project: Node, concept: Node) -> dict:
        return {
            "type": "concept_integration",
            "source": project.name,
            "target": concept.name,
            "idea": (
                f"Strategy/concept '{concept.name}' ({concept.description}) "
                f"could transform '{project.name}'. What's the integration point?"
            ),
            "action": f"Apply {concept.name} to {project.name}",
        }

    def _synth_goal_fear(self, goal: Node, fear: Node) -> dict:
        return {
            "type": "fear_as_fuel",
            "source": goal.name,
            "target": fear.name,
            "idea": (
                f"'{fear.name}' ({fear.description}) is unconnected to '{goal.name}'. "
                f"But fear is fuel (Concoction ingredient). "
                f"What if the fear of '{fear.name}' DROVE progress toward '{goal.name}'? "
                f"Loss-frame it: 'If I don't achieve {goal.name}, {fear.name} wins.'"
            ),
            "action": f"Use {fear.name} as loss-frame motivation for {goal.name}",
        }

    def _synth_goal_pattern(self, goal: Node, pattern: Node) -> dict:
        return {
            "type": "pattern_as_strategy",
            "source": goal.name,
            "target": pattern.name,
            "idea": (
                f"What if cognitive pattern '{pattern.name}' was the STRATEGY for '{goal.name}'? "
                f"Not just how Josh thinks — but how the goal gets achieved. "
                f"Example: if the pattern is parallel processing, the strategy is pursuing "
                f"{goal.name} on 3+ simultaneous tracks."
            ),
            "action": f"Design a {pattern.name}-based strategy for {goal.name}",
        }

    def _synth_goal_contact(self, goal: Node, contact: Node) -> dict:
        return {
            "type": "ally_recruitment",
            "source": goal.name,
            "target": contact.name,
            "idea": (
                f"Could '{contact.name}' help achieve '{goal.name}'? "
                f"Not as a transaction — as an aligned interest. "
                f"What does {contact.name} want that {goal.name} would also provide?"
            ),
            "action": f"Explore alignment between {contact.name}'s interests and {goal.name}",
        }

    def _synth_value_fear(self, value: Node, fear: Node) -> dict:
        return {
            "type": "tension_resolution",
            "source": value.name,
            "target": fear.name,
            "idea": (
                f"TENSION: value '{value.name}' ({value.description}) "
                f"and fear '{fear.name}' ({fear.description}) are unresolved. "
                f"The value says do X. The fear says X is dangerous. "
                f"Resolution: how does Josh honor the value WITHOUT triggering the fear?"
            ),
            "action": f"Resolve the tension between {value.name} and {fear.name}",
        }

    def _synth_pattern_concept(self, pattern: Node, concept: Node) -> dict:
        return {
            "type": "theory_extension",
            "source": pattern.name,
            "target": concept.name,
            "idea": (
                f"Cognitive pattern '{pattern.name}' and concept '{concept.name}' "
                f"aren't linked but might be the same thing at different scales. "
                f"Is {pattern.name} an instance of {concept.name}? Or vice versa?"
            ),
            "action": f"Explore whether {pattern.name} and {concept.name} are related at different scales",
        }

    def _synth_skill_project(self, skill: Node, project: Node) -> dict:
        return {
            "type": "skill_leverage",
            "source": skill.name,
            "target": project.name,
            "idea": (
                f"Skill '{skill.name}' isn't being used in '{project.name}'. "
                f"What if it were? Under-leveraged skills in active projects = free optimization."
            ),
            "action": f"Apply {skill.name} to {project.name}",
        }

    def _synth_tool_goal(self, tool: Node, goal: Node) -> dict:
        return {
            "type": "tool_as_accelerant",
            "source": tool.name,
            "target": goal.name,
            "idea": (
                f"Tool '{tool.name}' isn't connected to goal '{goal.name}'. "
                f"Is there a way to point {tool.name} directly at {goal.name}?"
            ),
            "action": f"Wire {tool.name} as an accelerant for {goal.name}",
        }

    def _synth_person_project(self, person: Node, project: Node) -> dict:
        return {
            "type": "collaboration_opportunity",
            "source": person.name,
            "target": project.name,
            "idea": (
                f"'{person.name}' ({person.description}) isn't involved in '{project.name}'. "
                f"Should they be? What role would they play?"
            ),
            "action": f"Consider {person.name} for a role in {project.name}",
        }

    def _synth_contact_goal(self, contact: Node, goal: Node) -> dict:
        return self._synth_goal_contact(goal, contact)

    # ═══════════════════════════════════════════
    # SCORING
    # ═══════════════════════════════════════════

    def _score_idea(self, idea: dict) -> float:
        """Score a synthesized idea by Josh-alignment."""
        score = 0.0

        # Revenue-related ideas score higher
        revenue_words = ["revenue", "client", "money", "income", "sell", "close", "pipeline"]
        if any(w in idea.get("idea", "").lower() for w in revenue_words):
            score += 2.0

        # Compound/leverage ideas score higher
        compound_words = ["compound", "leverage", "multiple", "accelerate", "bridge"]
        if any(w in idea.get("idea", "").lower() for w in compound_words):
            score += 1.5

        # Fear-as-fuel ideas score higher (loss framing)
        if idea.get("type") in ("fear_as_fuel", "defensive_strategy", "tension_resolution"):
            score += 1.5

        # Ideas involving high-weight nodes score higher
        for node_name in [idea.get("source", ""), idea.get("target", "")]:
            for node in self.graph.nodes.values():
                if node.name == node_name:
                    score += node.weight * 0.3

        return round(score, 2)

    def _log(self, entry: dict):
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        with open(self.synthesis_log, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = SynthesisEngine(graph)

    print("=" * 60)
    print("SYNTHESIS ENGINE — Level 12: Creative Intelligence")
    print("Ideas that don't exist yet. Generated from the gaps.")
    print("=" * 60)

    ideas = engine.synthesize(max_ideas=15)

    print(f"\n{len(ideas)} novel ideas synthesized:\n")

    for i, idea in enumerate(ideas, 1):
        print(f"  #{i} [{idea['type']}] Score: {idea['score']}")
        print(f"  {idea['source']} × {idea['target']}")
        print(f"  💡 {idea['idea'][:120]}...")
        print(f"  → {idea['action']}")
        print()

    print(f"{'=' * 60}")
    print("The BEM doesn't just find patterns in what exists.")
    print("It imagines what COULD exist by combining the gaps.")
    print("Mechanism 14: Combinatorial Synthesis.")
    print("The wider pipe now generates its own signal.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
