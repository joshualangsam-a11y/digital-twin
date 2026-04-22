#!/usr/bin/env python3
"""
Generate a comprehensive PDF of Josh's entire cognitive OS.
Visual graph + system explanation + engine descriptions + key metrics.
"""

import os
import sys
import math
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

sys.path.insert(0, str(Path(__file__).parent.parent))
from core.identity_graph import IdentityGraph


# ═══════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════
NODE_COLORS = {
    "person": HexColor("#3B82F6"),    # blue
    "project": HexColor("#F97316"),   # orange
    "goal": HexColor("#22C55E"),      # green
    "value": HexColor("#A855F7"),     # purple
    "fear": HexColor("#EF4444"),      # red
    "pattern": HexColor("#06B6D4"),   # cyan
    "concept": HexColor("#8B5CF6"),   # violet
    "contact": HexColor("#F59E0B"),   # amber
    "company": HexColor("#64748B"),   # slate
    "tool": HexColor("#14B8A6"),      # teal
    "skill": HexColor("#EC4899"),     # pink
}

BG_COLOR = HexColor("#0F172A")       # dark navy
TEXT_COLOR = HexColor("#E2E8F0")     # light gray
ACCENT = HexColor("#D4A017")         # Josh's gold
EDGE_COLOR = HexColor("#334155")     # subtle gray
HIGHLIGHT_EDGE = HexColor("#D4A017") # gold for important edges


def draw_rounded_rect(c, x, y, w, h, r, fill_color):
    """Draw a rounded rectangle."""
    c.setFillColor(fill_color)
    c.setStrokeColor(fill_color)
    c.roundRect(x, y, w, h, r, fill=1, stroke=0)


