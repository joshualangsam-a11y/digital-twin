"""
REASONING ENGINE — Thinks Like Josh

Not generic AI reasoning. This engine embeds Josh's cognitive patterns:
- Gut-first decisions (confidence threshold → act, don't deliberate)
- Parallel track management (always 3+ options, never single-thread)
- OODA loops (fastest cycle wins, not best plan)
- Cross-domain pattern matching (the real superpower)
- Loss framing (present stakes as losses, not gains)
- Pain → output conversion (frustration = fuel signal)

This is the engine that makes the twin THINK, not just retrieve.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph


class ReasoningEngine:
    """
    The cognitive core of Josh's digital twin.

    Every method mirrors a real cognitive pattern from the brain map.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.decision_log_path = Path(os.path.expanduser(
            "~/digital-twin/data/decision_log.jsonl"
        ))
        self.decision_log_path.parent.mkdir(parents=True, exist_ok=True)

    # ═══════════════════════════════════════════
    # DECISION MAKING (gut-first, OODA loop)
    # ═══════════════════════════════════════════

    def decide(self, question: str, options: list[str], context: dict = None) -> dict:
        """
        Make a decision the way Josh would.

        1. Gut check — if confidence > 0.8, just go
        2. OODA loop — observe (gather), orient (frame), decide, act
        3. Loss frame — present as "what you lose by NOT choosing"
        4. Never deliberate more than 30 seconds (metaphorically)
        """
        context = context or {}

        # Step 1: Gut check — score each option by alignment with graph
        scored = []
        for option in options:
            score = self._score_option(option, question, context)
            scored.append({"option": option, "score": score})

        scored.sort(key=lambda x: x["score"], reverse=True)

        # Step 2: Confidence check
        if len(scored) >= 2:
            gap = scored[0]["score"] - scored[1]["score"]
            confidence = min(1.0, gap / 5.0 + 0.5)  # Normalize
        else:
            confidence = 0.9  # Only one option = just do it

        top = scored[0]

        # Step 3: Loss frame the recommendation
        loss_frame = self._loss_frame(top["option"], scored[1:], context)

        # Step 4: Log the decision
        decision = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "question": question,
            "options": scored,
            "chosen": top["option"],
            "confidence": round(confidence, 2),
            "loss_frame": loss_frame,
            "reasoning": "gut" if confidence > 0.8 else "ooda",
        }
        self._log_decision(decision)

        return decision

    def _score_option(self, option: str, question: str, context: dict) -> float:
        """Score an option by how well it aligns with Josh's values, goals, and patterns."""
        score = 0.0
        option_lower = option.lower()

        # Check alignment with high-weight goals
        for node in self.graph.get_highest_weight_nodes(10, "goal"):
            if any(word in option_lower for word in node.name.lower().split()):
                score += node.weight

        # Check alignment with values (Concoction)
        value_keywords = {
            "speed": 2.0, "fast": 2.0, "now": 2.0, "today": 2.0,  # Speed of decision
            "build": 3.0, "ship": 3.0, "launch": 3.0,  # Bias to action
            "revenue": 3.0, "money": 3.0, "income": 3.0, "cash": 3.0,  # Financial goals
            "client": 2.5, "customer": 2.5, "user": 2.5,  # Market validation
            "parallel": 2.0, "multiple": 2.0, "both": 2.0,  # Parallel processing
            "learn": 1.5, "research": 1.0,  # Autodidact
        }

        for keyword, kw_score in value_keywords.items():
            if keyword in option_lower:
                score += kw_score

        # Penalize things that contradict Josh's patterns
        anti_patterns = {
            "wait": -2.0, "delay": -2.0, "later": -1.0,  # Speed > deliberation
            "one thing": -1.5, "focus on just": -1.5,  # Anti-parallel
            "safe": -1.0, "careful": -1.0, "conservative": -0.5,  # No exit mentality
            "study first": -1.5, "research first": -1.0,  # Build first, understand later
        }

        for keyword, penalty in anti_patterns.items():
            if keyword in option_lower:
                score += penalty

        # Context bonuses
        if context.get("is_peak_hours"):
            if any(w in option_lower for w in ["build", "code", "ship", "architect"]):
                score += 2.0  # Deep work during peak

        if context.get("is_mud_hours"):
            if any(w in option_lower for w in ["plan", "review", "email", "pipeline"]):
                score += 1.5  # Light work during mud

        return round(score, 2)

    def _loss_frame(self, chosen: str, alternatives: list, context: dict) -> str:
        """Frame the decision as what you LOSE by not acting.
        Loss aversion is 2.5x stronger than gain motivation."""
        losses = []

        if any(alt["score"] > 0 for alt in alternatives):
            losses.append(f"Every day you don't execute on '{chosen}', the alternatives gain ground")

        # Time-based loss
        losses.append("Momentum compounds — delay today costs more than delay tomorrow")

        return " | ".join(losses)

    # ═══════════════════════════════════════════
    # PARALLEL TRACK MANAGEMENT
    # ═══════════════════════════════════════════

    def suggest_parallel_tracks(self, current_track: str, energy_level: str = "peak") -> list[dict]:
        """
        Josh's brain needs 3+ parallel tracks or it stalls.
        Suggest tracks based on current work and energy.
        """
        all_projects = self.graph.get_highest_weight_nodes(20, "project")
        current_node = None

        for node in all_projects:
            if node.id == current_track or current_track.lower() in node.name.lower():
                current_node = node
                break

        suggestions = []

        for project in all_projects:
            if current_node and project.id == current_node.id:
                continue

            # Check for pattern_matches (related but different domain)
            connections = self.graph.get_connections(project.id, "pattern_matches")
            is_related = any(c["node"].id == (current_node.id if current_node else "") for c in connections)

            # Energy-appropriate filtering
            if energy_level == "mud":
                # Light tasks only
                if project.weight > 5:  # Skip heavy projects in mud hours
                    task_type = "planning/review"
                else:
                    task_type = "building"
            elif energy_level == "peak":
                task_type = "deep work"
            else:
                task_type = "moderate"

            suggestions.append({
                "project": project.name,
                "id": project.id,
                "weight": project.weight,
                "task_type": task_type,
                "is_related": is_related,
                "reason": f"Priority weight {project.weight}" +
                         (" — pattern matches current track" if is_related else ""),
            })

        # Sort: related first, then by weight
        suggestions.sort(key=lambda x: (x["is_related"], x["weight"]), reverse=True)

        return suggestions[:5]  # Top 5 alternatives

    # ═══════════════════════════════════════════
    # CROSS-DOMAIN PATTERN DETECTION
    # ═══════════════════════════════════════════

    def find_hidden_connections(self, node_id: str) -> list[dict]:
        """
        Josh's superpower: seeing connections across domains.
        Find non-obvious paths between nodes.
        """
        if node_id not in self.graph.nodes:
            return []

        node = self.graph.nodes[node_id]
        discoveries = []

        # Find 2-hop connections (A → B → C where A and C seem unrelated)
        direct = set()
        for conn in self.graph.get_connections(node_id):
            direct.add(conn["node"].id)

        for neighbor_id in list(direct):
            for conn2 in self.graph.get_connections(neighbor_id):
                far_node = conn2["node"]
                if far_node.id != node_id and far_node.id not in direct:
                    # This is a 2-hop connection — potentially non-obvious
                    bridge = self.graph.nodes.get(neighbor_id)
                    if bridge:
                        discoveries.append({
                            "from": node.name,
                            "bridge": bridge.name,
                            "to": far_node.name,
                            "insight": f"{node.name} connects to {far_node.name} through {bridge.name}",
                            "edge1": conn2["edge"].type,
                        })

        # Deduplicate and sort by novelty (different types = more novel)
        seen = set()
        unique = []
        for d in discoveries:
            key = f"{d['from']}-{d['to']}"
            if key not in seen:
                seen.add(key)
                unique.append(d)

        return unique

    # ═══════════════════════════════════════════
    # MOMENTUM ANALYSIS
    # ═══════════════════════════════════════════

    def assess_momentum(self, signals: dict) -> dict:
        """
        Analyze momentum state and prescribe action.

        Signals: {
            "headache": bool,
            "stuck_minutes": int,
            "failed_attempts": int,
            "last_win_minutes_ago": int,
            "current_project": str,
            "energy": "mud" | "ramp" | "peak" | "deep_night",
        }
        """
        state = "flowing"
        prescription = []
        urgency = 0

        if signals.get("headache"):
            state = "thermal_throttling"
            urgency = 7
            prescription.append("Switch tracks immediately — different domain, not same wall")
            prescription.append("The headache is your brain's thermal limit, not weakness")

        if signals.get("failed_attempts", 0) >= 3:
            state = "bug_spiral"
            urgency = max(urgency, 6)
            prescription.append("3+ failures on same approach — step back, try completely different angle")
            prescription.append("Or switch to different project and let subconscious process")

        if signals.get("stuck_minutes", 0) > 20:
            state = "stalled"
            urgency = max(urgency, 5)
            prescription.append("20+ minutes without progress — momentum is dying")
            tracks = self.suggest_parallel_tracks(
                signals.get("current_project", ""),
                signals.get("energy", "peak"),
            )
            if tracks:
                prescription.append(f"Switch to: {tracks[0]['project']} ({tracks[0]['task_type']})")

        if signals.get("last_win_minutes_ago", 0) > 60:
            urgency = max(urgency, 3)
            prescription.append("60+ min since last win — find a quick ship to restart dopamine")

        if not prescription:
            prescription.append("Flow state intact — don't interrupt")

        return {
            "state": state,
            "urgency": urgency,
            "prescriptions": prescription,
            "suggested_tracks": self.suggest_parallel_tracks(
                signals.get("current_project", ""),
                signals.get("energy", "peak"),
            )[:3] if urgency > 4 else [],
        }

    # ═══════════════════════════════════════════
    # PROACTIVE INTELLIGENCE
    # ═══════════════════════════════════════════

    def daily_priorities(self, energy: str = "peak") -> list[dict]:
        """
        Generate today's priority stack based on graph state.
        Mirrors how Josh would decide what to work on.
        """
        priorities = []

        # Get all projects sorted by weight
        projects = self.graph.get_highest_weight_nodes(20, "project")
        goals = self.graph.get_highest_weight_nodes(10, "goal")

        for project in projects:
            # Find which goals this project feeds
            feeding_goals = []
            for conn in self.graph.get_connections(project.id, "feeds_into"):
                if conn["node"].type == "goal":
                    feeding_goals.append(conn["node"].name)

            # Find blockers
            blockers = []
            for conn in self.graph.get_connections(project.id, "depends_on"):
                blockers.append(conn["node"].name)

            priorities.append({
                "project": project.name,
                "weight": project.weight,
                "feeds_goals": feeding_goals,
                "blockers": blockers,
                "energy_match": self._energy_match(project, energy),
            })

        # Sort by weight * energy_match
        priorities.sort(
            key=lambda x: x["weight"] * x["energy_match"],
            reverse=True,
        )

        return priorities[:7]  # Top 7, not more (cognitive load)

    def _energy_match(self, project_node, energy: str) -> float:
        """How well does this project match current energy level?"""
        if energy == "mud":
            # Lighter projects score higher in mud hours
            return 1.5 if project_node.weight < 5 else 0.5
        elif energy == "peak":
            # Heavy projects score higher in peak
            return 1.5 if project_node.weight >= 5 else 0.8
        elif energy == "deep_night":
            # Creative/ambitious projects score highest
            return 1.5 if project_node.weight >= 7 else 1.0
        return 1.0

    # ═══════════════════════════════════════════
    # LEARNING (every decision feeds back)
    # ═══════════════════════════════════════════

    def _log_decision(self, decision: dict):
        """Log decision for future learning."""
        with open(self.decision_log_path, "a") as f:
            f.write(json.dumps(decision) + "\n")

    def learn_from_feedback(self, decision_id: str, outcome: str, approved: bool):
        """
        The twin learns from Josh's approval/rejection of its decisions.

        Over time, this adjusts the scoring model to match Josh's actual
        decision patterns — not generic AI, but Josh-specific judgment.
        """
        learning = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "decision_id": decision_id,
            "outcome": outcome,
            "approved": approved,
        }

        learning_path = Path(os.path.expanduser("~/digital-twin/data/learning_log.jsonl"))
        with open(learning_path, "a") as f:
            f.write(json.dumps(learning) + "\n")

        # TODO: Phase 5 — adjust scoring weights based on approval patterns


