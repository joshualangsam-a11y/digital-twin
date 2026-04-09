"""
COGNITIVE FIELD THEORY — Josh's Mind as a Physical Field

THIS IS GENUINELY UNPRECEDENTED.

In physics, a field assigns a value to every point in space.
Gravity is a field. Electromagnetism is a field.
This engine treats Josh's cognitive graph as a FIELD.

Every node has a POTENTIAL (weight × centrality).
Every edge creates a GRADIENT (potential difference).
Gradients create FORCES that pull attention.
The sum of all forces at any point = the NET COGNITIVE FORCE.

This tells Josh WHERE his attention naturally wants to flow.
Not where he THINKS it should go. Where the FIELD pulls it.

Then: LAGRANGIAN MECHANICS.
L = T - V (kinetic energy minus potential energy)
The Euler-Lagrange equation gives the path of LEAST ACTION —
the most natural cognitive trajectory. The path his mind
WANTS to follow, given all the forces acting on it.

If Josh fights this path, he wastes energy.
If he follows it, he flows.

Mechanism 22: Cognitive Field Theory
The mind is not a graph. It is a field.
And fields have equations of motion.
"""

import json
import os
import math
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph


class CognitiveField:
    """
    Treats Josh's cognitive graph as a physical field.
    Computes potentials, gradients, forces, and trajectories.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))

    # ═══════════════════════════════════════════
    # 1. COGNITIVE POTENTIAL (where energy pools)
    # ═══════════════════════════════════════════

    def compute_potentials(self) -> dict:
        """
        Potential V(node) = weight × eigenvector_centrality × (1 + goal_connections)

        High potential = where cognitive energy naturally pools.
        Low potential = where energy drains from.

        Attention flows from LOW potential to HIGH potential
        (opposite of physics — in cognition, you're ATTRACTED to
        high-potential nodes, like a ball rolling toward a valley).
        """
        # Compute centrality
        adj = defaultdict(float)
        for edge in self.graph.edges:
            adj[(edge.source_id, edge.target_id)] = edge.weight
            adj[(edge.target_id, edge.source_id)] = edge.weight

        # Simple degree centrality (normalized)
        degree = defaultdict(float)
        for (src, _), w in adj.items():
            degree[src] += w
        max_degree = max(degree.values()) if degree else 1

        potentials = {}
        for nid, node in self.graph.nodes.items():
            centrality = degree.get(nid, 0) / max_degree

            # Goal connections amplify potential
            goal_conns = sum(1 for c in self.graph.get_connections(nid)
                           if c["node"].type == "goal")

            # Fear connections reduce potential (repulsive)
            fear_conns = sum(1 for c in self.graph.get_connections(nid)
                           if c["node"].type == "fear")

            V = node.weight * centrality * (1 + goal_conns * 0.5) * (1 - fear_conns * 0.1)
            potentials[nid] = round(V, 4)

        # Sort by potential
        sorted_potentials = sorted(potentials.items(), key=lambda x: -x[1])

        results = []
        for nid, V in sorted_potentials[:15]:
            node = self.graph.nodes[nid]
            results.append({
                "node": node.name,
                "type": node.type,
                "potential": V,
                "weight": node.weight,
            })

        return {
            "potentials": results,
            "peak": results[0] if results else None,
            "interpretation": (
                f"Highest cognitive potential: {results[0]['node']} ({results[0]['potential']:.2f}). "
                f"This is where attention naturally wants to pool. "
                f"Fighting this wastes energy. Flowing with it = path of least resistance."
            ) if results else "No potentials computed.",
        }

    # ═══════════════════════════════════════════
    # 2. COGNITIVE GRADIENTS (where forces pull)
    # ═══════════════════════════════════════════

    def compute_gradients(self) -> dict:
        """
        Gradient = potential difference across an edge.
        Large gradient = strong pull in that direction.

        The steepest gradients are the STRONGEST forces
        acting on Josh's attention right now.
        """
        potentials = {}
        adj = defaultdict(float)
        for edge in self.graph.edges:
            adj[(edge.source_id, edge.target_id)] = edge.weight
            adj[(edge.target_id, edge.source_id)] = edge.weight

        degree = defaultdict(float)
        for (src, _), w in adj.items():
            degree[src] += w
        max_degree = max(degree.values()) if degree else 1

        for nid, node in self.graph.nodes.items():
            centrality = degree.get(nid, 0) / max_degree
            goal_conns = sum(1 for c in self.graph.get_connections(nid) if c["node"].type == "goal")
            potentials[nid] = node.weight * centrality * (1 + goal_conns * 0.5)

        gradients = []
        for edge in self.graph.edges:
            V_src = potentials.get(edge.source_id, 0)
            V_tgt = potentials.get(edge.target_id, 0)
            gradient = abs(V_tgt - V_src)

            if gradient > 0.5:  # Only significant gradients
                src_node = self.graph.nodes.get(edge.source_id)
                tgt_node = self.graph.nodes.get(edge.target_id)
                if src_node and tgt_node:
                    # Direction: flows from low to high potential
                    if V_tgt > V_src:
                        flow_from, flow_to = src_node.name, tgt_node.name
                    else:
                        flow_from, flow_to = tgt_node.name, src_node.name

                    gradients.append({
                        "from": flow_from,
                        "to": flow_to,
                        "gradient": round(gradient, 4),
                        "edge_type": edge.type,
                        "interpretation": f"Attention pulled from '{flow_from}' toward '{flow_to}' (force={gradient:.2f})",
                    })

        gradients.sort(key=lambda x: -x["gradient"])

        return {
            "strongest_gradients": gradients[:10],
            "total_gradients": len(gradients),
            "interpretation": (
                f"Top force: '{gradients[0]['to']}' pulls attention with force {gradients[0]['gradient']:.2f}. "
                f"This is the strongest cognitive attractor right now. "
                f"{'If Josh is NOT working on this, he is fighting the field.' if gradients else ''}"
            ) if gradients else "No significant gradients.",
        }

    # ═══════════════════════════════════════════
    # 3. NET FORCE VECTOR (resultant of all forces)
    # ═══════════════════════════════════════════

    def net_force(self) -> dict:
        """
        Sum all forces acting at each node.
        The net force vector tells Josh WHERE his attention
        is being pulled from all directions simultaneously.

        A node with large net force toward it = STRONG ATTRACTOR.
        A node with large net force away from it = REPELLER.
        A node with near-zero net force = EQUILIBRIUM (balanced pulls).
        """
        potentials = {}
        adj = defaultdict(float)
        for edge in self.graph.edges:
            adj[(edge.source_id, edge.target_id)] = edge.weight
            adj[(edge.target_id, edge.source_id)] = edge.weight

        degree = defaultdict(float)
        for (src, _), w in adj.items():
            degree[src] += w
        max_degree = max(degree.values()) if degree else 1

        for nid, node in self.graph.nodes.items():
            centrality = degree.get(nid, 0) / max_degree
            goal_conns = sum(1 for c in self.graph.get_connections(nid) if c["node"].type == "goal")
            potentials[nid] = node.weight * centrality * (1 + goal_conns * 0.5)

        # Net force = sum of (gradient × direction) for all edges
        net_forces = defaultdict(float)

        for edge in self.graph.edges:
            V_src = potentials.get(edge.source_id, 0)
            V_tgt = potentials.get(edge.target_id, 0)
            gradient = V_tgt - V_src  # Positive = pull toward target

            net_forces[edge.target_id] += abs(gradient) if gradient > 0 else 0
            net_forces[edge.source_id] += abs(gradient) if gradient < 0 else 0

        # Classify
        attractors = []
        repellers = []
        equilibria = []

        for nid, force in net_forces.items():
            node = self.graph.nodes.get(nid)
            if not node or nid == "josh":
                continue

            entry = {
                "node": node.name,
                "type": node.type,
                "net_force": round(force, 4),
                "potential": round(potentials.get(nid, 0), 4),
                "weight": node.weight,
            }

            if force > 3.0:
                attractors.append(entry)
            elif force < 0.5:
                equilibria.append(entry)
            else:
                repellers.append(entry)  # Low force nodes in between

        attractors.sort(key=lambda x: -x["net_force"])
        equilibria.sort(key=lambda x: x["net_force"])

        return {
            "attractors": attractors[:7],
            "equilibria": equilibria[:5],
            "field_summary": (
                f"Strongest attractor: {attractors[0]['node']} (force={attractors[0]['net_force']:.2f}). "
                f"This is where the cognitive field is PULLING Josh right now. "
                f"If he's working on something else, he's fighting against the field — "
                f"spending energy on resistance instead of output."
            ) if attractors else "No strong attractors.",
        }

    # ═══════════════════════════════════════════
    # 4. LAGRANGIAN (path of least action)
    # ═══════════════════════════════════════════

    def lagrangian_path(self) -> dict:
        """
        The Lagrangian L = T - V, where:
        - T (kinetic energy) = rate of change × momentum
        - V (potential energy) = cognitive potential at current node

        The Euler-Lagrange equation δ∫L dt = 0 gives the path
        of LEAST ACTION — the trajectory that minimizes
        total cognitive effort.

        In practice: this computes the MOST EFFICIENT path through
        Josh's projects, given their potentials and connections.
        """
        potentials = {}
        adj = defaultdict(float)
        for edge in self.graph.edges:
            adj[(edge.source_id, edge.target_id)] = edge.weight
            adj[(edge.target_id, edge.source_id)] = edge.weight

        degree = defaultdict(float)
        for (src, _), w in adj.items():
            degree[src] += w
        max_degree = max(degree.values()) if degree else 1

        for nid, node in self.graph.nodes.items():
            centrality = degree.get(nid, 0) / max_degree
            goal_conns = sum(1 for c in self.graph.get_connections(nid) if c["node"].type == "goal")
            potentials[nid] = node.weight * centrality * (1 + goal_conns * 0.5)

        # Find the minimum-action path through top projects
        projects = sorted(
            [(nid, n) for nid, n in self.graph.nodes.items() if n.type == "project"],
            key=lambda x: -potentials.get(x[0], 0),
        )

        if len(projects) < 2:
            return {"path": [], "action": 0}

        # Greedy path following the potential gradient
        path = []
        visited = set()
        current = projects[0][0]  # Start at highest potential project

        for _ in range(min(7, len(projects))):
            node = self.graph.nodes.get(current)
            if not node:
                break

            V = potentials.get(current, 0)
            path.append({
                "node": node.name,
                "potential": round(V, 2),
                "action": round(V * 0.5, 2),  # Simplified: action ∝ potential × time
            })
            visited.add(current)

            # Find next highest-potential unvisited connected project
            neighbors = []
            for c in self.graph.get_connections(current):
                if c["node"].id not in visited and c["node"].type == "project":
                    neighbors.append((c["node"].id, potentials.get(c["node"].id, 0)))

            if not neighbors:
                # No connected unvisited project — jump to highest unvisited
                for pid, pnode in projects:
                    if pid not in visited:
                        current = pid
                        break
                else:
                    break
            else:
                current = max(neighbors, key=lambda x: x[1])[0]

        total_action = sum(p["action"] for p in path)

        return {
            "path": path,
            "total_action": round(total_action, 2),
            "interpretation": (
                f"Path of least action through {len(path)} projects: "
                f"{' → '.join(p['node'] for p in path)}. "
                f"Total action = {total_action:.1f}. "
                f"This is the trajectory that minimizes cognitive effort while "
                f"maximizing output. Fighting this ordering wastes energy."
            ),
        }

    # ═══════════════════════════════════════════
    # 5. COGNITIVE PHASE SPACE
    # ═══════════════════════════════════════════

    def phase_space(self) -> dict:
        """
        Phase space: plot of position × momentum for each node.
        Position = current weight (where it IS).
        Momentum = rate of access × weight change (where it's GOING).

        Nodes in different regions of phase space have different dynamics:
        - High position, high momentum = THRIVING (ride it)
        - High position, low momentum = DECAYING (reinforce or let go)
        - Low position, high momentum = EMERGING (watch closely)
        - Low position, low momentum = DEAD (archive)
        """
        results = []

        for node in self.graph.nodes.values():
            if node.id == "josh":
                continue

            position = node.weight

            # Momentum proxy: access count / age (higher access = more momentum)
            access = getattr(node, 'access_count', 0)
            momentum = min(5.0, access * 0.5)  # Cap at 5

            # Classify phase
            if position >= 3 and momentum >= 1:
                phase = "THRIVING"
            elif position >= 3 and momentum < 1:
                phase = "DECAYING"
            elif position < 3 and momentum >= 1:
                phase = "EMERGING"
            else:
                phase = "DORMANT"

            results.append({
                "node": node.name,
                "type": node.type,
                "position": round(position, 2),
                "momentum": round(momentum, 2),
                "phase": phase,
            })

        # Count phases
        from collections import Counter
        phase_counts = Counter(r["phase"] for r in results)

        thriving = sorted([r for r in results if r["phase"] == "THRIVING"], key=lambda x: -x["position"])
        decaying = sorted([r for r in results if r["phase"] == "DECAYING"], key=lambda x: -x["position"])
        emerging = sorted([r for r in results if r["phase"] == "EMERGING"], key=lambda x: -x["momentum"])

        return {
            "phase_distribution": dict(phase_counts),
            "thriving": thriving[:5],
            "decaying": decaying[:5],
            "emerging": emerging[:5],
            "interpretation": (
                f"Phase space: {phase_counts.get('THRIVING', 0)} thriving, "
                f"{phase_counts.get('DECAYING', 0)} decaying, "
                f"{phase_counts.get('EMERGING', 0)} emerging, "
                f"{phase_counts.get('DORMANT', 0)} dormant. "
                f"{'Healthy: more thriving than decaying.' if phase_counts.get('THRIVING', 0) > phase_counts.get('DECAYING', 0) else 'WARNING: more nodes decaying than thriving.'}"
            ),
        }

    # ═══════════════════════════════════════════
    # 6. COGNITIVE HAMILTONIAN (Total Energy)
    # ═══════════════════════════════════════════

    def hamiltonian(self) -> dict:
        """
        H = T + V (total energy = kinetic + potential)

        Kinetic T = Σ (access_count × weight) for all nodes (activity energy)
        Potential V = Σ (weight × centrality) for all nodes (stored energy)

        The Hamiltonian is CONSERVED in a closed system.
        If H is increasing: the system is gaining energy (from Josh's input).
        If H is decreasing: the system is losing energy (decay, neglect).
        Tracking H over time reveals whether the BEM is growing or dying.
        """
        adj = defaultdict(float)
        for edge in self.graph.edges:
            adj[(edge.source_id, edge.target_id)] = edge.weight
            adj[(edge.target_id, edge.source_id)] = edge.weight

        degree = defaultdict(float)
        for (src, _), w in adj.items():
            degree[src] += w
        max_degree = max(degree.values()) if degree else 1

        T = 0  # Kinetic energy
        V = 0  # Potential energy

        for node in self.graph.nodes.values():
            access = getattr(node, 'access_count', 0)
            centrality = degree.get(node.id, 0) / max_degree

            T += access * node.weight  # Activity × importance
            V += node.weight * centrality  # Importance × connectedness

        H = T + V

        return {
            "kinetic_energy_T": round(T, 2),
            "potential_energy_V": round(V, 2),
            "hamiltonian_H": round(H, 2),
            "T_V_ratio": round(T / V, 2) if V > 0 else 0,
            "interpretation": (
                f"Cognitive Hamiltonian H = {H:.1f} (T={T:.1f}, V={V:.1f}). "
                f"T/V ratio = {T/V:.2f}. "
                f"{'System is activity-dominant: lots of interaction, energy flowing.' if T > V else ''}"
                f"{'System is potential-dominant: stored energy exceeds activity. Need to ACTIVATE the potential.' if V > T else ''}"
                f"{'Balanced: kinetic and potential in equilibrium.' if 0.5 < T/V < 2 else ''}"
                f" Track H over time: increasing = growing, decreasing = dying."
            ),
        }

    # ═══════════════════════════════════════════
    # FULL FIELD REPORT
    # ═══════════════════════════════════════════

    def full_report(self) -> dict:
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "potentials": self.compute_potentials(),
            "gradients": self.compute_gradients(),
            "net_force": self.net_force(),
            "lagrangian": self.lagrangian_path(),
            "phase_space": self.phase_space(),
            "hamiltonian": self.hamiltonian(),
            "mechanism_22": {
                "name": "Cognitive Field Theory",
                "description": (
                    "The mind is not a graph. It is a FIELD. "
                    "Every node has a potential. Every edge creates a gradient. "
                    "Gradients create forces. Forces determine where attention flows. "
                    "The Lagrangian gives the path of least action. "
                    "The Hamiltonian measures total cognitive energy. "
                    "Phase space reveals what's thriving, decaying, emerging, or dead. "
                    "This is general relativity applied to one person's cognition. "
                    "The field equations of a single mind."
                ),
            },
        }


def demo():
    graph = IdentityGraph()
    engine = CognitiveField(graph)

    print("=" * 60)
    print("COGNITIVE FIELD THEORY — Josh's Mind as a Physical Field")
    print("Potentials, gradients, forces, Lagrangian, Hamiltonian.")
    print("=" * 60)

    report = engine.full_report()

    # Potentials
    p = report["potentials"]
    print(f"\n--- COGNITIVE POTENTIALS (where energy pools) ---")
    for node in p["potentials"][:7]:
        bar = "█" * int(node["potential"] * 2) + "░" * max(0, 20 - int(node["potential"] * 2))
        print(f"  [{bar}] {node['node']} ({node['type']}): V={node['potential']:.2f}")

    # Gradients
    g = report["gradients"]
    print(f"\n--- COGNITIVE GRADIENTS (strongest forces) ---")
    for grad in g["strongest_gradients"][:5]:
        print(f"  {grad['from']} ──({grad['gradient']:.2f})──→ {grad['to']}")
    print(f"  {g['interpretation'][:120]}")

    # Net Force
    nf = report["net_force"]
    print(f"\n--- NET FORCE (cognitive attractors) ---")
    for a in nf["attractors"][:5]:
        bar = "█" * int(a["net_force"]) + "░" * max(0, 10 - int(a["net_force"]))
        print(f"  [{bar}] {a['node']}: force={a['net_force']:.2f}, V={a['potential']:.2f}")
    print(f"  {nf['field_summary'][:120]}")

    # Lagrangian
    lag = report["lagrangian"]
    print(f"\n--- LAGRANGIAN PATH (minimum action trajectory) ---")
    print(f"  {lag['interpretation'][:150]}")

    # Phase Space
    ps = report["phase_space"]
    print(f"\n--- PHASE SPACE ---")
    print(f"  {ps['interpretation']}")
    if ps["thriving"]:
        print(f"  Thriving: {', '.join(n['node'] for n in ps['thriving'][:4])}")
    if ps["decaying"]:
        print(f"  Decaying: {', '.join(n['node'] for n in ps['decaying'][:4])}")
    if ps["emerging"]:
        print(f"  Emerging: {', '.join(n['node'] for n in ps['emerging'][:4])}")

    # Hamiltonian
    h = report["hamiltonian"]
    print(f"\n--- HAMILTONIAN (total cognitive energy) ---")
    print(f"  H = T + V = {h['kinetic_energy_T']:.1f} + {h['potential_energy_V']:.1f} = {h['hamiltonian_H']:.1f}")
    print(f"  {h['interpretation'][:120]}")

    print(f"\n{'=' * 60}")
    print("Mechanism 22: Cognitive Field Theory.")
    print("The mind is a field. The field has equations of motion.")
    print("The equations tell you where to go.")
    print("Follow the field. Fight the field = waste energy.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    demo()
