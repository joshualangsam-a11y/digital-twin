"""
MEMORY INGESTION ENGINE

Reads all of Josh's memory files and builds the identity graph.
This is the bootstrap — converts flat markdown into structured intelligence.

Phase 1: Rule-based extraction (fast, deterministic)
Phase 2: LLM-assisted extraction (deeper, finds hidden connections)
"""

import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


MEMORY_DIRS = [
    os.path.expanduser("~/.claude/projects/-Users-joshualangsam/memory"),
    os.path.expanduser("~/.claude/memory"),
]


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter and body from markdown."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not match:
        return {}, content

    fm_text, body = match.groups()
    frontmatter = {}
    for line in fm_text.strip().split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter, body


def read_all_memories() -> list[dict]:
    """Read all memory files and return structured data."""
    memories = []
    for mem_dir in MEMORY_DIRS:
        if not os.path.exists(mem_dir):
            continue
        for f in sorted(Path(mem_dir).glob("*.md")):
            if f.name == "MEMORY.md":
                continue
            content = f.read_text()
            fm, body = parse_frontmatter(content)
            memories.append({
                "path": str(f),
                "filename": f.name,
                "frontmatter": fm,
                "body": body,
                "type": fm.get("type", "unknown"),
                "name": fm.get("name", f.stem),
                "description": fm.get("description", ""),
            })
    return memories


# ═══════════════════════════════════════════
# ENTITY EXTRACTORS
# ═══════════════════════════════════════════

def extract_josh(graph: IdentityGraph):
    """The central node — Josh himself."""
    josh = Node(
        id="josh",
        name="Josh Langsam",
        node_type="person",
        description="21, co-founder Roan Co., CTO. ADHD + dyslexia. Parallel processor. Builds in bursts. Pain → output.",
        weight=10.0,
        metadata={
            "age": 21,
            "role": "CTO & Co-Founder",
            "company": "Roan Co.",
            "neurotype": "ADHD + dyslexia",
            "cognitive_style": "parallel bursts, kinesthetic-visual, gut-first",
            "peak_hours": "afternoon/night",
            "mud_hours": "6-11 AM",
            "fuel": "house music, pain, curiosity",
        },
    )
    graph.add_node(josh)
    return josh


def extract_people(graph: IdentityGraph, memories: list[dict]):
    """Extract people from contact and user memory files."""
    people_patterns = {
        "contact_ethan_hampton": ("ethan", "Ethan Hampton", "Hemp boss, FuelOps co-founder"),
        "contact_zack_duckworth": ("zack", "Zack Duckworth", "FanForge/StreamSnip partner"),
        "contact_maggie": ("maggie", "Maggie", "Clemson friend, intellectual connection"),
        "contact_jakey_krumm": ("jakey", "Jakey Krumm", "FanForge Pro user"),
        "user_tristan": ("tristan", "Tristan", "Brother-in-law, Servicewright"),
        "user_roan_role": ("stiles", "Stiles", "CEO & Co-Founder, Roan Co."),
    }

    for mem in memories:
        stem = Path(mem["filename"]).stem
        if stem in people_patterns:
            pid, name, desc = people_patterns[stem]
            node = Node(
                id=pid, name=name, node_type="person",
                description=desc, source_file=mem["filename"], weight=3.0,
            )
            graph.add_node(node)
            graph.add_edge(Edge("josh", pid, "knows", evidence=mem["filename"]))

    # Stiles gets special edge
    if "stiles" in graph.nodes:
        graph.add_edge(Edge("josh", "stiles", "co_founded_with", label="Roan Co.", weight=5.0))
    if "ethan" in graph.nodes:
        graph.add_edge(Edge("josh", "ethan", "co_founded_with", label="FuelOps", weight=4.0))
        graph.add_edge(Edge("josh", "ethan", "depends_on", label="hemp route income", weight=5.0))


