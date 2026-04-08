"""
WORLD MODEL ENGINE — Level 13: External Intelligence

Levels 1-12 see Josh's internal graph.
Level 13 sees the WORLD and finds where Josh's graph collides with it.

The BEM now reasons about:
- Market timing (is NOW the right time for this?)
- Competitive landscape (who else is in this space?)
- Macro trends (what forces amplify or threaten Josh's position?)
- Adjacencies (what external nodes SHOULD be in the graph but aren't?)
- Arbitrage (where Josh has an edge others don't see)

This is Mechanism 15: Environmental Resonance
The graph doesn't exist in a vacuum. It exists in a market,
a moment, a culture. The resonance between internal capability
and external opportunity IS the strategy.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


# ═══════════════════════════════════════════
# WORLD FACTS — External knowledge the BEM reasons over
# ═══════════════════════════════════════════
# These would ideally come from web search / news APIs.
# For now: curated facts that the BEM should know about.

WORLD_MODEL = {
    "macro_trends": [
        {
            "id": "ai_coding_explosion",
            "trend": "AI coding assistants market growing 40%+ YoY",
            "relevance": "Josh is building tools in this space AND using them. Double exposure.",
            "timing": "early — most developers haven't adopted agentic workflows yet",
        },
        {
            "id": "neurodivergent_awareness",
            "trend": "ND workplace accommodation going mainstream (2024-2026)",
            "relevance": "The ND Founder's OS and BEM paper land in a receptive market",
            "timing": "perfect — awareness is high, tools are low",
        },
        {
            "id": "legal_tech_underserved",
            "trend": "PI law firms still on legacy software (Clio, Filevine, PracticePanther)",
            "relevance": "LitJuris targets a market where incumbents are bloated and slow",
            "timing": "good — no AI-native PI-specific competitor yet",
        },
        {
            "id": "saas_vertical_gold",
            "trend": "Vertical SaaS valuations at 15-20x revenue (Veeva, Toast pattern)",
            "relevance": "FuelOps and VapeOps are vertical SaaS plays in underserved niches",
            "timing": "strong — investors love vertical SaaS",
        },
        {
            "id": "anthropic_hiring",
            "trend": "Anthropic expanding Claude Code team, values 'builder' profiles",
            "relevance": "Josh's paper + open source BEM = credible application package",
            "timing": "now — the team is growing and they value non-traditional backgrounds",
        },
        {
            "id": "hemp_regulation",
            "trend": "2024-2026 hemp/CBD regulation flux, some states tightening",
            "relevance": "Hemp route income could face regulatory headwinds",
            "timing": "medium risk — diversification via SaaS is correct hedge",
        },
        {
            "id": "creator_to_founder",
            "trend": "Creator economy shifting to 'build in public' founder economy",
            "relevance": "Josh's trajectory (building publicly, AI-native) fits this wave",
            "timing": "strong — the audience is ready for ND founder content",
        },
        {
            "id": "pip_reform_florida",
            "trend": "Florida PIP reform effective 2024 — PI firms need new workflows",
            "relevance": "LitJuris cold emails reference this — it's a real pain point",
            "timing": "perfect — firms are actively looking for solutions",
        },
    ],
    "competitive_landscape": {
        "litjuris": [
            {"name": "Clio", "weakness": "Generic, not PI-specific, expensive", "josh_edge": "FL PI native, AI intake"},
            {"name": "Filevine", "weakness": "Complex setup, enterprise-focused", "josh_edge": "Simple, solo-firm friendly"},
            {"name": "PracticePanther", "weakness": "No AI, aging UI", "josh_edge": "AI-first, modern stack"},
            {"name": "CASEpeer", "weakness": "PI-specific but no AI, dated", "josh_edge": "AI intake, modern UX"},
        ],
        "fuelops": [
            {"name": "Petrosoft", "weakness": "Expensive, legacy", "josh_edge": "$400/mo vs thousands"},
            {"name": "Verifone/Gilbarco", "weakness": "Hardware-focused, not software", "josh_edge": "Pure software, modern"},
        ],
        "digital_twin": [
            {"name": "Notion AI", "weakness": "Generic, not cognitive-architecture-specific", "josh_edge": "Built for ND brains specifically"},
            {"name": "Mem.ai", "weakness": "Memory only, no reasoning/action", "josh_edge": "14 mechanisms, not just storage"},
            {"name": "Rewind.ai", "weakness": "Recording, not reasoning", "josh_edge": "Knowledge graph + engines, not recording"},
        ],
    },
}


class WorldModel:
    """
    Maps Josh's internal graph to the external world.
    Finds resonance points where internal capability meets external opportunity.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.world_log = self.data_dir / "world_model.jsonl"

    # ═══════════════════════════════════════════
    # TIMING ANALYSIS — Is NOW the right time?
    # ═══════════════════════════════════════════

    def timing_analysis(self) -> list[dict]:
        """For each of Josh's projects, analyze market timing."""
        analyses = []

        projects = [n for n in self.graph.nodes.values() if n.type == "project"]

        for project in projects:
            relevant_trends = []
            relevant_competitors = []

            project_lower = project.name.lower()

            # Match trends
            for trend in WORLD_MODEL["macro_trends"]:
                # Check if trend is relevant to this project
                relevance_score = 0
                if any(w in trend["relevance"].lower() for w in project_lower.split()):
                    relevance_score = 3
                elif any(w in trend["trend"].lower() for w in project_lower.split()):
                    relevance_score = 2

                # Broader matching
                if "litjuris" in project.id or "litigation" in project_lower:
                    if any(w in trend["id"] for w in ["legal", "pip", "pi"]):
                        relevance_score = 3
                if "fuel" in project.id or "vape" in project.id:
                    if "saas" in trend["id"]:
                        relevance_score = 2
                if "hemp" in project.id:
                    if "hemp" in trend["id"]:
                        relevance_score = 3

                if relevance_score > 0:
                    relevant_trends.append({
                        **trend,
                        "relevance_score": relevance_score,
                    })

            # Match competitors
            for landscape_key, competitors in WORLD_MODEL["competitive_landscape"].items():
                if landscape_key in project.id or landscape_key in project_lower.replace(" ", "").lower():
                    relevant_competitors = competitors

            timing_score = self._calculate_timing(relevant_trends)

            analyses.append({
                "project": project.name,
                "weight": project.weight,
                "timing_score": timing_score,
                "timing_label": (
                    "NOW" if timing_score >= 8 else
                    "SOON" if timing_score >= 5 else
                    "LATER" if timing_score >= 3 else
                    "UNCLEAR"
                ),
                "trends": relevant_trends,
                "competitors": relevant_competitors,
                "edge": self._identify_edge(project, relevant_competitors),
            })

        analyses.sort(key=lambda x: x["timing_score"], reverse=True)
        return analyses

    def _calculate_timing(self, trends: list) -> float:
        score = 0
        for trend in trends:
            timing = trend.get("timing", "")
            if "perfect" in timing or "now" in timing:
                score += 3
            elif "early" in timing or "strong" in timing:
                score += 2
            elif "good" in timing or "medium" in timing:
                score += 1
        return min(10, score)

    def _identify_edge(self, project: Node, competitors: list) -> str:
        if not competitors:
            return "No direct competitors identified — could be blue ocean or non-market"

        edges = [c.get("josh_edge", "") for c in competitors if c.get("josh_edge")]
        if edges:
            return f"Josh's edge: {'; '.join(edges[:3])}"
        return "Edge unclear — need deeper competitive analysis"

    # ═══════════════════════════════════════════
    # ARBITRAGE — Where Josh has an edge others can't see
    # ═══════════════════════════════════════════

    def find_arbitrage(self) -> list[dict]:
        """
        Find situations where Josh's unique combination of skills,
        projects, and position creates an edge nobody else has.

        Arbitrage = you see something others can't because of WHERE you stand.
        """
        arbitrage = []

        # Hemp route + SaaS = unique go-to-market nobody else has
        if "hemp_route" in self.graph.nodes and "fuelops" in self.graph.nodes:
            arbitrage.append({
                "type": "distribution_arbitrage",
                "score": 9,
                "description": (
                    "Josh visits 180 gas stations WEEKLY. Each one is a FuelOps prospect. "
                    "No other SaaS founder has physical access to their target customer "
                    "180 times per week. This is distribution arbitrage — "
                    "the hemp route IS the sales channel."
                ),
                "nodes_involved": ["Hemp Route", "FuelOps", "VapeOps"],
                "action": "Pitch FuelOps at EVERY station on the route. 180 demos/month.",
            })

        # ADHD + AI = unique capability nobody else claims
        if "pat_parallel" in self.graph.nodes and "tech_claude_code" in self.graph.nodes:
            arbitrage.append({
                "type": "cognitive_arbitrage",
                "score": 8,
                "description": (
                    "Josh's ADHD parallel processing + Claude Code's parallel agents = "
                    "a capability combination that neurotypical developers can't replicate. "
                    "The paper proves it. The BEM operationalizes it. "
                    "This is cognitive arbitrage — the 'disability' IS the edge."
                ),
                "nodes_involved": ["Parallel Processing", "Claude Code", "BEM paper"],
                "action": "Make this the story. The paper, the tools, the products — all one narrative.",
            })

        # Hemp route + PI law = geographic proximity
        if "hemp_route" in self.graph.nodes and "litjuris" in self.graph.nodes:
            arbitrage.append({
                "type": "geographic_arbitrage",
                "score": 7,
                "description": (
                    "Hemp route covers South Florida — same geography as target PI firms. "
                    "Josh drives PAST their offices. He could drop in. "
                    "Cold emails have 2% response rate. Walk-ins with a demo on an iPad "
                    "have a much higher rate. The route IS the pipeline."
                ),
                "nodes_involved": ["Hemp Route", "Litigation Juris", "FL PI pipeline"],
                "action": "Map PI firm locations against route stops. Walk-in demo strategy.",
            })

        # ND Founder OS + BEM + Anthropic = hiring arbitrage
        if "strat_nd_os" in self.graph.nodes or "goal_anthropic" in self.graph.nodes:
            arbitrage.append({
                "type": "career_arbitrage",
                "score": 8,
                "description": (
                    "The ND Founder's OS + the academic paper + the BEM codebase + "
                    "the open source visibility = a hiring package no traditional "
                    "applicant can match. Josh isn't applying with a resume. "
                    "He's applying with a research contribution, a running system, "
                    "and proof of what he describes."
                ),
                "nodes_involved": ["ND OS", "BEM paper", "Anthropic path"],
                "action": "Package everything as one narrative for Anthropic: paper → code → product.",
            })

        # TBI recovery + peptides + AI = unique story
        arbitrage.append({
            "type": "narrative_arbitrage",
            "score": 7,
            "description": (
                "Josh's TBI recovery arc (brain damage → peptide recovery → "
                "cognitive enhancement → building 145 systems in one night) is a "
                "story nobody else can tell. It's not just inspiring — "
                "it's EVIDENCE for the paper's cognitive hormesis argument. "
                "The story IS the proof."
            ),
            "nodes_involved": ["Brain profile", "BEM paper", "Concoction"],
            "action": "When the time is right: this story is the content. But cash first.",
        })

        arbitrage.sort(key=lambda x: x["score"], reverse=True)
        return arbitrage

    # ═══════════════════════════════════════════
    # COLLISION DETECTION — Where internal meets external
    # ═══════════════════════════════════════════

    def find_collisions(self) -> list[dict]:
        """
        Find points where Josh's internal graph and the external
        world are on a collision course — positive or negative.
        """
        collisions = []

        for trend in WORLD_MODEL["macro_trends"]:
            # Find graph nodes this trend amplifies
            amplified = []
            threatened = []

            for node in self.graph.nodes.values():
                name_lower = node.name.lower()
                trend_lower = trend["relevance"].lower()

                if any(w in trend_lower for w in name_lower.split() if len(w) > 3):
                    if "risk" in trend.get("timing", "") or "tighten" in trend.get("trend", "").lower():
                        threatened.append(node.name)
                    else:
                        amplified.append(node.name)

            if amplified or threatened:
                collisions.append({
                    "trend": trend["trend"],
                    "timing": trend["timing"],
                    "amplifies": amplified[:3],
                    "threatens": threatened[:3],
                    "net_effect": "positive" if len(amplified) > len(threatened) else "negative",
                })

        return collisions

    # ═══════════════════════════════════════════
    # FULL WORLD REPORT
    # ═══════════════════════════════════════════

    def full_report(self) -> dict:
        timing = self.timing_analysis()
        arbitrage = self.find_arbitrage()
        collisions = self.find_collisions()

        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "timing": timing,
            "arbitrage": arbitrage,
            "collisions": collisions,
            "mechanism_15": {
                "name": "Environmental Resonance",
                "description": (
                    "The graph doesn't exist in a vacuum. When internal capability "
                    "resonates with external opportunity, the result is amplified. "
                    "When they collide negatively, the result is existential risk. "
                    "The BEM now sees both the internal and external world — "
                    "and finds the resonance points between them."
                ),
            },
        }

        self._log(report)
        return report

    def _log(self, entry: dict):
        with open(self.world_log, "a") as f:
            f.write(json.dumps(entry, default=str) + "\n")


