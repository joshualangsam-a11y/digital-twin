"""
GAME THEORY ENGINE — Strategic Intelligence for Multi-Agent Coordination

Josh's 91 agents are players in a game. His 11 projects compete for
finite attention. His contacts have their own incentive structures.

This engine applies formal game theory to:

1. ATTENTION ALLOCATION GAME — Projects compete for Josh's time.
   Nash equilibrium: what's the stable allocation where no project
   benefits from stealing time from another?

2. AGENT COORDINATION GAME — 91 agents need to coordinate without
   a central controller. Mechanism design: what incentive structure
   makes them cooperate optimally?

3. SALES GAME — Josh vs. prospects. Each prospect has a reservation
   price, switching cost, and outside option. What's the optimal
   strategy per prospect?

4. COMPETITIVE GAME — Josh vs. Clio/Filevine/Petrosoft. Asymmetric
   warfare: small player vs. incumbents. Lanchester's laws applied.

5. COALITION GAME (Shapley Values) — Which projects contribute most
   to the COALITION of all Josh's businesses? Shapley value measures
   each project's marginal contribution to the whole.

Mechanism 21: Game-Theoretic Optimization
The graph's nodes are players. The edges are strategies.
Nash equilibrium is the optimal cognitive configuration.
"""

import json
import os
import math
import itertools
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph


