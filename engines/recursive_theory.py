"""
RECURSIVE THEORY ENGINE — Theory-Building as Bandwidth Mechanism

Based on BEM Mechanism 11: Theory-Building is Itself Bandwidth Expansion

The meta-insight: Building theory about bandwidth generates new bandwidth.
As we implement the engines, patterns emerge the paper couldn't predict.

This engine:
1. Watches all other engines for emergent patterns
2. Crystallizes patterns into testable theories
3. Connects theories back to code (theory → code → new theory)
4. Tracks the divergent-convergent spiral (discovery #1)
5. Generates academic-format papers suitable for publication

The twin helps you think about thinking. This engine helps you think about
how you build systems that help you think about thinking.
It's metacognition made computational.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


class RecursiveTheory:
    """
    Watches the twin's engines for patterns.
    When patterns crystallize into theory, records them.
    Connects theory to code, and new insights back to theory.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.theory_log = self.data_dir / "recursive_theories.jsonl"
        self.spiral_log = self.data_dir / "divergent_convergent_spiral.jsonl"
        self.papers_dir = self.data_dir / "theory_papers"
        self.papers_dir.mkdir(exist_ok=True)

        # Theory tracking
        self.active_theories: dict[str, dict] = {}
        self.spiral_level = 0  # How many diverge-converge cycles?

    # ═══════════════════════════════════════════
    # THEORY OBSERVATION & CRYSTALLIZATION
    # ═══════════════════════════════════════════

    def observe_pattern(self, source: str, pattern_name: str, evidence: list[str],
                       confidence: float = 0.5) -> dict:
        """
        Observe a pattern emerging from engine outputs.

        source: which engine? ("reasoning" | "learning" | "action" | "bandwidth" | "domain_router" | "session_bridge")
        pattern_name: human-readable name
        evidence: list of specific observations
        confidence: 0-1, how sure are we this is a real pattern?
        """
        now = datetime.now(timezone.utc)
        pattern_id = f"pattern_{source}_{pattern_name.lower().replace(' ', '_')[:30]}"

        entry = {
            "timestamp": now.isoformat(),
            "pattern_id": pattern_id,
            "source_engine": source,
            "pattern_name": pattern_name,
            "evidence": evidence,
            "confidence": confidence,
            "status": "observed",
        }

        # Store pattern for tracking
        if pattern_id not in self.active_theories:
            self.active_theories[pattern_id] = {
                "name": pattern_name,
                "source": source,
                "evidence": [],
                "confidence": confidence,
                "observations": 1,
                "crystallized": False,
            }
        else:
            # Accumulate evidence
            theory = self.active_theories[pattern_id]
            theory["evidence"].extend(evidence)
            theory["observations"] += 1
            # Increase confidence with each observation
            theory["confidence"] = min(1.0, theory["confidence"] + 0.1)

        self._append_log(self.theory_log, entry)

        return {
            "pattern_id": pattern_id,
            "observations": self.active_theories[pattern_id]["observations"],
            "confidence": self.active_theories[pattern_id]["confidence"],
            "status": "observing",
        }

    def crystallize_theory(self, pattern_id: str, name: str, description: str,
                          implication: str, novel_mechanism: bool = False) -> dict:
        """
        A pattern has been observed enough times. Crystallize it into theory.

        When confidence is high enough (> 0.7), we elevate observation to theory.
        """
        if pattern_id not in self.active_theories:
            return {"error": f"Unknown pattern: {pattern_id}"}

        theory = self.active_theories[pattern_id]
        if theory["confidence"] < 0.7:
            return {
                "error": f"Confidence too low ({theory['confidence']:.2f}). Need > 0.7",
                "pattern_id": pattern_id,
            }

        now = datetime.now(timezone.utc)

        # Add to graph as a concept
        theory_node_id = f"theory_{name.lower().replace(' ', '_')[:40]}"
        theory_node = Node(
            id=theory_node_id,
            name=name,
            node_type="concept",
            description=description,
            weight=3.5 if novel_mechanism else 2.5,
            metadata={
                "theory_type": "mechanism" if novel_mechanism else "pattern",
                "source_engine": theory["source"],
                "observations": theory["observations"],
                "confidence": theory["confidence"],
                "crystallized_at": now.isoformat(),
            },
        )
        self.graph.add_node(theory_node)

        # Connect to source engine (conceptually)
        engine_node_id = f"engine_{theory['source']}"
        if engine_node_id not in self.graph.nodes:
            engine_node = Node(
                id=engine_node_id,
                name=f"Engine: {theory['source']}",
                node_type="tool",
                weight=2.0,
            )
            self.graph.add_node(engine_node)

        edge = Edge(
            source_id=engine_node_id,
            target_id=theory_node_id,
            edge_type="generates",
            label="discovered",
            weight=2.0,
            evidence=f"Theory crystallized from {theory['observations']} observations",
        )
        self.graph.add_edge(edge)

        # Mark as crystallized
        self.active_theories[pattern_id]["crystallized"] = True

        entry = {
            "timestamp": now.isoformat(),
            "event": "theory_crystallized",
            "pattern_id": pattern_id,
            "theory_node_id": theory_node_id,
            "name": name,
            "novel_mechanism": novel_mechanism,
            "observations_accumulated": theory["observations"],
            "confidence": theory["confidence"],
        }
        self._append_log(self.theory_log, entry)

        self.graph.save()

        return {
            "theory_id": theory_node_id,
            "name": name,
            "status": "crystallized",
            "novel_mechanism": novel_mechanism,
            "observations_accumulated": theory["observations"],
        }

    # ═══════════════════════════════════════════
    # DIVERGENT-CONVERGENT SPIRAL (Discovery #1)
    # ═══════════════════════════════════════════

    def record_spiral_iteration(self, phase: str, output: str, abstraction_level: int,
                               back_to_code: bool = False) -> dict:
        """
        Record one iteration of the divergent-convergent spiral.

        phase: "diverge" | "converge"
        abstraction_level: 0 (code) → 1 (patterns) → 2 (frameworks) → 3+ (meta-theory)
        back_to_code: did we go back to implementation?

        The spiral is: Brain map (data) → ND OS (framework) → Audit (synthesis) →
        Digital twin (arch) → Bandwidth engine (theory-as-code) →
        Meta-theory engine (theory-about-theory).
        Each is higher abstraction.
        """
        now = datetime.now(timezone.utc)
        self.spiral_level += 1

        entry = {
            "timestamp": now.isoformat(),
            "spiral_iteration": self.spiral_level,
            "phase": phase,
            "abstraction_level": abstraction_level,
            "output": output[:200],  # First 200 chars
            "back_to_code": back_to_code,
        }
        self._append_log(self.spiral_log, entry)

        if back_to_code:
            return {
                "spiral_iteration": self.spiral_level,
                "status": "back_to_implementation",
                "implication": "New theory is feeding back into code. The spiral is compounding.",
            }
        else:
            return {
                "spiral_iteration": self.spiral_level,
                "phase": phase,
                "abstraction_level": abstraction_level,
                "status": "spiraling",
            }

    # ═══════════════════════════════════════════
    # THEORY-TO-CODE LINKING
    # ═══════════════════════════════════════════

    def link_theory_to_code(self, theory_node_id: str, file_path: str,
                           function_name: str = "", line_numbers: tuple = None) -> dict:
        """
        Connect a theory to the code that implements it.

        This is the key insight: theory doesn't stay abstract.
        It immediately becomes code, which generates new theory.
        """
        if theory_node_id not in self.graph.nodes:
            return {"error": f"Unknown theory: {theory_node_id}"}

        now = datetime.now(timezone.utc)

        # Create or get code node
        code_node_id = f"code_{file_path.split('/')[-1].replace('.py', '')}_{function_name}"
        if code_node_id not in self.graph.nodes:
            code_node = Node(
                id=code_node_id,
                name=f"Code: {function_name or file_path.split('/')[-1]}",
                node_type="tool",
                description=f"File: {file_path}",
                weight=2.0,
                metadata={
                    "file_path": file_path,
                    "function_name": function_name,
                    "line_numbers": line_numbers,
                },
            )
            self.graph.add_node(code_node)

        # Link theory → code
        edge = Edge(
            source_id=theory_node_id,
            target_id=code_node_id,
            edge_type="implemented_as",
            weight=2.0,
            evidence=f"Theory implemented in {function_name or file_path}",
        )
        self.graph.add_edge(edge)

        entry = {
            "timestamp": now.isoformat(),
            "event": "theory_linked_to_code",
            "theory_id": theory_node_id,
            "code_id": code_node_id,
            "file_path": file_path,
            "function_name": function_name,
        }
        self._append_log(self.theory_log, entry)

        self.graph.save()

        return {
            "theory_id": theory_node_id,
            "code_id": code_node_id,
            "linked": True,
            "status": "theory_→_code_feedback_loop_established",
        }

    # ═══════════════════════════════════════════
    # ACADEMIC PAPER GENERATION
    # ═══════════════════════════════════════════

    def generate_paper(self, title: str, theories: list[str],
                      abstract: str = "") -> dict:
        """
        Generate an academic-style paper from crystallized theories.

        Suitable for publication describing the twin's discoveries.
        """
        now = datetime.now(timezone.utc)
        paper_id = f"paper_{now.strftime('%Y%m%d_%H%M%S')}"

        # Collect theory details
        included = []
        for theory_id in theories:
            if theory_id in self.graph.nodes:
                node = self.graph.nodes[theory_id]
                included.append({
                    "name": node.name,
                    "description": node.description,
                    "metadata": node.metadata,
                })

        # Build paper structure
        paper = {
            "id": paper_id,
            "title": title,
            "abstract": abstract,
            "generated_at": now.isoformat(),
            "theories": included,
            "sections": [
                {
                    "heading": "Introduction",
                    "content": "This paper documents theoretical discoveries made during implementation of a cognitive architecture for ADHD neurotypes.",
                },
                {
                    "heading": "Methods",
                    "content": "We built a digital twin with engines for reasoning, learning, action, and bandwidth expansion. Each implementation revealed emergent patterns not predicted by theory.",
                },
                {
                    "heading": "Discoveries",
                    "subsections": [
                        {
                            "theory": t["name"],
                            "content": t["description"],
                        }
                        for t in included
                    ],
                },
                {
                    "heading": "Implications",
                    "content": "Building computational models of cognition isn't just engineering — it's discovery. The act of formalization reveals structure the brain couldn't see in itself.",
                },
            ],
        }

        # Save paper
        paper_file = self.papers_dir / f"{paper_id}.json"
        with open(paper_file, "w") as f:
            json.dump(paper, f, indent=2)

        # Generate markdown version too
        md_file = self.papers_dir / f"{paper_id}.md"
        md_content = self._paper_to_markdown(paper)
        with open(md_file, "w") as f:
            f.write(md_content)

        entry = {
            "timestamp": now.isoformat(),
            "event": "paper_generated",
            "paper_id": paper_id,
            "title": title,
            "theories_included": len(included),
            "file_path": str(paper_file),
        }
        self._append_log(self.theory_log, entry)

        return {
            "paper_id": paper_id,
            "title": title,
            "theories_included": len(included),
            "file_json": str(paper_file),
            "file_markdown": str(md_file),
            "status": "generated",
        }

    def _paper_to_markdown(self, paper: dict) -> str:
        """Convert paper JSON to markdown."""
        lines = [
            f"# {paper['title']}",
            f"\n*Generated {paper['generated_at']}*\n",
        ]

        if paper.get("abstract"):
            lines.append(f"## Abstract\n{paper['abstract']}\n")

        for section in paper.get("sections", []):
            lines.append(f"## {section['heading']}\n")
            if section.get('content'):
                lines.append(f"{section['content']}\n")

            if "subsections" in section:
                for sub in section["subsections"]:
                    lines.append(f"### {sub.get('theory', 'Untitled')}\n")
                    if sub.get('content'):
                        lines.append(f"{sub['content']}\n")

        return "\n".join(lines)

    # ═══════════════════════════════════════════
    # UTILITIES
    # ═══════════════════════════════════════════

    def _append_log(self, log_file: Path, entry: dict):
        """Append to log file."""
        with open(log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_active_theories(self) -> dict:
        """All currently-tracking patterns/theories."""
        return {
            theory_id: {
                "name": theory["name"],
                "source": theory["source"],
                "observations": theory["observations"],
                "confidence": theory["confidence"],
                "crystallized": theory["crystallized"],
            }
            for theory_id, theory in self.active_theories.items()
        }

    def stats(self) -> dict:
        """Statistics on theory building."""
        return {
            "total_theories": len(self.graph.nodes) if self.graph else 0,
            "active_patterns": len(self.active_theories),
            "crystallized_theories": sum(
                1 for t in self.active_theories.values() if t["crystallized"]
            ),
            "spiral_iterations": self.spiral_level,
            "papers_generated": len(list(self.papers_dir.glob("*.md"))),
        }