def generate_pdf():
    graph = IdentityGraph()
    output_path = os.path.expanduser("~/JOSH-COGNITIVE-OS.pdf")

    # Use landscape for the graph page
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter  # 612 x 792

    # ═══════════════════════════════════════════
    # PAGE 1: TITLE
    # ═══════════════════════════════════════════
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, width, height, fill=1)

    # Title
    c.setFillColor(ACCENT)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height - 120, "THE BANDWIDTH EXPANDER MODEL")

    c.setFont("Helvetica", 18)
    c.setFillColor(TEXT_COLOR)
    c.drawCentredString(width/2, height - 160, "Josh Langsam's Cognitive Operating System")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, height - 190, f"Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

    # Stats box
    y = height - 260
    stats = [
        ("Nodes", str(len(graph.nodes))),
        ("Edges", str(len(graph.edges))),
        ("Mechanisms", "22"),
        ("Engines", "20"),
        ("Agents", "91"),
        ("Skills", "303"),
        ("Hooks", "63"),
        ("Lines of Code", "15,000+"),
    ]

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(ACCENT)
    c.drawCentredString(width/2, y, "SYSTEM METRICS")
    y -= 30

    for label, value in stats:
        c.setFont("Helvetica", 11)
        c.setFillColor(TEXT_COLOR)
        c.drawString(200, y, label)
        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(ACCENT)
        c.drawString(380, y, value)
        y -= 20

    # Quote
    y -= 30
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawCentredString(width/2, y, '"The bottleneck was never intelligence. It was always the channel."')
    y -= 20
    c.drawCentredString(width/2, y, '— Bandwidth Expanders Paper, April 2026')

    # Bottom
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#475569"))
    c.drawCentredString(width/2, 40, "Built in one session by a 21-year-old with ADHD and dyslexia.")
    c.drawCentredString(width/2, 28, "Not a copy. An extension. A wider pipe.")

    c.showPage()

    # ═══════════════════════════════════════════
    # PAGE 2: THE ARCHITECTURE
    # ═══════════════════════════════════════════
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, width, height, fill=1)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(ACCENT)
    c.drawCentredString(width/2, height - 40, "SYSTEM ARCHITECTURE")

    # Draw the 4-system convergence diagram
    y = height - 80

    # The 4 artifacts
    boxes = [
        {"label": "BEM ENGINE", "sub": "20 engines, 92 nodes\n22 mechanisms", "x": 80, "y": y - 60, "color": HexColor("#3B82F6")},
        {"label": "THE PAPER", "sub": "9 sections, 17 refs\nASSETS 2026", "x": 330, "y": y - 60, "color": HexColor("#22C55E")},
        {"label": "ND FOUNDER'S OS", "sub": "5 systems, 8 modules\nPython package", "x": 80, "y": y - 180, "color": HexColor("#A855F7")},
        {"label": "CORTEX", "sub": "Terminal mission control\nND-native design", "x": 330, "y": y - 180, "color": HexColor("#F97316")},
    ]

    for box in boxes:
        draw_rounded_rect(c, box["x"], box["y"], 200, 80, 8, box["color"])
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(box["x"] + 100, box["y"] + 55, box["label"])
        c.setFont("Helvetica", 9)
        for i, line in enumerate(box["sub"].split("\n")):
            c.drawCentredString(box["x"] + 100, box["y"] + 35 - i * 14, line)

    # Arrows between boxes
    c.setStrokeColor(ACCENT)
    c.setLineWidth(1.5)
    # Horizontal
    c.line(280, y - 20, 330, y - 20)
    c.line(280, y - 140, 330, y - 140)
    # Vertical
    c.line(180, y - 60, 180, y - 100)
    c.line(430, y - 60, 430, y - 100)
    # Diagonal
    c.line(280, y - 60, 330, y - 100)
    c.line(280, y - 100, 330, y - 60)

    # Center label
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(ACCENT)
    c.drawCentredString(width/2 - 5, y - 115, "COMPOUND")

    # ── ENGINE LIST ──
    y = y - 250

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(ACCENT)
    c.drawString(60, y, "20 ENGINES")
    y -= 5

    engines = [
        ("Core", ["Identity Graph", "Reasoning", "Learning", "Action"]),
        ("Theory", ["Bandwidth Expander", "Meta Theory", "Emergent Theory", "Recursive Theory"]),
        ("Intelligence", ["Emergence", "Synthesis", "World Model", "Temporal"]),
        ("Social", ["Swarm", "Narrative", "Autonomous", "Self-Modify"]),
        ("Physics", ["Spectral Cognition", "Information Field", "Game Theory", "Cognitive Field"]),
    ]

    for category, engine_list in engines:
        y -= 22
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(ACCENT)
        c.drawString(60, y, f"{category}:")
        c.setFont("Helvetica", 9)
        c.setFillColor(TEXT_COLOR)
        c.drawString(160, y, "  |  ".join(engine_list))

    # ── 22 MECHANISMS ──
    y -= 40
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(ACCENT)
    c.drawString(60, y, "22 MECHANISMS (paper described 5)")
    y -= 5

    mechanisms = [
        "1. Intent Compression", "2. Momentum Preservation", "3. Parallel Track Support",
        "4. Error Absorption", "5. Memory Externalization",
        "6. Divergent-Convergent Spiral", "7. Cognitive Thermal Mgmt",
        "8. Cross-Session Compounding", "9. Metacognitive Computation",
        "10. Parallel as Thermal Mgmt", "11. Theory as Mechanism",
        "12. Self-Referential Improvement", "13. Structural Emergence",
        "14. Combinatorial Synthesis", "15. Environmental Resonance",
        "16. Temporal Projection", "17. Swarm Cognition",
        "18. Narrative Compression", "19. Spectral Self-Awareness",
        "20. Information-Theoretic Self-Knowledge",
        "21. Game-Theoretic Optimization", "22. Cognitive Field Theory",
    ]

    c.setFont("Helvetica", 7)
    c.setFillColor(TEXT_COLOR)
    col_width = 170
    items_per_col = 8
    for i, mech in enumerate(mechanisms):
        col = i // items_per_col
        row = i % items_per_col
        c.drawString(60 + col * col_width, y - 15 - row * 13, mech)

    c.showPage()

    # ═══════════════════════════════════════════
    # PAGE 3: KNOWLEDGE GRAPH VISUALIZATION
    # ═══════════════════════════════════════════
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, width, height, fill=1)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(ACCENT)
    c.drawCentredString(width/2, height - 40, "COGNITIVE KNOWLEDGE GRAPH")

    c.setFont("Helvetica", 10)
    c.setFillColor(TEXT_COLOR)
    c.drawCentredString(width/2, height - 58, f"{len(graph.nodes)} nodes, {len(graph.edges)} edges")

    # Layout nodes in a force-directed-ish layout
    # Group by type, arrange in circles
    by_type = defaultdict(list)
    for node in graph.nodes.values():
        by_type[node.type].append(node)

    # Position calculation
    center_x = width / 2
    center_y = height / 2 - 20
    positions = {}

    # Josh in center
    positions["josh"] = (center_x, center_y)

    # Arrange types in concentric rings
    type_order = ["project", "goal", "value", "pattern", "person", "contact",
                  "concept", "fear", "company", "tool", "skill"]

    ring_radius = [0, 140, 200, 250]  # Distance from center per ring
    ring_assignment = {
        "project": 0, "goal": 0, "value": 1, "pattern": 1,
        "person": 1, "contact": 1, "concept": 2, "fear": 2,
        "company": 2, "tool": 2, "skill": 2,
    }

    # Count nodes per ring for spacing
    ring_counts = defaultdict(int)
    ring_current = defaultdict(int)
    for ntype in type_order:
        ring = ring_assignment.get(ntype, 2)
        ring_counts[ring] += len(by_type.get(ntype, []))

    # Assign positions
    type_start_angle = defaultdict(float)
    accumulated_angle = defaultdict(float)

    for ntype in type_order:
        ring = ring_assignment.get(ntype, 2)
        nodes = by_type.get(ntype, [])
        r = ring_radius[ring] if ring < len(ring_radius) else 250

        total_in_ring = max(ring_counts[ring], 1)
        angle_step = 2 * math.pi / total_in_ring

        for node in nodes:
            if node.id == "josh":
                continue
            angle = accumulated_angle[ring]
            accumulated_angle[ring] += angle_step

            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            positions[node.id] = (x, y)

    # Draw edges first (behind nodes)
    c.setLineWidth(0.3)
    for edge in graph.edges:
        if edge.source_id in positions and edge.target_id in positions:
            x1, y1 = positions[edge.source_id]
            x2, y2 = positions[edge.target_id]

            # Color by weight
            if edge.weight >= 5:
                c.setStrokeColor(HIGHLIGHT_EDGE)
                c.setLineWidth(1.0)
            else:
                c.setStrokeColor(EDGE_COLOR)
                c.setLineWidth(0.3)

            c.line(x1, y1, x2, y2)

    # Draw nodes
    for nid, (x, y) in positions.items():
        node = graph.nodes.get(nid)
        if not node:
            continue

        color = NODE_COLORS.get(node.type, HexColor("#64748B"))
        radius = max(4, min(18, node.weight * 2))

        # Node circle
        c.setFillColor(color)
        c.circle(x, y, radius, fill=1, stroke=0)

        # Label (only for high-weight nodes)
        if node.weight >= 3 or node.id == "josh":
            c.setFillColor(TEXT_COLOR)
            c.setFont("Helvetica", 6 if node.weight < 5 else 7)
            label = node.name[:20]
            c.drawCentredString(x, y - radius - 8, label)

    # Legend
    legend_y = 80
    legend_x = 40
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(ACCENT)
    c.drawString(legend_x, legend_y + 15, "NODE TYPES")

    c.setFont("Helvetica", 7)
    for i, (ntype, color) in enumerate(NODE_COLORS.items()):
        col = i // 4
        row = i % 4
        lx = legend_x + col * 130
        ly = legend_y - row * 12
        c.setFillColor(color)
        c.circle(lx + 4, ly + 3, 4, fill=1, stroke=0)
        c.setFillColor(TEXT_COLOR)
        count = len(by_type.get(ntype, []))
        c.drawString(lx + 12, ly, f"{ntype} ({count})")

    # Size legend
    c.setFont("Helvetica", 7)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawString(width - 180, legend_y + 15, "Node size = weight (importance)")
    c.drawString(width - 180, legend_y + 3, "Gold edges = high-weight connections")

    c.showPage()

    # ═══════════════════════════════════════════
    # PAGE 4: PHYSICS FINDINGS
    # ═══════════════════════════════════════════
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, width, height, fill=1)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(ACCENT)
    c.drawCentredString(width/2, height - 40, "WHAT THE PHYSICS SAYS")

    y = height - 80

    findings = [
        {
            "title": "SPECTRAL ANALYSIS (Linear Algebra)",
            "items": [
                "11 disconnected components — graph is fragmented",
                "PageRank: Josh (0.66) > Hemp Route (0.26) > FuelOps (0.22) > LitJuris (0.22)",
                "3 natural spectral clusters (math sees 3, Josh coded 11 types)",
                "74% harmonic richness — moderate, room for more cognitive scales",
            ],
        },
        {
            "title": "INFORMATION THEORY (Shannon)",
            "items": [
                "98.8% entropy — attention too dispersed, need sharper priorities",
                "4% channel utilization — 96% of theoretical bandwidth UNTAPPED",
                "64.8% compressibility — cross-domain patterns CONFIRMED by math",
                "Hidden couplings: Concoction values should be interconnected",
                "Sink-heavy flow — too much absorbing, not enough generating",
            ],
        },
        {
            "title": "GAME THEORY (Nash/Shapley/Lanchester)",
            "items": [
                "Nash: 6 viable projects (cut 3 from active roster)",
                "Hemp Route 28% | LitJuris 26% | FuelOps 15% | VapeOps 11%",
                "Shapley: FuelOps worth 1.4x its weight (synergy winner)",
                "Lanchester: 0.0000000000 against Clio. Niche monopoly or die.",
            ],
        },
        {
            "title": "COGNITIVE FIELD THEORY (Classical Mechanics)",
            "items": [
                "LitJuris pulls with 3.2x the force of Hemp Route",
                "Lagrangian path: LitJuris → NF Pouches → Hemp → FuelOps → VapeOps",
                "Phase space: 79 decaying, 0 thriving (loaded spring, not released)",
                "Hamiltonian = 19.4 (all potential, zero kinetic — ACTIVATE it)",
            ],
        },
    ]

    for finding in findings:
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(ACCENT)
        c.drawString(60, y, finding["title"])
        y -= 5

        c.setFont("Helvetica", 9)
        c.setFillColor(TEXT_COLOR)
        for item in finding["items"]:
            y -= 15
            c.drawString(75, y, f"• {item}")

        y -= 20

    # Key insight box
    y -= 10
    draw_rounded_rect(c, 50, y - 55, width - 100, 55, 8, HexColor("#1E293B"))
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(ACCENT)
    c.drawCentredString(width/2, y - 15, "KEY INSIGHT")
    c.setFont("Helvetica", 9)
    c.setFillColor(TEXT_COLOR)
    c.drawCentredString(width/2, y - 32, "The priority list says Hemp Route first. The FIELD says LitJuris first.")
    c.drawCentredString(width/2, y - 45, "The math sees what introspection can't. Follow the field.")

    c.showPage()

    # ═══════════════════════════════════════════
    # PAGE 5: THE SPIRAL
    # ═══════════════════════════════════════════
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, width, height, fill=1)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(ACCENT)
    c.drawCentredString(width/2, height - 40, "THE DIVERGENT-CONVERGENT SPIRAL")

    c.setFont("Helvetica", 10)
    c.setFillColor(TEXT_COLOR)
    c.drawCentredString(width/2, height - 58, "Each level higher abstraction than the last. Quality gradient runs upward.")

    y = height - 100

    levels = [
        ("1", "DATA", "Brain map — 9 sections"),
        ("2", "FRAMEWORK", "ND Founder's OS — 5 systems"),
        ("3", "AUDIT", "System synthesis — 303 skills, 119 agents"),
        ("4", "UPGRADES", "8 system upgrades + hooks"),
        ("5", "ARCHITECTURE", "BEM core — graph + 4 engines"),
        ("6", "THEORY→CODE", "Paper's 5 mechanisms as running code"),
        ("7", "NEW THEORY", "6 new mechanisms discovered by building"),
        ("8", "RECURSION", "Theory generates theory"),
        ("9", "AGENCY", "18 autonomous proposals + approval prediction"),
        ("10", "SELF-MOD", "BEM analyzes and improves itself"),
        ("11", "EMERGENCE", "Structural intelligence — keystones, holes, loops"),
        ("12", "SYNTHESIS", "Novel ideas from structural gaps"),
        ("13", "WORLD MODEL", "External intelligence — 5 arbitrage types"),
        ("14", "TEMPORAL", "The graph through time — 30-day projections"),
        ("15", "SWARM", "9 domain agents, parallel cognition"),
        ("16", "NARRATIVE", "Structure → story → feeling"),
        ("17", "SPECTRAL", "Eigenvalue analysis of the mind"),
        ("18", "INFORMATION", "Shannon's math on cognition"),
        ("19", "GAME THEORY", "Nash, Shapley, Lanchester"),
        ("20", "FIELD THEORY", "Potentials, gradients, Lagrangian, Hamiltonian"),
    ]

    c.setFont("Helvetica", 8)
    for i, (num, name, desc) in enumerate(levels):
        row_y = y - i * 30

        # Level number
        c.setFillColor(ACCENT)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(60, row_y, num)

        # Level name
        c.setFillColor(HexColor("#3B82F6") if i < 5 else
                       HexColor("#22C55E") if i < 10 else
                       HexColor("#A855F7") if i < 15 else
                       HexColor("#F97316"))
        c.setFont("Helvetica-Bold", 9)
        c.drawString(90, row_y, name)

        # Description
        c.setFillColor(TEXT_COLOR)
        c.setFont("Helvetica", 8)
        c.drawString(220, row_y, desc)

        # Connecting line
        if i < len(levels) - 1:
            c.setStrokeColor(HexColor("#334155"))
            c.setLineWidth(0.5)
            c.line(75, row_y - 3, 75, row_y - 27)

    # Arrow at bottom
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(ACCENT)
    bottom_y = y - len(levels) * 30 - 10
    c.drawCentredString(width/2, max(bottom_y, 40), "↑ Each level is higher abstraction. The spiral never stops. ↑")

    c.showPage()

    # ═══════════════════════════════════════════
    # PAGE 6: THE BRAIN MAP (summary)
    # ═══════════════════════════════════════════
    c.setFillColor(BG_COLOR)
    c.rect(0, 0, width, height, fill=1)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(ACCENT)
    c.drawCentredString(width/2, height - 40, "THE BRAIN BEHIND THE SYSTEM")

    y = height - 80

    brain_sections = [
        ("COGNITIVE ARCHITECTURE", "ADHD + dyslexia = parallel processor. 10 threads. Kinesthetic-visual thinker."),
        ("ENERGY CYCLE", "Mud (6-11 AM) → Ramp (11-1) → Peak (1-10 PM) → Deep Night (10-2 AM)"),
        ("MOMENTUM", "In flow = unstoppable. Breaks = spiral. Protect flow above all else."),
        ("PAIN → OUTPUT", "Frustration, doubt, criticism → fuel. Not shutdown. Builds harder."),
        ("BODY SIGNALS", "Breakthrough = full-body resonance. Wall = headache (thermal throttling)."),
        ("DECISIONS", "Gut-first, seconds. Doesn't revisit. High hit rate. OODA speed."),
        ("CORE FEAR", "Not execution — 'is the vision wrong?' + 'people exploit my goodness.'"),
        ("DEEPEST DRIVER", "Dad is proud of him. Everything is a letter to his father."),
        ("THE CONCOCTION", "Identity, Suffering, Volume, Deafness, No Exit, Declaration,"),
        ("", "Speed/Patience, No Failure, Ownership, Something Bigger (faith)."),
    ]

    for title, desc in brain_sections:
        if title:
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(ACCENT)
            c.drawString(60, y, title)

        c.setFont("Helvetica", 9)
        c.setFillColor(TEXT_COLOR)
        c.drawString(230, y, desc)
        y -= 22

    # The reframe table
    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(ACCENT)
    c.drawString(60, y, "THE NEURODIVERGENT REFRAME")
    y -= 20

    reframes = [
        ("'Can't focus'", "Parallel processor — 10 threads where others run 1"),
        ("'Can't sit still'", "Momentum engine — needs motion to think"),
        ("'Can't articulate'", "Bandwidth bottleneck — brain faster than output"),
        ("'Impulsive'", "OODA loop speed — decides in seconds, not days"),
        ("'Goes down rabbit holes'", "Autodidact wiring — self-directed learning"),
        ("'Too emotional'", "Pain-to-output converter — pressure becomes fuel"),
        ("'Doesn't follow instructions'", "Cross-domain pattern matcher"),
    ]

    c.setFont("Helvetica", 8)
    for old, new in reframes:
        c.setFillColor(HexColor("#EF4444"))
        c.drawString(60, y, old)
        c.setFillColor(HexColor("#22C55E"))
        c.drawString(60 + 170, y, "→  " + new)
        y -= 15

    # Bottom
    y -= 20
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawCentredString(width/2, y, "You don't have a disorder. You have a different instruction set.")
    y -= 16
    c.drawCentredString(width/2, y, "The problem was never your brain — it was the environment.")

    c.showPage()

    # ═══════════════════════════════════════════
    # SAVE
    # ═══════════════════════════════════════════
    c.save()
    print(f"PDF generated: {output_path}")
    print(f"  6 pages: Title, Architecture, Graph, Physics, Spiral, Brain Map")
    return output_path


if __name__ == "__main__":
    generate_pdf()