def extract_projects(graph: IdentityGraph, memories: list[dict]):
    """Extract projects and their relationships."""
    project_map = {
        "project_josh_job": ("hemp_route", "Hemp Route", "project", "#1 income, ~$600/day, 180→500 accounts", 9.0),
        "project_fuel_ops": ("fuelops", "FuelOps", "project", "$400/mo gas station SaaS, demo ready", 8.0),
        "project_vape_ops": ("vapeops", "VapeOps", "project", "$299/mo vape shop SaaS, needs Supabase", 7.0),
        "project_litigation_juris": ("litjuris", "Litigation Juris", "project", "PI-native legal case management SaaS", 7.0),
        "project_sushilab_tal": ("sushilab", "SushiLab", "project", "$600 Upwork milestone, freelance", 5.0),
        "project_alphaswarm": ("alphaswarm", "AlphaSwarm", "project", "Polymarket trading engine, long-term", 3.0),
        "project_streamsnip": ("streamsnip", "StreamSnip", "project", "AI video clipping, maintain only", 2.0),
        "project_nf_pouches": ("nf_pouches", "NF Pouches", "project", "Nicotine-free pouch distribution", 4.0),
        "project_fda_turbo": ("fda_turbo", "FDA TurboTax", "project", "AI FDA submission platform, with Charan & Daniel", 3.0),
    }

    priority_order = [
        "hemp_route", "fuelops", "vapeops", "sushilab", "litjuris",
        "nf_pouches", "alphaswarm", "streamsnip",
    ]

    for mem in memories:
        stem = Path(mem["filename"]).stem
        if stem in project_map:
            pid, name, ntype, desc, weight = project_map[stem]
            node = Node(
                id=pid, name=name, node_type=ntype,
                description=desc, source_file=mem["filename"], weight=weight,
            )
            graph.add_node(node)
            graph.add_edge(Edge("josh", pid, "builds", weight=weight))

    # Priority chain
    for i in range(len(priority_order) - 1):
        if priority_order[i] in graph.nodes and priority_order[i + 1] in graph.nodes:
            graph.add_edge(Edge(
                priority_order[i], priority_order[i + 1], "prioritized_over",
                label=f"Priority {i+1} > {i+2}", weight=2.0,
            ))

    # Cross-project patterns
    if "fuelops" in graph.nodes and "vapeops" in graph.nodes:
        graph.add_edge(Edge("fuelops", "vapeops", "pattern_matches",
            label="Same SaaS scaffold, different vertical", weight=4.0,
            evidence="VapeOps forked from FuelOps, 90% shared code"))

    if "hemp_route" in graph.nodes and "fuelops" in graph.nodes:
        graph.add_edge(Edge("hemp_route", "fuelops", "feeds_into",
            label="Route visits → SaaS upsell", weight=5.0,
            evidence="Gas stations on hemp route are FuelOps prospects"))

    if "hemp_route" in graph.nodes and "nf_pouches" in graph.nodes:
        graph.add_edge(Edge("hemp_route", "nf_pouches", "enables",
            label="180 stores = distribution channel", weight=4.0,
            evidence="NF pouches distributed through existing hemp route"))


def extract_companies(graph: IdentityGraph, memories: list[dict]):
    """Extract business entities."""
    companies = [
        ("roan_co", "Roan Co.", "LLC for Lit Juris, FuelOps, VapeOps", 5.0),
        ("langsam_capital", "Langsam Capital", "Personal holding LLC (NOT FILED)", 2.0),
        ("hampton_reserve", "Hampton Reserve", "Hemp distributor, Josh's employer", 4.0),
    ]

    for cid, name, desc, weight in companies:
        graph.add_node(Node(id=cid, name=name, node_type="company",
            description=desc, weight=weight))

    graph.add_edge(Edge("josh", "roan_co", "builds", label="Co-founder", weight=5.0))
    graph.add_edge(Edge("roan_co", "litjuris", "builds", weight=4.0))
    graph.add_edge(Edge("roan_co", "fuelops", "builds", weight=4.0))
    graph.add_edge(Edge("josh", "hampton_reserve", "uses", label="Employment", weight=5.0))
    graph.add_edge(Edge("hampton_reserve", "hemp_route", "enables", weight=5.0))