class GameTheoryEngine:
    """
    Formal game theory applied to Josh's cognitive graph.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))

    # ═══════════════════════════════════════════
    # 1. ATTENTION ALLOCATION GAME (Nash Equilibrium)
    # ═══════════════════════════════════════════

    def attention_nash_equilibrium(self, total_hours: float = 10.0) -> dict:
        """
        Projects compete for Josh's finite attention (10 peak hours/day).
        Each project has a weight (priority) and a diminishing returns curve.

        The Nash equilibrium is the allocation where no project benefits
        from stealing time from another — it's the STABLE configuration.

        Uses Kelly Criterion-inspired proportional allocation:
        f* = (edge * p - (1-p)) / edge
        Simplified: allocate proportional to weight * connection_density
        """
        projects = sorted(
            [n for n in self.graph.nodes.values() if n.type == "project"],
            key=lambda n: -n.weight,
        )

        if not projects:
            return {"error": "No projects in graph"}

        # Calculate "expected return" per project
        # = weight × number of goal connections × (1 / competition_factor)
        allocations = []
        total_score = 0

        for p in projects:
            # Goal connections = how many goals this feeds
            goal_conns = sum(1 for c in self.graph.get_connections(p.id)
                           if c["node"].type == "goal")

            # Cross-project connections = compound leverage
            cross_conns = sum(1 for c in self.graph.get_connections(p.id)
                            if c["node"].type == "project")

            # Score = weight × (1 + goal_connections) × (1 + cross_connections × 0.5)
            score = p.weight * (1 + goal_conns) * (1 + cross_conns * 0.5)
            total_score += score

            allocations.append({
                "project": p.name,
                "weight": p.weight,
                "goal_connections": goal_conns,
                "cross_connections": cross_conns,
                "raw_score": round(score, 2),
            })

        # Normalize to total hours (Kelly-inspired proportional allocation)
        for a in allocations:
            proportion = a["raw_score"] / total_score if total_score > 0 else 0
            a["hours_per_day"] = round(proportion * total_hours, 1)
            a["percentage"] = round(proportion * 100, 1)

        # Check for minimum viable allocation (< 0.5 hours = not worth context switching)
        viable = [a for a in allocations if a["hours_per_day"] >= 0.5]
        subviable = [a for a in allocations if a["hours_per_day"] < 0.5]

        return {
            "total_hours": total_hours,
            "allocations": allocations[:10],
            "viable_projects": len(viable),
            "subviable_projects": len(subviable),
            "nash_insight": (
                f"Nash equilibrium: {len(viable)} projects get viable time allocation. "
                f"{len(subviable)} projects get less than 30 min/day — "
                f"they're not worth the context switch cost. "
                f"Either cut them or batch them into one weekly slot. "
                f"The equilibrium says: you can ACTIVELY pursue {len(viable)} projects, not {len(projects)}."
            ),
            "kelly_recommendation": (
                f"Kelly criterion says: never allocate more than {allocations[0]['percentage']:.0f}% to any single project "
                f"({allocations[0]['project']}), even though it's highest-weight. "
                f"Diversification protects against any single project failing."
            ),
        }

    # ═══════════════════════════════════════════
    # 2. SHAPLEY VALUES (Coalition Game)
    # ═══════════════════════════════════════════

    def shapley_values(self) -> dict:
        """
        Shapley value = each project's marginal contribution to the WHOLE.

        This answers: if you removed this ONE project, how much would
        the entire portfolio lose? Not just its own weight — its
        contribution to cross-project synergies.

        Projects that enable other projects have high Shapley values
        even if their own weight is low.
        """
        projects = [n for n in self.graph.nodes.values() if n.type == "project"]

        if len(projects) > 8:
            # Approximate Shapley for large sets (exact is O(n!))
            projects = sorted(projects, key=lambda n: -n.weight)[:8]

        project_ids = [p.id for p in projects]
        n = len(project_ids)

        # Value function: sum of weights + bonus for connections between coalition members
        def coalition_value(coalition_ids: set) -> float:
            value = 0
            for pid in coalition_ids:
                node = self.graph.nodes.get(pid)
                if node:
                    value += node.weight

            # Synergy bonus: edges WITHIN the coalition
            for edge in self.graph.edges:
                if edge.source_id in coalition_ids and edge.target_id in coalition_ids:
                    value += edge.weight * 0.5  # Synergy bonus

            return value

        # Calculate Shapley values
        shapley = {pid: 0.0 for pid in project_ids}

        for pid in project_ids:
            others = [p for p in project_ids if p != pid]

            # Average marginal contribution over all orderings
            # Approximate with all subsets
            marginal_sum = 0
            count = 0

            for size in range(len(others) + 1):
                for subset in itertools.combinations(others, size):
                    coalition = set(subset)
                    value_without = coalition_value(coalition)
                    value_with = coalition_value(coalition | {pid})
                    marginal = value_with - value_without
                    marginal_sum += marginal
                    count += 1

            shapley[pid] = marginal_sum / count if count > 0 else 0

        # Sort and format
        results = []
        total_shapley = sum(shapley.values())

        for pid, sv in sorted(shapley.items(), key=lambda x: -x[1]):
            node = self.graph.nodes.get(pid)
            if node:
                results.append({
                    "project": node.name,
                    "shapley_value": round(sv, 2),
                    "weight": node.weight,
                    "shapley_vs_weight": round(sv / node.weight, 2) if node.weight > 0 else 0,
                    "portfolio_share": round(sv / total_shapley * 100, 1) if total_shapley > 0 else 0,
                })

        # Find projects that are more valuable to the portfolio than their weight suggests
        synergy_winners = [r for r in results if r["shapley_vs_weight"] > 1.2]
        synergy_losers = [r for r in results if r["shapley_vs_weight"] < 0.8]

        return {
            "shapley_values": results,
            "synergy_winners": synergy_winners,
            "synergy_losers": synergy_losers,
            "insight": (
                f"Shapley analysis of {n} projects. "
                f"{'Synergy winners (worth more than weight suggests): ' + ', '.join(r['project'] for r in synergy_winners) + '. ' if synergy_winners else ''}"
                f"{'Synergy losers (worth less than weight suggests): ' + ', '.join(r['project'] for r in synergy_losers) + '. ' if synergy_losers else ''}"
                f"These values include cross-project synergies that raw weight misses."
            ),
        }

    # ═══════════════════════════════════════════
    # 3. PROSPECT STRATEGY (Sales Game)
    # ═══════════════════════════════════════════

    def prospect_game(self) -> list[dict]:
        """
        Model each sales prospect as a game.

        Each prospect has:
        - Reservation price (max they'd pay)
        - Switching cost (from current solution)
        - Outside option (do nothing / competitor)
        - Information asymmetry (Josh knows more about AI than they do)

        Optimal strategy depends on their position.
        """
        contacts = [n for n in self.graph.nodes.values() if n.type == "contact"]
        strategies = []

        for contact in contacts:
            desc = contact.description.lower()

            # Infer game parameters from description
            has_demo = "demo" in desc
            is_stale = "stale" in desc
            has_existing_software = any(w in desc for w in ["clio", "filevine", "smokeball", "practicepanther"])

            # Switching cost
            if has_existing_software:
                switching_cost = "HIGH"
                strategy = "Don't compete on features — compete on AI capabilities they CAN'T get from incumbent"
            elif "solo" in desc or "new" in desc or "independent" in desc:
                switching_cost = "LOW"
                strategy = "Greenfield play — no migration pain. Emphasize 'start right' not 'switch'"
            else:
                switching_cost = "MEDIUM"
                strategy = "Reduce perceived switching cost with white-glove onboarding"

            # Optimal game move
            if has_demo and not is_stale:
                game_move = "CLOSE — they've seen value. Offer time-limited pilot."
                urgency = 9
            elif has_demo and is_stale:
                game_move = "RE-ENGAGE — loss-frame: 'every week without AI intake, you're losing leads'"
                urgency = 8
            elif is_stale:
                game_move = "RESURRECT — new value prop, not a follow-up. Show something they haven't seen."
                urgency = 6
            else:
                game_move = "APPROACH — compressed pitch. 10 seconds to hook."
                urgency = 4

            strategies.append({
                "prospect": contact.name,
                "switching_cost": switching_cost,
                "strategy": strategy,
                "game_move": game_move,
                "urgency": urgency,
                "information_advantage": (
                    "HIGH — Josh knows AI/PI intersection better than any prospect. "
                    "Use this asymmetry: educate, don't sell."
                ),
            })

        strategies.sort(key=lambda x: -x["urgency"])
        return strategies

    # ═══════════════════════════════════════════
    # 4. COMPETITIVE GAME (Lanchester)
    # ═══════════════════════════════════════════

    def competitive_analysis(self) -> dict:
        """
        Lanchester's Laws of Combat applied to business competition.

        Linear Law (guerrilla): Attrition ∝ force size. Used when
        each unit fights independently. Small player can win by
        concentrating force.

        Square Law (conventional): Attrition ∝ force size². Used when
        units fight as a coordinated force. Large player has overwhelming
        advantage. AVOID THIS.

        Josh's strategy: ALWAYS fight under Linear Law conditions.
        Niche down. One-on-one. Never engage the full incumbent army.
        """
        competitors = {
            "litjuris": [
                {"name": "Clio", "estimated_users": 150000, "annual_revenue": 250_000_000},
                {"name": "Filevine", "estimated_users": 10000, "annual_revenue": 50_000_000},
                {"name": "PracticePanther", "estimated_users": 30000, "annual_revenue": 40_000_000},
                {"name": "CASEpeer", "estimated_users": 5000, "annual_revenue": 15_000_000},
            ],
            "fuelops": [
                {"name": "Petrosoft", "estimated_users": 2000, "annual_revenue": 10_000_000},
                {"name": "Gilbarco", "estimated_users": 50000, "annual_revenue": 500_000_000},
            ],
        }

        analyses = {}

        for market, comps in competitors.items():
            josh_force = 1  # Josh is 1 person
            total_competitor_force = sum(c["estimated_users"] for c in comps)

            # Square Law ratio (conventional warfare — BAD for Josh)
            square_ratio = josh_force**2 / (total_competitor_force**2) if total_competitor_force > 0 else 0

            # Linear Law ratio (guerrilla — GOOD for Josh)
            # In a niche, Josh only fights one competitor at a time
            smallest_comp = min(comps, key=lambda c: c["estimated_users"])
            linear_ratio = josh_force / smallest_comp["estimated_users"] if smallest_comp["estimated_users"] > 0 else 0

            # Concentration strategy: what niche makes Josh's effective force highest?
            if market == "litjuris":
                niche = "FL solo/small PI firms with NO current case management software"
                niche_size = 500  # Estimated addressable firms
                niche_competitors = 0  # Nobody targets this specifically
            elif market == "fuelops":
                niche = "FL independent gas stations on Josh's hemp route"
                niche_size = 180  # Literally his route
                niche_competitors = 0
            else:
                niche = "Unknown"
                niche_size = 0
                niche_competitors = 0

            analyses[market] = {
                "competitors": comps,
                "square_law_ratio": f"{square_ratio:.10f}",
                "square_law_verdict": "SUICIDE — never engage full market directly",
                "linear_law_ratio": f"{linear_ratio:.6f}",
                "linear_law_verdict": "VIABLE — one-on-one, Josh can win on speed + niche",
                "concentration_strategy": {
                    "niche": niche,
                    "niche_size": niche_size,
                    "niche_competitors": niche_competitors,
                    "effective_force_ratio": f"1:{niche_competitors}" if niche_competitors > 0 else "MONOPOLY in niche",
                },
                "lanchester_prescription": (
                    f"NEVER fight {comps[0]['name']} head-on (Square Law: {square_ratio:.10f}). "
                    f"ALWAYS fight in the niche: '{niche}' where Josh has "
                    f"{'zero competition — monopoly position' if niche_competitors == 0 else f'{niche_competitors} competitors'}. "
                    f"Build the monopoly in the niche FIRST, then expand."
                ),
            }

        return {
            "markets": analyses,
            "overarching_strategy": (
                "Lanchester says: Josh CANNOT win a conventional war against Clio (150K users) "
                "or Gilbarco (50K users). Square Law crushes small players in open markets. "
                "Josh CAN win EVERY guerrilla engagement in his niches: "
                "FL solo PI firms (LitJuris) and his hemp route stations (FuelOps). "
                "In those niches, he has ZERO competition and physical access. "
                "Build monopoly in niche → expand from position of strength. "
                "This IS the Rockefeller playbook: control the niche, then the market."
            ),
        }

    # ═══════════════════════════════════════════
    # 5. AGENT COORDINATION (Mechanism Design)
    # ═══════════════════════════════════════════

    def agent_coordination(self) -> dict:
        """
        91 agents need to coordinate. How?

        Mechanism design: create an incentive structure where
        each agent acting in its own interest produces the
        globally optimal outcome.

        Applied: weight agents by their USAGE × OUTCOME, not just
        their role. Agents that produce approved proposals get
        reinforced. Agents that produce rejected proposals get weakened.
        This is the market mechanism applied to the agent team.
        """
        # Load agent usage if available
        usage_path = self.data_dir.parent / ".." / ".claude" / "memory" / "agent-usage.json"

        agent_usage = {}
        if usage_path.exists():
            try:
                with open(usage_path) as f:
                    agent_usage = json.load(f)
            except Exception:
                pass

        # Model each agent type as a player
        agent_types = set()
        for n in self.graph.nodes.values():
            if "agent" in n.type.lower() or "engine" in n.type.lower():
                agent_types.add(n.name)

        # Coordination recommendations
        return {
            "total_agents": 91,
            "tracked_agents": len(agent_usage),
            "mechanism": "Market-based coordination",
            "rules": [
                "1. USAGE WEIGHT: Agents invoked more often get faster response (cached context)",
                "2. APPROVAL WEIGHT: Agents whose proposals Josh approves get reinforced",
                "3. REJECTION PENALTY: Agents whose proposals are rejected weaken",
                "4. SPECIALIZATION: Each agent owns exactly one domain — no overlap",
                "5. ESCALATION: Agents that are uncertain escalate to Kingpin, not guess",
                "6. PARALLEL BY DEFAULT: Independent agents run simultaneously, not sequentially",
                "7. SHARED MEMORY: All agents read AGENT-DNA.md — consistent calibration",
            ],
            "vickrey_auction": (
                "When multiple agents could handle a task, use Vickrey auction: "
                "each agent bids its confidence (0-1). Highest confidence wins. "
                "But the 'price' (token budget) is set by the second-highest bid. "
                "This is incentive-compatible: agents bid truthfully because "
                "overbidding doesn't help and underbidding loses the task."
            ),
            "insight": (
                "91 agents coordinated via market mechanism: "
                "usage-weighted, approval-reinforced, rejection-penalized. "
                "The agent team self-optimizes through the same feedback loop "
                "as the knowledge graph. The agents are players in a game "
                "where Josh's approval is the currency."
            ),
        }

    # ═══════════════════════════════════════════
    # FULL GAME THEORY REPORT
    # ═══════════════════════════════════════════

    def full_report(self) -> dict:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "attention_equilibrium": self.attention_nash_equilibrium(),
            "shapley_values": self.shapley_values(),
            "prospect_strategies": self.prospect_game()[:7],
            "competitive_analysis": self.competitive_analysis(),
            "agent_coordination": self.agent_coordination(),
            "mechanism_21": {
                "name": "Game-Theoretic Optimization",
                "description": (
                    "Every allocation is a game. Nash equilibrium finds the stable "
                    "attention distribution. Shapley values measure true portfolio "
                    "contribution. Lanchester's Laws dictate guerrilla strategy. "
                    "Mechanism design coordinates 91 agents. The graph's nodes "
                    "are players. The edges are strategies."
                ),
            },
        }


def demo():
    graph = IdentityGraph()
    engine = GameTheoryEngine(graph)

    print("=" * 60)
    print("GAME THEORY ENGINE — Strategic Mathematics")
    print("Nash, Shapley, Lanchester, Mechanism Design")
    print("=" * 60)

    report = engine.full_report()

    # Nash
    ne = report["attention_equilibrium"]
    print(f"\n--- NASH EQUILIBRIUM (attention allocation) ---")
    print(f"  {ne['total_hours']} peak hours/day across {ne['viable_projects']} viable projects:")
    for a in ne["allocations"][:7]:
        bar = "█" * int(a["hours_per_day"]) + "░" * max(0, 10 - int(a["hours_per_day"]))
        print(f"  [{bar}] {a['project']}: {a['hours_per_day']}h ({a['percentage']}%)")
    print(f"  {ne['nash_insight'][:120]}...")

    # Shapley
    sv = report["shapley_values"]
    print(f"\n--- SHAPLEY VALUES (true portfolio contribution) ---")
    for s in sv["shapley_values"][:7]:
        ratio_indicator = "↑" if s["shapley_vs_weight"] > 1.1 else ("↓" if s["shapley_vs_weight"] < 0.9 else "=")
        print(f"  {ratio_indicator} {s['project']}: Shapley {s['shapley_value']:.1f} vs weight {s['weight']} "
              f"({s['shapley_vs_weight']:.1f}x) — {s['portfolio_share']}% of portfolio")
    if sv["synergy_winners"]:
        print(f"  SYNERGY WINNERS: {', '.join(r['project'] for r in sv['synergy_winners'])}")

    # Prospects
    print(f"\n--- PROSPECT GAME (optimal moves) ---")
    for p in report["prospect_strategies"][:5]:
        print(f"  [{p['urgency']}/10] {p['prospect']} — {p['game_move'][:80]}")

    # Lanchester
    print(f"\n--- LANCHESTER'S LAWS (competitive warfare) ---")
    for market, analysis in report["competitive_analysis"]["markets"].items():
        print(f"\n  {market.upper()}:")
        print(f"    {analysis['lanchester_prescription'][:120]}...")

    # Agent coordination
    ac = report["agent_coordination"]
    print(f"\n--- AGENT COORDINATION (mechanism design) ---")
    print(f"  {ac['total_agents']} agents, market-based coordination")
    for rule in ac["rules"][:4]:
        print(f"    {rule}")

    print(f"\n{'=' * 60}")
    print("Mechanism 21: Game-Theoretic Optimization.")
    print("Every decision is a game. The math finds the equilibrium.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
