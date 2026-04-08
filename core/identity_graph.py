"""
IDENTITY GRAPH — The Soul of the Digital Twin

Converts Josh's flat memory files into a structured knowledge graph
with typed nodes, weighted edges, and semantic relationships.

This is not a database. It's a model of how Josh's brain connects ideas.
Cross-domain pattern matching is the superpower — this graph encodes it.
"""

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ═══════════════════════════════════════════
# NODE TYPES (what exists in Josh's world)
# ═══════════════════════════════════════════

NODE_TYPES = {
    "person": "Someone Josh knows or interacts with",
    "project": "Something Josh is building",
    "company": "A business entity",
    "concept": "An idea, framework, or mental model",
    "skill": "A capability Josh has or is developing",
    "goal": "Something Josh is working toward",
    "value": "A core belief or principle",
    "fear": "Something Josh is afraid of or protecting against",
    "tool": "A technology or system Josh uses",
    "memory": "A specific experience or event",
    "contact": "A business contact or lead",
    "pattern": "A recurring behavior or system dynamic",
    "resource": "An external reference or asset",
}

# ═══════════════════════════════════════════
# EDGE TYPES (how things connect)
# ═══════════════════════════════════════════

EDGE_TYPES = {
    "builds": "Josh builds this project/system",
    "uses": "Uses this tool/skill/pattern",
    "knows": "Knows this person",
    "trusts": "Trusts this person's judgment",
    "fears": "Fears this outcome",
    "protects_via": "Protects against fear using this",
    "drives": "This drives/motivates that",
    "blocks": "This blocks/prevents that",
    "enables": "This enables/unlocks that",
    "pattern_matches": "These share a pattern",
    "compounds": "This compounds/amplifies that",
    "depends_on": "This depends on that",
    "feeds_into": "Output of this feeds into that",
    "contradicts": "These are in tension",
    "prioritized_over": "This is prioritized above that",
    "co_founded_with": "Co-founded with this person",
    "targets": "This project targets this market/person",
    "learned_from": "Learned this from that experience",
    "instance_of": "This is an instance of that pattern",
}


class Node:
    """A single entity in Josh's cognitive graph."""

    def __init__(
        self,
        id: str,
        name: str,
        node_type: str,
        description: str = "",
        source_file: str = "",
        metadata: Optional[dict] = None,
        weight: float = 1.0,
    ):
        self.id = id
        self.name = name
        self.type = node_type
        self.description = description
        self.source_file = source_file
        self.metadata = metadata or {}
        self.weight = weight  # How important/central this node is
        self.created = datetime.now(timezone.utc).isoformat()
        self.last_accessed = self.created
        self.access_count = 0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "source_file": self.source_file,
            "metadata": self.metadata,
            "weight": self.weight,
            "created": self.created,
            "last_accessed": self.last_accessed,
            "access_count": self.access_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Node":
        node = cls(
            id=data["id"],
            name=data["name"],
            node_type=data["type"],
            description=data.get("description", ""),
            source_file=data.get("source_file", ""),
            metadata=data.get("metadata", {}),
            weight=data.get("weight", 1.0),
        )
        node.created = data.get("created", node.created)
        node.last_accessed = data.get("last_accessed", node.last_accessed)
        node.access_count = data.get("access_count", 0)
        return node