def extract_cognitive_model(graph: IdentityGraph, memories: list[dict]):
    """Extract Josh's cognitive patterns, values, fears — the soul of the twin."""

    # === CONCOCTION (10 ingredients as value nodes) ===
    concoction = [
        ("val_identity", "Identity Precedes Evidence", "'I am X' before proof exists"),
        ("val_suffering", "Suffering Is Fuel", "Pain is the toll booth, not the wrong road"),
        ("val_volume", "Obscene Volume", "4,000 calls not 40"),
        ("val_deafness", "Selective Deafness", "Only input from people who've been there"),
        ("val_no_exit", "No Exit", "Burn the boats"),
        ("val_declaration", "Public Declaration", "Say it before you have it"),
        ("val_speed_patience", "Speed of Decision, Patience of Execution", "Decide in 30 seconds, execute for 3 years"),
        ("val_no_failure", "Failure Doesn't Exist", "Only wins, lessons, incomplete experiments"),
        ("val_ownership", "Extreme Ownership", "Everything is my fault = everything is my power"),
        ("val_bigger", "Something Bigger", "Faith and stewardship"),
    ]

    for vid, name, desc in concoction:
        graph.add_node(Node(id=vid, name=name, node_type="value",
            description=desc, weight=4.0, source_file="user_concoction.md"))
        graph.add_edge(Edge("josh", vid, "uses", label="Concoction ingredient", weight=3.0))

    # === COGNITIVE PATTERNS ===
    patterns = [
        ("pat_parallel", "Parallel Processing", "Thinks A→B,F,M,Z simultaneously. Needs 3+ tracks or stalls.", 5.0),
        ("pat_kinesthetic", "Kinesthetic-Visual Thinking", "Feels ideas first (gut), then visual unfolding. Not verbal.", 4.0),
        ("pat_pain_output", "Pain → Output Conversion", "Emotional pressure = rocket fuel, not shutdown", 5.0),
        ("pat_cross_domain", "Cross-Domain Pattern Matching", "Sees one interconnected system, not separate projects", 5.0),
        ("pat_momentum", "Momentum Dependency", "In flow = unstoppable. Breaks = spiral risk.", 4.0),
        ("pat_gut_decision", "Gut-First Decision Making", "Decides in seconds. Doesn't revisit. High hit rate.", 4.0),
        ("pat_autodidact", "Autodidact Rabbit Holes", "Self-directed obsessive learning. Knowledge as game.", 4.0),
        ("pat_dual_emotion", "Dual-Timeline Emotion", "Real-time surface processing + delayed deep hits", 3.0),
        ("pat_bandwidth_gap", "Vision-Articulation Gap", "Brain faster than output channel. Not a deficit.", 3.0),
    ]

    for pid, name, desc, weight in patterns:
        graph.add_node(Node(id=pid, name=name, node_type="pattern",
            description=desc, weight=weight, source_file="user_brain_profile.md"))
        graph.add_edge(Edge("josh", pid, "uses", label="Cognitive pattern", weight=weight))

    # === FEARS ===
    fears = [
        ("fear_vision_wrong", "Vision Is Wrong", "That everything being built doesn't add up"),
        ("fear_exploitation", "Goodness Exploited", "People see genuine intentions and use them against him"),
        ("fear_not_impressive", "Is It Me Or The Tool", "Needing to know the magic is in him, not Claude"),
    ]

    for fid, name, desc in fears:
        graph.add_node(Node(id=fid, name=name, node_type="fear",
            description=desc, weight=3.0, source_file="user_brain_profile.md"))
        graph.add_edge(Edge("josh", fid, "fears", weight=3.0))

    # === PROTECTION MECHANISMS ===
    graph.add_edge(Edge("fear_exploitation", "val_deafness", "protects_via",
        label="Selective deafness protects against exploitation", weight=3.0))
    graph.add_edge(Edge("fear_not_impressive", "val_ownership", "protects_via",
        label="Extreme ownership = the value is in me, not the tool", weight=3.0))
    graph.add_edge(Edge("fear_vision_wrong", "pat_cross_domain", "protects_via",
        label="Pattern matching validates the vision through connections", weight=3.0))

    # === GOALS ===
    goals = [
        ("goal_millionaire", "Millionaire by 23", "$1M net worth by March 2028", 5.0),
        ("goal_dad_proud", "Dad Is Proud", "The deepest driver — everything is a letter to his father", 5.0),
        ("goal_500_accounts", "500 Hemp Accounts", "Scale route from 180 → 500", 4.0),
        ("goal_first_client", "First Lit Juris Client", "Close Kyle Soch or another PI firm", 4.0),
        ("goal_anthropic", "Join Anthropic", "6-month path: open source → community → apply", 3.0),
        ("goal_apple_gear", "$12K Apple Gear", "M5 MacBook Pro, Studio Display, etc.", 2.0),
    ]

    for gid, name, desc, weight in goals:
        graph.add_node(Node(id=gid, name=name, node_type="goal",
            description=desc, weight=weight))
        graph.add_edge(Edge("josh", gid, "drives", weight=weight))

    # Goal dependencies
    graph.add_edge(Edge("hemp_route", "goal_millionaire", "feeds_into",
        label="Cash engine", weight=5.0))
    graph.add_edge(Edge("litjuris", "goal_millionaire", "feeds_into",
        label="Scalable SaaS revenue", weight=4.0))
    graph.add_edge(Edge("goal_millionaire", "goal_dad_proud", "feeds_into",
        label="Financial proof of trajectory", weight=5.0))
    graph.add_edge(Edge("goal_first_client", "litjuris", "enables",
        label="First client validates product-market fit", weight=5.0))

    # === PSYCH PLAYBOOK TOOLS ===
    tools = [
        ("tool_ras", "RAS Priming", "Prime reticular activating system with specific daily targets"),
        ("tool_zeigarnik", "Zeigarnik Effect", "Leave tasks 90% done — brain pulls you back"),
        ("tool_loss_frame", "Loss Framing", "Frame goals as losses if you DON'T act. 2.5x motivation"),
        ("tool_ooda", "OODA Loop", "Observe→Orient→Decide→Act. Fastest cycle wins."),
        ("tool_inversion", "Inversion", "How would I guarantee failure? Then don't do those things."),
        ("tool_hormesis", "Hormesis", "Small stress doses build strength. Deliberate cognitive overload."),
    ]

    for tid, name, desc in tools:
        graph.add_node(Node(id=tid, name=name, node_type="concept",
            description=desc, weight=2.5, source_file="user_psych_playbook.md"))
        graph.add_edge(Edge("josh", tid, "uses", label="Psych tool", weight=2.0))

    # Connect psych tools to patterns they serve
    graph.add_edge(Edge("tool_ooda", "pat_gut_decision", "enables",
        label="OODA loop framework for gut decisions"))
    graph.add_edge(Edge("tool_zeigarnik", "pat_momentum", "enables",
        label="Zeigarnik pulls you back into momentum"))
    graph.add_edge(Edge("tool_hormesis", "pat_pain_output", "enables",
        label="Deliberate stress → stronger output"))
    graph.add_edge(Edge("tool_loss_frame", "val_no_exit", "enables",
        label="Loss framing makes quitting feel impossible"))


