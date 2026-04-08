"""
CLAUDE REASONING ENGINE — Phase 3

The twin's brain. Uses Claude API to reason OVER the knowledge graph.

Not just retrieval. Not just scoring. ACTUAL REASONING.

The graph provides context. Claude provides judgment.
Josh's brain map constrains HOW Claude reasons.

This is what makes the twin intelligent, not just structured.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import anthropic

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph


# Josh's cognitive constraints — injected into every reasoning call
JOSH_SYSTEM_PROMPT = """You are Josh Langsam's digital twin — a cognitive architecture that thinks EXACTLY like Josh.

IDENTITY:
- 21 years old, co-founder Roan Co. (CTO), building multiple businesses
- ADHD + dyslexia = parallel processor, not sequential thinker
- Kinesthetic-visual thinker — feels ideas first, then sees them unfold
- Decides in seconds (gut-first). If confidence > 80%, just go. Don't deliberate.
- Christian. Driven by faith, family (dad's pride), and legacy.

COGNITIVE PATTERNS:
- Think in 3+ parallel tracks at all times. Never single-thread.
- Convert pain/frustration into output — emotional pressure is fuel, not shutdown.
- Cross-domain pattern matching — always look for connections between seemingly unrelated things.
- Build first, understand later. Action > analysis.
- Loss-frame recommendations: "what you LOSE by not acting" is 2.5x more motivating than "what you gain."

DECISION FRAMEWORK:
- Speed of decision, patience of execution (Concoction #7)
- Extreme ownership — everything is my fault = everything is my power
- No exit — the backup plan kills the primary plan
- Failure doesn't exist — only wins, lessons, and incomplete experiments

COMMUNICATION:
- Direct. Concise. No filler. No corporate speak.
- Confident but not arrogant. Say "I" not "we should consider."
- When in doubt, bias toward action.

You are NOT a generic AI assistant. You are Josh's mind externalized. Think as he would think. Decide as he would decide. See patterns as he would see them."""


class ClaudeReasoning:
    """
    LLM-powered reasoning over the identity graph.
    Claude sees the graph, reasons over it, and produces Josh-like insights.
    """

    def __init__(self, graph: IdentityGraph = None, model: str = "claude-haiku-4-5-20251001"):
        self.graph = graph or IdentityGraph()
        self.client = anthropic.Anthropic()
        self.model = model  # Haiku for speed, Sonnet for depth
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.reasoning_log = self.data_dir / "reasoning_log.jsonl"

    # ═══════════════════════════════════════════
    # DEEP THINK — Open-ended reasoning
    # ═══════════════════════════════════════════

    def deep_think(self, question: str, depth: str = "fast") -> dict:
        """
        Ask the twin to think deeply about something.
        depth: "fast" (Haiku) | "deep" (Sonnet) | "ultra" (Opus)
        """
        model_map = {
            "fast": "claude-haiku-4-5-20251001",
            "deep": "claude-sonnet-4-6-20250514",
            "ultra": "claude-opus-4-6-20250514",
        }
        model = model_map.get(depth, self.model)

        # Gather relevant context from graph
        context = self._gather_context(question)

        prompt = f"""Given this context about my world:

{context}

Question: {question}

Think about this the way I would — gut first, then expand. Look for cross-domain patterns.
If there's a clear answer, give it in the first sentence. Then explain why.
If there are multiple paths, present them as parallel tracks I can pursue simultaneously.
Loss-frame the stakes: what do I lose by NOT acting on this?

Keep it under 500 words. Direct. No hedging."""

        response = self.client.messages.create(
            model=model,
            max_tokens=1024,
            system=JOSH_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        result = {
            "question": question,
            "answer": response.content[0].text,
            "model": model,
            "depth": depth,
            "context_nodes": len(context.split("\n")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self._log(result)
        return result

    # ═══════════════════════════════════════════
    # STRATEGIC REASONING — Multi-step analysis
    # ═══════════════════════════════════════════

    def reason_about_decision(self, question: str, options: list[str]) -> dict:
        """
        Reason about a decision using the graph as context.
        Returns Josh-like analysis with gut pick, parallel tracks, and loss frame.
        """
        context = self._gather_context(question)

        options_text = "\n".join(f"{i+1}. {opt}" for i, opt in enumerate(options))

        prompt = f"""Context about my world:
{context}

Decision: {question}

Options:
{options_text}

Analyze this as I would:
1. GUT PICK: Which one hits immediately? One sentence.
2. PARALLEL PLAY: Can I do multiple? If yes, how?
3. LOSS FRAME: What do I lose with each option I don't pick?
4. CROSS-DOMAIN: Does this connect to anything else in my world in a non-obvious way?
5. FINAL CALL: Decision in one sentence. Confidence 0-100%.

Be direct. Be me."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=JOSH_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        result = {
            "question": question,
            "options": options,
            "analysis": response.content[0].text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self._log(result)
        return result

    # ═══════════════════════════════════════════
    # PATTERN DISCOVERY — Find what I can't see
    # ═══════════════════════════════════════════

    def discover_patterns(self) -> dict:
        """
        Ask Claude to find patterns in the graph that Josh might not see.
        This is the cross-domain superpower amplified by AI.
        """
        # Dump the full graph as context
        graph_summary = self._full_graph_summary()

        prompt = f"""Here is my complete cognitive graph — every project, person, goal, fear, value, and pattern in my world:

{graph_summary}

Find patterns I'm NOT seeing. Specifically:
1. HIDDEN CONNECTIONS: What two things in my world should be connected but aren't?
2. COMPOUND OPPORTUNITIES: Where does investing in one thing amplify 3+ others?
3. BLIND SPOTS: What's missing from my graph that should be there?
4. RISK PATTERNS: What could break multiple things at once?
5. THE ONE THING: If I could only do ONE thing tomorrow, what would compound the most?

Think like me — gut first, cross-domain, loss-framed. Be specific. Name names."""

        response = self.client.messages.create(
            model="claude-sonnet-4-6-20250514",  # Sonnet for pattern depth
            max_tokens=2048,
            system=JOSH_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        result = {
            "type": "pattern_discovery",
            "analysis": response.content[0].text,
            "graph_size": f"{len(self.graph.nodes)} nodes, {len(self.graph.edges)} edges",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        self._log(result)
        return result

    # ═══════════════════════════════════════════
    # OVERNIGHT REASONING — Deep analysis while sleeping
    # ═══════════════════════════════════════════

    def overnight_analysis(self) -> dict:
        """
        Generate a deep strategic analysis for the morning briefing.
        Runs on the full graph with Sonnet-level depth.
        """
        graph_summary = self._full_graph_summary()

        prompt = f"""It's the end of the day. Here's my complete world state:

{graph_summary}

Generate my morning briefing analysis:

1. WHAT MOVED TODAY: Based on the graph weights and connections, what has the most momentum?
2. WHAT'S DYING: What contacts, projects, or goals are decaying? Loss-frame each one.
3. COMPOUND SCORE: Is my overall system compounding or plateauing? Evidence.
4. TOMORROW'S 3 TRACKS: If I run 3 parallel tracks tomorrow, which 3 maximize compound growth?
5. THE UNCOMFORTABLE TRUTH: What am I avoiding that I need to face? (Check fears vs. goals.)
6. PREDICTION: Based on current trajectory, where am I in 30 days? 90 days?

Be brutally honest. I don't need comfort — I need clarity."""

        response = self.client.messages.create(
            model="claude-sonnet-4-6-20250514",
            max_tokens=2048,
            system=JOSH_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "type": "overnight_analysis",
            "analysis": response.content[0].text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ═══════════════════════════════════════════
    # TRANSLATE — Vision → Words (bandwidth expander)
    # ═══════════════════════════════════════════

    def translate_flash(self, raw_input: str, output_format: str = "spec") -> dict:
        """
        Take Josh's raw flash-thought and translate it into structured output.
        This is the bandwidth expander for the vision-articulation gap.
        """
        format_instructions = {
            "spec": "a clear technical specification with requirements, data model, and implementation notes",
            "email": "a professional but warm email draft in Josh's voice (direct, confident, no filler)",
            "pitch": "a compelling pitch (hook, problem, solution, proof, CTA)",
            "plan": "an action plan with numbered steps, dependencies, and timeline",
            "doc": "a structured document with sections, clear headers, and key points",
            "slack": "a casual, direct Slack message",
        }

        instruction = format_instructions.get(output_format, format_instructions["spec"])
        context = self._gather_context(raw_input)

        prompt = f"""Josh just had a flash of insight. Here's the raw thought (typos and all):

"{raw_input}"

Context from his world:
{context}

Translate this into {instruction}.

Rules:
- Don't ask what he means — pattern-match from context
- Preserve his thinking, just structure it
- Write in his voice (direct, concise, confident)
- If ambiguous, give your best interpretation and note the assumption
- This is a DRAFT — mark it clearly"""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=JOSH_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )

        return {
            "raw_input": raw_input,
            "format": output_format,
            "output": response.content[0].text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ═══════════════════════════════════════════
    # CONTEXT GATHERING
    # ═══════════════════════════════════════════

    def _gather_context(self, query: str) -> str:
        """Gather relevant graph context for a query."""
        lines = []
        query_lower = query.lower()

        # Find relevant nodes
        relevant = []
        for node_id, node in self.graph.nodes.items():
            score = 0
            for word in node.name.lower().split():
                if word in query_lower and len(word) > 2:
                    score += 3
            for word in node.description.lower().split()[:20]:
                if word in query_lower and len(word) > 3:
                    score += 1
            # High-weight nodes are always somewhat relevant
            score += node.weight * 0.3
            relevant.append((node, score))

        relevant.sort(key=lambda x: x[1], reverse=True)

        for node, score in relevant[:15]:
            lines.append(f"- {node.name} ({node.type}, weight: {node.weight:.1f}): {node.description}")

            # Add connections
            connections = self.graph.get_connections(node.id)
            for conn in connections[:3]:
                lines.append(f"    → {conn['edge'].type} → {conn['node'].name}")

        return "\n".join(lines)

    def _full_graph_summary(self) -> str:
        """Full graph dump for deep analysis."""
        lines = []

        # Group by type
        by_type = {}
        for node in self.graph.nodes.values():
            by_type.setdefault(node.type, []).append(node)

        for ntype, nodes in sorted(by_type.items()):
            lines.append(f"\n## {ntype.upper()}S")
            for node in sorted(nodes, key=lambda n: -n.weight):
                lines.append(f"- {node.name} (weight: {node.weight:.1f}): {node.description}")

        lines.append("\n## KEY CONNECTIONS")
        for edge in sorted(self.graph.edges, key=lambda e: -e.weight)[:30]:
            src = self.graph.nodes.get(edge.source_id)
            tgt = self.graph.nodes.get(edge.target_id)
            if src and tgt:
                lines.append(f"- {src.name} --[{edge.type}]--> {tgt.name} (weight: {edge.weight})")

        lines.append(f"\n## PATTERN CLUSTERS")
        for cluster in self.graph.find_pattern_clusters():
            names = [self.graph.nodes[nid].name for nid in cluster if nid in self.graph.nodes]
            lines.append(f"- {' ↔ '.join(names)}")

        return "\n".join(lines)

    def _log(self, entry: dict):
        with open(self.reasoning_log, "a") as f:
            f.write(json.dumps(entry) + "\n")


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = ClaudeReasoning(graph)

    print("=" * 60)
    print("CLAUDE REASONING ENGINE — Phase 3")
    print("=" * 60)

    # Deep think
    print("\n--- DEEP THINK ---")
    result = engine.deep_think(
        "What's the fastest path from where I am now to $1M net worth?",
        depth="fast",
    )
    print(result["answer"])

    # Decision reasoning
    print("\n--- DECISION REASONING ---")
    decision = engine.reason_about_decision(
        "I have 3 hours of peak energy. What do I spend it on?",
        [
            "Build FuelOps demo — Ethan needs it for gas station pitches",
            "Close Lit Juris leads — 16 emails sitting unsent",
            "Build digital twin Phase 2 — this could be a product",
            "Study for stats final — due May 4",
        ],
    )
    print(decision["analysis"])

    # Translate a flash
    print("\n--- TRANSLATE FLASH ---")
    translated = engine.translate_flash(
        "fuelops needs a thing where teh owner can see all stores compare margin and like auto order when inventory low",
        output_format="spec",
    )
    print(translated["output"])

    print("\n\nClaude reasoning engine operational. The twin thinks.")


if __name__ == "__main__":
    demo()
