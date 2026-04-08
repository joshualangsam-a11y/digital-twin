#!/usr/bin/env python3
"""
DEMO: New Engines (Session Bridge, Domain Router, Recursive Theory)

Shows how the three new engines work together as part of the digital twin.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.identity_graph import IdentityGraph
from engines.session_bridge import SessionBridge
from engines.domain_router import DomainRouter
from engines.recursive_theory import RecursiveTheory


def demo_session_bridge():
    """Session Bridge: Cross-session working memory."""
    print("\n" + "=" * 70)
    print("SESSION BRIDGE — Cross-Session Working Memory")
    print("=" * 70)

    graph = IdentityGraph()
    bridge = SessionBridge(graph)

    # Start a work session
    print("\n[START SESSION] Morning work session...")
    session = bridge.start_session("work")
    print(f"  Session ID: {session['session_id']}")
    print(f"  Context priorities: {session['context']['priorities'][:3]}")

    # During the session, record thoughts and insights
    print("\n[DURING SESSION] Working on code...")
    bridge.record_thought(
        "Parallel tracks might not be for engagement — they're thermal management",
        about_node_id="concept_adhd",
        confidence=0.6,
    )

    print("\n[AHA MOMENT] Insight crystallizes...")
    aha = bridge.record_aha_moment(
        insight="ADHD brains distribute thermal load across domains, not a focus failure",
        connected_nodes=["concept_adhd", "concept_bandwidth"],
        novelty="connection",
    )
    print(f"  Aha ID: {aha['id']}")
    print(f"  Added to graph: {aha['added_to_graph']}")

    print("\n[PROGRESS] Recording work on FuelOps...")
    bridge.record_progress(
        "fuelops",
        "Implemented demo endpoint",
        blockers=["Need to add authentication"],
    )

    print("\n[THERMAL STATE] Updating cognitive load...")
    thermal = bridge.update_thermal_state(0.65)
    print(f"  Thermal level: {thermal['thermal_level']}")
    print(f"  Status: {thermal['status']}")
    print(f"  Recommendation: {thermal['recommendation']}")

    # End session and save state
    print("\n[END SESSION] Saving session state...")
    end = bridge.end_session()
    print(f"  Snapshot saved to: {end['snapshot_file']}")
    print(f"  Aha moments protected: {end['aha_moments_protected']}")
    print(f"  Unfinished threads: {end['unfinished_threads']}")

    # Stats
    stats = bridge.stats()
    print(f"\n[SESSION STATS]")
    print(f"  Total sessions: {stats['total_sessions']}")
    print(f"  Total aha moments: {stats['total_aha_moments']}")
    print(f"  Total unfinished threads: {stats['total_unfinished_threads']}")


def demo_domain_router():
    """Domain Router: Cognitive thermal management."""
    print("\n" + "=" * 70)
    print("DOMAIN ROUTER — Cognitive Thermal Management")
    print("=" * 70)

    graph = IdentityGraph()
    router = DomainRouter(graph)

    # Start in code_building domain
    print("\n[DOMAIN SWITCH] Starting with code_building...")
    switch = router.switch_to_domain("code_building", reason="Morning focus")
    print(f"  Domain: {switch['domain']}")
    print(f"  Description: {switch['description']}")

    # Simulate work with errors
    print("\n[WORK SESSION] Code building for 30 minutes, 2 errors...")
    result = router.record_work(
        "code_building",
        duration_minutes=30,
        errors=2,
        quality_score=0.8,
    )
    print(f"  Thermal: {result['thermal']}")
    print(f"  Status: {result['thermal_status']}")

    # Domain is getting hot, suggest switch
    print("\n[THERMAL MANAGEMENT] Simulate more code work (adding heat)...")
    router.record_work("code_building", duration_minutes=20, errors=3, quality_score=0.7)

    suggestion = router.suggest_domain_switch()
    if suggestion:
        print(f"  SUGGESTION: {suggestion['reason']}")
        print(f"  Recommended domain: {suggestion['suggested_domain']}")

    # Switch to cool domain
    print("\n[PARALLEL TRACK] Opening writing track to cool code domain...")
    router.open_parallel_track("writing", reason="Cool code domain while doing docs")

    # Get thermal map
    print("\n[THERMAL MAP]")
    thermal_map = router.get_thermal_map()
    print(f"  Current domain: {thermal_map['current_domain']}")
    print(f"  Active tracks: {thermal_map['active_tracks']}")
    for domain, state in list(thermal_map["domains"].items())[:3]:
        print(f"    {domain}: {state['thermal']} ({state['status']})")

    # Stats
    stats = router.stats()
    print(f"\n[DOMAIN STATS]")
    print(f"  Total time: {stats['total_domain_time_hours']} hours")
    print(f"  Total errors: {stats['total_errors_across_domains']}")


def demo_recursive_theory():
    """Recursive Theory: Theory-building from code."""
    print("\n" + "=" * 70)
    print("RECURSIVE THEORY — Theory-Building as Bandwidth Mechanism")
    print("=" * 70)

    graph = IdentityGraph()
    theory = RecursiveTheory(graph)

    # Observe patterns emerging from other engines
    print("\n[PATTERN 1] From domain_router...")
    theory.observe_pattern(
        source="domain_router",
        pattern_name="Thermal Zones Trigger Domain Switches",
        evidence=[
            "Domain heat > 0.7 → suggestion generated",
            "User switched domains after 3 observations",
            "New domain cooled, enabled continuation",
        ],
        confidence=0.6,
    )

    print("\n[PATTERN 2] From session_bridge...")
    theory.observe_pattern(
        source="session_bridge",
        pattern_name="Aha Moments Enable Cross-Session Recall",
        evidence=[
            "5 aha moments recorded and added to graph",
            "Next session context included 4/5 of those concepts",
            "User recalled insights without prompting",
        ],
        confidence=0.8,
    )

    # Get active theories to find the right pattern ID
    active = theory.get_active_theories()
    aha_pattern_id = None
    for pid, p in active.items():
        if "aha" in p["name"].lower():
            aha_pattern_id = pid
            break

    # Crystallize second pattern (confidence > 0.7)
    if aha_pattern_id:
        print("\n[CRYSTALLIZE] Aha moment pattern → theory...")
        crystallized = theory.crystallize_theory(
            pattern_id=aha_pattern_id,
            name="Aha Moments as Cross-Session Bridges",
            description="High-confidence insights, when immediately added to graph, survive session resets and trigger recall in subsequent sessions",
            implication="ADHD working memory resets are not catastrophic if critical insights are protected immediately. The identity graph is the time-bridge.",
            novel_mechanism=True,
        )
        print(f"  Theory ID: {crystallized['theory_id']}")
        print(f"  Status: {crystallized['status']}")
    else:
        # Manually create a theory node for demo purposes
        print("\n[CRYSTALLIZE] Creating theory node directly...")
        theory_node_id = "theory_aha_moments_as_bridges"
        crystallized = {"theory_id": theory_node_id, "status": "crystallized"}

    # Link theory to code
    print("\n[CODE LINKING] Theory → Implementation...")
    linked = theory.link_theory_to_code(
        theory_node_id=crystallized["theory_id"],
        file_path="engines/session_bridge.py",
        function_name="record_aha_moment",
        line_numbers=(156, 195),
    )
    print(f"  Linked: {linked['linked']}")

    # Record spiral iteration
    print("\n[SPIRAL ITERATION] Theory-building cycle...")
    spiral1 = theory.record_spiral_iteration(
        phase="observe",
        output="Patterns in session bridge logs",
        abstraction_level=0,
    )
    spiral2 = theory.record_spiral_iteration(
        phase="crystallize",
        output="Aha moment theory",
        abstraction_level=1,
    )
    spiral3 = theory.record_spiral_iteration(
        phase="code_link",
        output="Theory connected to session_bridge.record_aha_moment()",
        abstraction_level=1,
        back_to_code=True,
    )
    print(f"  Spiral iterations: {spiral3['spiral_iteration']}")

    # Generate academic paper
    print("\n[PAPER GENERATION] Academic synthesis...")
    paper = theory.generate_paper(
        title="Cross-Session Compounding in ADHD: The Identity Graph as Memory Bridge",
        theories=[crystallized["theory_id"]],
        abstract="This paper describes how immediately protecting aha moments in a persistent knowledge graph enables ADHD brains to compound intelligence across working memory resets.",
    )
    print(f"  Paper ID: {paper['paper_id']}")
    print(f"  Markdown: {paper['file_markdown']}")

    # Stats
    stats = theory.stats()
    print(f"\n[THEORY STATS]")
    print(f"  Total theories: {stats['total_theories']}")
    print(f"  Active patterns: {stats['active_patterns']}")
    print(f"  Crystallized: {stats['crystallized_theories']}")
    print(f"  Spiral iterations: {stats['spiral_iterations']}")
    print(f"  Papers generated: {stats['papers_generated']}")


def main():
    print("\n" + "=" * 70)
    print("DIGITAL TWIN — New Engines Demo")
    print("=" * 70)

    demo_session_bridge()
    demo_domain_router()
    demo_recursive_theory()

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nAll three engines are now operational:")
    print("  1. SessionBridge — Protects working memory across sleep")
    print("  2. DomainRouter — Manages cognitive thermal load")
    print("  3. RecursiveTheory — Generates theory from implementation")
    print("\nAgent definitions in .claude/agents/:")
    print("  - twin-core.md — Builds identity graph + twin orchestrator")
    print("  - twin-bandwidth.md — Builds bandwidth expansion engines")
    print("  - twin-bridge.md — Builds session bridge")
    print("  - twin-theory.md — Builds theory-building system")
    print("=" * 70)


if __name__ == "__main__":
    main()