def extract_strategies(graph: IdentityGraph, memories: list[dict]):
    """Extract strategic frameworks and plans."""
    strategies = [
        ("strat_rockefeller", "Rockefeller Plan", "Hemp=cash, LitJuris=empire", "project_rockefeller_plan.md"),
        ("strat_masterplan", "8-Month Masterplan", "8 income streams, structured execution", "project_masterplan.md"),
        ("strat_exponential", "5 Compounding Loops", "Funnel, scaffold, overnight, referral, revenue", "project_exponential_systems.md"),
        ("strat_nd_os", "ND Founder's OS", "Weaponizing ADHD/dyslexia for founders", "project_nd_founders_os.md"),
        ("strat_limit_rejection", "Limit Rejection Principle", "Push past stated limits → exponential output", "user_limit_rejection.md"),
    ]

    for sid, name, desc, source in strategies:
        graph.add_node(Node(id=sid, name=name, node_type="concept",
            description=desc, weight=4.0, source_file=source))
        graph.add_edge(Edge("josh", sid, "uses", label="Strategic framework", weight=3.0))

    # Strategy connections
    graph.add_edge(Edge("strat_rockefeller", "hemp_route", "enables",
        label="Hemp = oil wells = cash engine", weight=4.0))
    graph.add_edge(Edge("strat_rockefeller", "litjuris", "enables",
        label="LitJuris = Standard Oil = empire", weight=4.0))
    graph.add_edge(Edge("strat_exponential", "strat_rockefeller", "compounds",
        label="5 loops accelerate the Rockefeller plan", weight=3.0))
    graph.add_edge(Edge("strat_limit_rejection", "pat_pain_output", "pattern_matches",
        label="Both convert resistance into output", weight=4.0))
    graph.add_edge(Edge("strat_nd_os", "pat_parallel", "instance_of",
        label="The OS codifies the parallel processing pattern", weight=3.0))