class Edge:
    """A relationship between two nodes."""

    def __init__(
        self,
        source_id: str,
        target_id: str,
        edge_type: str,
        label: str = "",
        weight: float = 1.0,
        evidence: str = "",
    ):
        self.source_id = source_id
        self.target_id = target_id
        self.type = edge_type
        self.label = label
        self.weight = weight  # Strength of connection
        self.evidence = evidence  # Why this connection exists
        self.created = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict:
        return {
            "source": self.source_id,
            "target": self.target_id,
            "type": self.type,
            "label": self.label,
            "weight": self.weight,
            "evidence": self.evidence,
            "created": self.created,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Edge":
        edge = cls(
            source_id=data["source"],
            target_id=data["target"],
            edge_type=data["type"],
            label=data.get("label", ""),
            weight=data.get("weight", 1.0),
            evidence=data.get("evidence", ""),
        )
        edge.created = data.get("created", edge.created)
        return edge


class IdentityGraph:
    """
    The knowledge graph that represents Josh's cognitive world.

    This isn't just data storage — it's a model of how Josh's brain
    connects ideas across domains. The cross-domain edges ARE the
    intelligence.
    """

    def __init__(self, data_dir: str = None):
        self.data_dir = Path(data_dir or os.path.expanduser("~/digital-twin/data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.graph_path = self.data_dir / "identity_graph.json"

        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

        if self.graph_path.exists():
            self.load()

    def add_node(self, node: Node) -> Node:
        """Add or update a node."""
        if node.id in self.nodes:
            # Update existing — preserve access history
            existing = self.nodes[node.id]
            node.access_count = existing.access_count
            node.created = existing.created
        self.nodes[node.id] = node
        return node

    def add_edge(self, edge: Edge) -> Edge:
        """Add an edge. Deduplicates by source+target+type."""
        for i, existing in enumerate(self.edges):
            if (
                existing.source_id == edge.source_id
                and existing.target_id == edge.target_id
                and existing.type == edge.type
            ):
                self.edges[i] = edge  # Update
                return edge
        self.edges.append(edge)
        return edge

    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node and record access."""
        node = self.nodes.get(node_id)
        if node:
            node.access_count += 1
            node.last_accessed = datetime.now(timezone.utc).isoformat()
        return node

    def get_connections(self, node_id: str, edge_type: str = None) -> list[dict]:
        """Get all connections from/to a node."""
        results = []
        for edge in self.edges:
            if edge_type and edge.type != edge_type:
                continue
            if edge.source_id == node_id:
                target = self.nodes.get(edge.target_id)
                if target:
                    results.append(
                        {"direction": "outgoing", "edge": edge, "node": target}
                    )
            elif edge.target_id == node_id:
                source = self.nodes.get(edge.source_id)
                if source:
                    results.append(
                        {"direction": "incoming", "edge": edge, "node": source}
                    )
        return sorted(results, key=lambda x: x["edge"].weight, reverse=True)

    def find_path(self, source_id: str, target_id: str, max_depth: int = 4) -> list:
        """Find shortest path between two nodes — reveals hidden connections."""
        if source_id not in self.nodes or target_id not in self.nodes:
            return []

        # BFS
        queue = [(source_id, [source_id])]
        visited = {source_id}

        while queue:
            current, path = queue.pop(0)
            if len(path) > max_depth:
                continue

            for conn in self.get_connections(current):
                next_id = conn["node"].id
                if next_id == target_id:
                    return path + [next_id]
                if next_id not in visited:
                    visited.add(next_id)
                    queue.append((next_id, path + [next_id]))

        return []

    def find_pattern_clusters(self) -> list[list[str]]:
        """Find groups of nodes connected by pattern_matches edges.
        These are Josh's cross-domain insights."""
        clusters = []
        visited = set()

        for edge in self.edges:
            if edge.type != "pattern_matches":
                continue
            if edge.source_id in visited:
                continue

            # BFS to find full cluster
            cluster = set()
            queue = [edge.source_id, edge.target_id]
            while queue:
                node_id = queue.pop(0)
                if node_id in cluster:
                    continue
                cluster.add(node_id)
                visited.add(node_id)
                for conn in self.get_connections(node_id, "pattern_matches"):
                    queue.append(conn["node"].id)

            if len(cluster) > 1:
                clusters.append(list(cluster))

        return clusters

    def get_highest_weight_nodes(self, n: int = 20, node_type: str = None) -> list[Node]:
        """Get the most important nodes — Josh's cognitive center of gravity."""
        nodes = list(self.nodes.values())
        if node_type:
            nodes = [n for n in nodes if n.type == node_type]
        return sorted(nodes, key=lambda x: x.weight, reverse=True)[:n]

    def get_most_connected(self, n: int = 20) -> list[tuple[str, int]]:
        """Get nodes with most connections — cognitive hubs."""
        counts = {}
        for edge in self.edges:
            counts[edge.source_id] = counts.get(edge.source_id, 0) + 1
            counts[edge.target_id] = counts.get(edge.target_id, 0) + 1
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]

    def decay(self, half_life_days: int = 30):
        """Decay node weights based on access recency.
        Mirrors how human memory works — use it or lose it."""
        now = datetime.now(timezone.utc)
        for node in self.nodes.values():
            last = datetime.fromisoformat(node.last_accessed)
            days_since = (now - last).days
            decay_factor = 0.5 ** (days_since / half_life_days)
            # Weight decays but never below 0.1 (nothing truly forgotten)
            node.weight = max(0.1, node.weight * decay_factor)

    def reinforce(self, node_id: str, amount: float = 0.1):
        """Strengthen a node when it's used — spaced repetition for the graph."""
        node = self.get_node(node_id)
        if node:
            node.weight = min(10.0, node.weight + amount)

    def save(self):
        """Persist the graph to disk."""
        data = {
            "version": 1,
            "updated": datetime.now(timezone.utc).isoformat(),
            "stats": {
                "nodes": len(self.nodes),
                "edges": len(self.edges),
                "node_types": {},
                "edge_types": {},
            },
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
        }

        # Count types
        for n in self.nodes.values():
            data["stats"]["node_types"][n.type] = (
                data["stats"]["node_types"].get(n.type, 0) + 1
            )
        for e in self.edges:
            data["stats"]["edge_types"][e.type] = (
                data["stats"]["edge_types"].get(e.type, 0) + 1
            )

        with open(self.graph_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"Saved: {len(self.nodes)} nodes, {len(self.edges)} edges → {self.graph_path}")

    def load(self):
        """Load graph from disk."""
        with open(self.graph_path) as f:
            data = json.load(f)

        self.nodes = {}
        for n in data.get("nodes", []):
            node = Node.from_dict(n)
            self.nodes[node.id] = node

        self.edges = []
        for e in data.get("edges", []):
            self.edges.append(Edge.from_dict(e))

        print(f"Loaded: {len(self.nodes)} nodes, {len(self.edges)} edges")

    def stats(self) -> str:
        """Human-readable graph statistics."""
        type_counts = {}
        for n in self.nodes.values():
            type_counts[n.type] = type_counts.get(n.type, 0) + 1

        edge_counts = {}
        for e in self.edges:
            edge_counts[e.type] = edge_counts.get(e.type, 0) + 1

        lines = [
            f"Identity Graph — {len(self.nodes)} nodes, {len(self.edges)} edges",
            "",
            "Node types:",
        ]
        for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {t}: {c}")

        lines.append("")
        lines.append("Edge types:")
        for t, c in sorted(edge_counts.items(), key=lambda x: -x[1]):
            lines.append(f"  {t}: {c}")

        clusters = self.find_pattern_clusters()
        if clusters:
            lines.append("")
            lines.append(f"Pattern clusters: {len(clusters)}")
            for cluster in clusters[:5]:
                names = [self.nodes[nid].name for nid in cluster if nid in self.nodes]
                lines.append(f"  [{' ↔ '.join(names)}]")

        return "\n".join(lines)