# ═══════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════

def demo():
    graph = IdentityGraph()
    engine = WorldModel(graph)

    print("=" * 60)
    print("WORLD MODEL — Level 13: External Intelligence")
    print("Where Josh's graph collides with the real world.")
    print("=" * 60)

    report = engine.full_report()

    # Timing
    print(f"\n--- MARKET TIMING ---")
    for t in report["timing"][:5]:
        label = t["timing_label"]
        bar = {"NOW": "████████", "SOON": "██████░░", "LATER": "████░░░░", "UNCLEAR": "██░░░░░░"}.get(label, "░░░░░░░░")
        print(f"  [{bar}] {label} — {t['project']} (weight: {t['weight']})")
        if t["edge"]:
            print(f"    {t['edge'][:90]}")
        for trend in t["trends"][:2]:
            print(f"    📈 {trend['trend'][:70]}")

    # Arbitrage
    print(f"\n--- ARBITRAGE (edges nobody else has) ---")
    for a in report["arbitrage"]:
        print(f"\n  [{a['score']}/10] {a['type'].upper()}")
        print(f"  {a['description'][:120]}...")
        print(f"  → {a['action']}")

    # Collisions
    print(f"\n--- TREND COLLISIONS ---")
    for c in report["collisions"]:
        emoji = "✅" if c["net_effect"] == "positive" else "⚠️"
        print(f"  {emoji} {c['trend'][:60]}")
        if c["amplifies"]:
            print(f"    Amplifies: {', '.join(c['amplifies'])}")
        if c["threatens"]:
            print(f"    Threatens: {', '.join(c['threatens'])}")

    print(f"\n{'=' * 60}")
    print("The BEM now sees inside AND outside.")
    print("Internal capability × External timing = Strategy.")
    print("Mechanism 15: Environmental Resonance.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