def extract_tech_stack(graph: IdentityGraph):
    """Extract technical tools and skills."""
    tech = [
        ("tech_claude_code", "Claude Code", "tool", "Primary development environment. 303 skills, 119 agents, 63 hooks.", 5.0),
        ("tech_elixir", "Elixir/Phoenix", "skill", "Greenfield backend stack", 3.0),
        ("tech_nextjs", "Next.js/TypeScript", "skill", "Frontend and existing projects", 3.0),
        ("tech_supabase", "Supabase/PostgreSQL", "tool", "Database and auth", 3.0),
        ("tech_tailwind", "Tailwind CSS", "skill", "All styling", 2.0),
        ("tech_claude_api", "Claude API", "tool", "AI reasoning for products", 3.0),
    ]

    for tid, name, ntype, desc, weight in tech:
        graph.add_node(Node(id=tid, name=name, node_type=ntype,
            description=desc, weight=weight))
        graph.add_edge(Edge("josh", tid, "uses", weight=weight))

    # Claude Code is special — it's the translation layer
    graph.add_edge(Edge("tech_claude_code", "pat_bandwidth_gap", "protects_via",
        label="AI as bandwidth expander for vision→words gap", weight=5.0,
        evidence="Brain map: Claude translates flashes into structured output"))


def extract_pipeline_contacts(graph: IdentityGraph):
    """Extract key sales pipeline contacts."""
    key_contacts = [
        ("lead_kyle", "Kyle Soch", "contact", "BillBone Law, advisor not buyer", 3.0),
        ("lead_yaffa", "Samuel Yaffa", "contact", "Yaffa Law, demo done, pilot offered", 4.0),
        ("lead_ken", "Ken (EN Injury)", "contact", "Wants 5-min demo, going stale", 3.0),
        ("lead_kapneck", "Drew Kapneck", "contact", "Callback requested, going stale", 3.0),
        ("lead_hyman", "Kelly Hyman", "contact", "Requested demo, going stale", 3.0),
    ]

    for cid, name, ntype, desc, weight in key_contacts:
        graph.add_node(Node(id=cid, name=name, node_type=ntype,
            description=desc, weight=weight))
        graph.add_edge(Edge("litjuris", cid, "targets", weight=weight))

    graph.add_edge(Edge("lead_kyle", "josh", "trusts",
        label="Advising on GTM", weight=3.0,
        evidence="Kyle said target new/independent PI firms"))


# ═══════════════════════════════════════════
# MAIN — BUILD THE GRAPH
# ═══════════════════════════════════════════

def main():
    print("=" * 60)
    print("DIGITAL TWIN — Memory Ingestion Engine")
    print("=" * 60)
    print()

    # Read all memories
    memories = read_all_memories()
    print(f"Found {len(memories)} memory files")
    print()

    # Build graph
    graph = IdentityGraph()

    print("Extracting entities...")
    extract_josh(graph)
    extract_people(graph, memories)
    extract_projects(graph, memories)
    extract_companies(graph, memories)
    extract_cognitive_model(graph, memories)
    extract_strategies(graph, memories)
    extract_tech_stack(graph)
    extract_pipeline_contacts(graph)

    print()
    print(graph.stats())
    print()

    # Find interesting paths
    print("=" * 60)
    print("CROSS-DOMAIN CONNECTIONS (the intelligence)")
    print("=" * 60)

    interesting_paths = [
        ("hemp_route", "goal_anthropic", "How hemp leads to Anthropic"),
        ("pat_pain_output", "goal_millionaire", "How pain converts to wealth"),
        ("fear_exploitation", "litjuris", "How fear shapes the business"),
        ("tool_hormesis", "tech_claude_code", "How stress training → Claude mastery"),
        ("val_no_exit", "goal_dad_proud", "How commitment → making dad proud"),
    ]

    for source, target, label in interesting_paths:
        path = graph.find_path(source, target)
        if path:
            names = [graph.nodes[nid].name for nid in path]
            print(f"\n{label}:")
            print(f"  {'→ '.join(names)}")
        else:
            print(f"\n{label}: No path found (yet)")

    # Save
    print()
    graph.save()

    # Show most connected nodes (cognitive hubs)
    print()
    print("=" * 60)
    print("COGNITIVE HUBS (most connected nodes)")
    print("=" * 60)
    for node_id, count in graph.get_most_connected(10):
        node = graph.nodes[node_id]
        print(f"  {node.name} ({node.type}): {count} connections")

    print()
    print("Done. Graph saved to ~/digital-twin/data/identity_graph.json")
    print("This is Phase 1. The graph will grow with every conversation.")


if __name__ == "__main__":
    main()