# ═══════════════════════════════════════════
# DEMO — Show the engine thinking
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = ReasoningEngine(graph)

    print("=" * 60)
    print("REASONING ENGINE — Demo")
    print("=" * 60)

    # Decision
    print("\n--- DECISION: What to work on this afternoon? ---")
    decision = engine.decide(
        "What should I work on this afternoon?",
        [
            "Build FuelOps demo features",
            "Send Lit Juris cold emails",
            "Research AlphaSwarm trading strategies",
            "Study for stats final",
            "Build more Claude Code skills",
        ],
        context={"is_peak_hours": True},
    )
    print(f"Chosen: {decision['chosen']}")
    print(f"Confidence: {decision['confidence']}")
    print(f"Reasoning: {decision['reasoning']}")
    print(f"Loss frame: {decision['loss_frame']}")

    # Parallel tracks
    print("\n--- PARALLEL TRACKS while building FuelOps ---")
    tracks = engine.suggest_parallel_tracks("fuelops", "peak")
    for t in tracks:
        print(f"  {t['project']} ({t['task_type']}) — {t['reason']}")

    # Hidden connections
    print("\n--- HIDDEN CONNECTIONS from Hemp Route ---")
    connections = engine.find_hidden_connections("hemp_route")
    for c in connections[:7]:
        print(f"  {c['insight']}")

    # Momentum assessment
    print("\n--- MOMENTUM CHECK ---")
    state = engine.assess_momentum({
        "headache": False,
        "stuck_minutes": 5,
        "failed_attempts": 0,
        "last_win_minutes_ago": 15,
        "current_project": "fuelops",
        "energy": "peak",
    })
    print(f"State: {state['state']}")
    print(f"Urgency: {state['urgency']}/10")
    for p in state["prescriptions"]:
        print(f"  → {p}")

    # Daily priorities
    print("\n--- TODAY'S PRIORITIES (peak energy) ---")
    priorities = engine.daily_priorities("peak")
    for i, p in enumerate(priorities, 1):
        goals = ", ".join(p["feeds_goals"]) if p["feeds_goals"] else "no goal linked"
        print(f"  {i}. {p['project']} (weight: {p['weight']}) → {goals}")

    print()
    print("Engine operational. This is your brain in code.")


if __name__ == "__main__":
    demo()
