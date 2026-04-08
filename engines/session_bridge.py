"""
SESSION BRIDGE — Cross-Session Working Memory

THE #1 ADHD PROBLEM: Working memory resets at sleep.
THE SOLUTION: Session state snapshot + Zeigarnik effect + memory consolidation.

How it works:
1. At end of work session: capture what was being thought, what clicked, what's about to click
2. Compress via identity graph: connect session insights to existing knowledge
3. At start of new session: decompress with context, restore flow state
4. Track "aha moments" to ensure they survive the reset

This is the time-bridge that lets ADHD brains compound intelligence.
Without it, every session starts from zero. With it, each session starts from the peak of the last.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node, Edge


class SessionBridge:
    """
    Bridges the gap between sessions for ADHD working memory.
    Saves session state, restores flow context, preserves aha moments.
    """

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.sessions_dir = self.data_dir / "sessions"
        self.sessions_dir.mkdir(exist_ok=True)

        self.session_log = self.data_dir / "session_bridge.jsonl"
        self.current_session_id: Optional[str] = None
        self.current_session_state: dict = {}

    # ═══════════════════════════════════════════
    # SESSION START — Restore from last state
    # ═══════════════════════════════════════════

    def start_session(self, session_type: str = "work") -> dict:
        """
        Wake up with context from the last session.
        Load compressed state + aha moments + unfinished threads.

        session_type: "work" | "research" | "creative" | "admin"
        """
        now = datetime.now(timezone.utc)
        self.current_session_id = f"session_{now.strftime('%Y%m%d_%H%M%S')}"

        self.current_session_state = {
            "session_id": self.current_session_id,
            "started_at": now.isoformat(),
            "type": session_type,
            "thoughts": [],
            "aha_moments": [],
            "progress": {},
            "thermal_state": "cold",
        }

        # Load previous session snapshot
        restoration = self._load_previous_snapshot()

        # Log startup
        entry = {
            "timestamp": now.isoformat(),
            "event": "session_start",
            "session_id": self.current_session_id,
            "type": session_type,
            "restored_from": restoration.get("previous_session_id"),
            "restored_items": {
                "unfinished_thoughts": len(restoration.get("unfinished_thoughts", [])),
                "aha_moments": len(restoration.get("aha_moments", [])),
                "context_nodes": len(restoration.get("context_nodes", [])),
            },
        }
        self._append_log(entry)

        return {
            "session_id": self.current_session_id,
            "restored": restoration,
            "context": self._build_session_context(),
        }

    def _load_previous_snapshot(self) -> dict:
        """
        Load the most recent session snapshot.
        Prioritize aha moments and unfinished threads.
        """
        # Find most recent session file
        session_files = sorted(self.sessions_dir.glob("session_*.json"))
        if not session_files:
            return {
                "unfinished_thoughts": [],
                "aha_moments": [],
                "context_nodes": [],
            }

        with open(session_files[-1]) as f:
            snapshot = json.load(f)

        return {
            "previous_session_id": snapshot.get("session_id"),
            "unfinished_thoughts": snapshot.get("unfinished_thoughts", []),
            "aha_moments": snapshot.get("aha_moments", []),
            "context_nodes": snapshot.get("context_nodes", []),
            "thermal_baseline": snapshot.get("thermal_state", "cold"),
        }

    def _build_session_context(self) -> dict:
        """Build the cognitive context for this session from the graph."""
        # Get highest-weight nodes (what matters most)
        important = self.graph.get_highest_weight_nodes(n=10)

        # Get most-connected nodes (cognitive hubs)
        hubs = self.graph.get_most_connected(n=5)
        hub_names = [self.graph.nodes[hub_id].name for hub_id, _ in hubs
                     if hub_id in self.graph.nodes]

        # Find pattern clusters (cross-domain insights)
        clusters = self.graph.find_pattern_clusters()

        return {
            "priorities": [n.name for n in important],
            "cognitive_hubs": hub_names,
            "active_patterns": [
                [self.graph.nodes[nid].name for nid in cluster if nid in self.graph.nodes]
                for cluster in clusters[:3]
            ],
            "graph_health": {
                "total_nodes": len(self.graph.nodes),
                "total_edges": len(self.graph.edges),
                "density": len(self.graph.edges) / max(len(self.graph.nodes), 1),
            },
        }

    # ═══════════════════════════════════════════
    # DURING SESSION — Capture thoughts & moments
    # ═══════════════════════════════════════════

    def record_thought(self, content: str, about_node_id: str = None,
                      confidence: float = 0.5) -> dict:
        """
        Record a thought during the session.
        If it connects to existing nodes, strengthen those connections.
        """
        thought = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": content,
            "about_node_id": about_node_id,
            "confidence": confidence,
        }

        self.current_session_state["thoughts"].append(thought)

        # If this thought is about a graph node, reinforce it
        if about_node_id and about_node_id in self.graph.nodes:
            self.graph.reinforce(about_node_id, amount=0.05)

        return thought

    def record_aha_moment(self, insight: str, connected_nodes: list[str] = None,
                         novelty: str = "new") -> dict:
        """
        Record an aha moment — insights that need to survive the session reset.

        novelty: "new" | "connection" | "refinement"

        These are protected memory. They get added to the graph immediately
        so they don't disappear at sleep.
        """
        now = datetime.now(timezone.utc)
        aha_id = f"aha_{now.strftime('%H%M%S')}"

        # Add to graph as a concept node
        aha_node = Node(
            id=aha_id,
            name=f"Aha: {insight[:50]}",
            node_type="concept",
            description=insight,
            weight=3.0,
            metadata={
                "novelty": novelty,
                "session_id": self.current_session_id,
                "timestamp": now.isoformat(),
            },
        )
        self.graph.add_node(aha_node)

        # Connect to relevant nodes
        if connected_nodes:
            for node_id in connected_nodes:
                if node_id in self.graph.nodes:
                    edge = Edge(
                        source_id=aha_id,
                        target_id=node_id,
                        edge_type="learned_from",
                        weight=2.0,
                        evidence=insight,
                    )
                    self.graph.add_edge(edge)

        self.current_session_state["aha_moments"].append({
            "id": aha_id,
            "insight": insight,
            "novelty": novelty,
            "connected_nodes": connected_nodes or [],
        })

        # Log immediately (don't wait for session end)
        entry = {
            "timestamp": now.isoformat(),
            "event": "aha_moment",
            "session_id": self.current_session_id,
            "aha_id": aha_id,
            "insight": insight,
            "novelty": novelty,
        }
        self._append_log(entry)

        return {"id": aha_id, "added_to_graph": True}

    def record_progress(self, project_id: str, work_done: str,
                       blockers: list[str] = None) -> dict:
        """
        Record progress on a project during the session.
        Useful for remembering what was accomplished and what's stuck.
        """
        if project_id not in self.current_session_state["progress"]:
            self.current_session_state["progress"][project_id] = {
                "work_items": [],
                "blockers": [],
            }

        self.current_session_state["progress"][project_id]["work_items"].append(
            work_done
        )

        if blockers:
            self.current_session_state["progress"][project_id]["blockers"].extend(
                blockers
            )

        return self.current_session_state["progress"][project_id]

    def update_thermal_state(self, level: float) -> dict:
        """
        Track cognitive thermal state during session.
        0.0 = cool, 0.5 = warm, 1.0 = thermal throttling
        """
        self.current_session_state["thermal_state"] = level

        if level > 0.8:
            return {
                "thermal_level": level,
                "status": "THROTTLING",
                "recommendation": "Switch domains or take a break",
            }
        elif level > 0.6:
            return {
                "thermal_level": level,
                "status": "HOT",
                "recommendation": "Start second track to cool primary domain",
            }
        else:
            return {
                "thermal_level": level,
                "status": "NOMINAL",
                "recommendation": "Continue focus",
            }

    # ═══════════════════════════════════════════
    # SESSION END — Save state for next session
    # ═══════════════════════════════════════════

    def end_session(self) -> dict:
        """
        End of session: compress state and save for next session.

        Process:
        1. Identify unfinished threads (incomplete work, open questions)
        2. Protect aha moments (already in graph, but also in snapshot)
        3. Create Zeigarnik hooks (what's most likely to be thought about?)
        4. Save compressed snapshot
        """
        if not self.current_session_id:
            return {"error": "No active session"}

        now = datetime.now(timezone.utc)

        # Identify unfinished threads (work in progress, incomplete thoughts)
        unfinished = self._extract_unfinished_threads()

        # Extract context nodes we were working with
        context_node_ids = self._extract_active_context_nodes()

        # Build the snapshot
        snapshot = {
            "session_id": self.current_session_id,
            "started_at": self.current_session_state["started_at"],
            "ended_at": now.isoformat(),
            "type": self.current_session_state["type"],

            # What to restore next time
            "unfinished_thoughts": unfinished,
            "aha_moments": self.current_session_state["aha_moments"],
            "context_nodes": context_node_ids,
            "progress_by_project": self.current_session_state["progress"],

            # Thermal baseline for next session
            "thermal_state": self.current_session_state["thermal_state"],

            # Metadata for analysis
            "total_thoughts": len(self.current_session_state["thoughts"]),
            "total_aha_moments": len(self.current_session_state["aha_moments"]),
            "session_duration_minutes": (
                (datetime.fromisoformat(now.isoformat()) -
                 datetime.fromisoformat(self.current_session_state["started_at"])).total_seconds() / 60
            ),
        }

        # Save snapshot to file
        session_file = self.sessions_dir / f"{self.current_session_id}.json"
        with open(session_file, "w") as f:
            json.dump(snapshot, f, indent=2)

        # Save graph (contains all aha moments)
        self.graph.save()

        # Log session end
        entry = {
            "timestamp": now.isoformat(),
            "event": "session_end",
            "session_id": self.current_session_id,
            "type": self.current_session_state["type"],
            "aha_moments_created": len(self.current_session_state["aha_moments"]),
            "unfinished_threads": len(unfinished),
            "snapshot_saved": str(session_file),
        }
        self._append_log(entry)

        self.current_session_id = None

        return {
            "session_id": snapshot["session_id"],
            "snapshot_file": str(session_file),
            "aha_moments_protected": len(snapshot["aha_moments"]),
            "unfinished_threads": len(snapshot["unfinished_thoughts"]),
            "ready_for_next_session": True,
        }

    def _extract_unfinished_threads(self) -> list[dict]:
        """
        Extract incomplete thoughts and work items.
        These become Zeigarnik hooks for the next session.
        """
        unfinished = []

        # Recent thoughts with low confidence are unfinished
        for thought in self.current_session_state["thoughts"]:
            if thought["confidence"] < 0.7:
                unfinished.append({
                    "type": "incomplete_thought",
                    "content": thought["content"],
                    "about_node": thought.get("about_node_id"),
                })

        # Work items with blockers are unfinished
        for project_id, progress in self.current_session_state["progress"].items():
            if progress.get("blockers"):
                for blocker in progress["blockers"]:
                    unfinished.append({
                        "type": "blocker",
                        "content": blocker,
                        "project": project_id,
                    })

        return unfinished

    def _extract_active_context_nodes(self) -> list[str]:
        """
        Find which nodes we were actively thinking about this session.
        These become high-weight in the next session's context.
        """
        context_nodes = []

        # Nodes mentioned in thoughts
        for thought in self.current_session_state["thoughts"]:
            if thought.get("about_node_id"):
                context_nodes.append(thought["about_node_id"])

        # Nodes connected to aha moments
        for aha in self.current_session_state["aha_moments"]:
            context_nodes.extend(aha.get("connected_nodes", []))

        # Remove duplicates and invalid refs
        valid_context = list(set(
            nid for nid in context_nodes if nid in self.graph.nodes
        ))

        return valid_context[:10]  # Top 10 context nodes

    # ═══════════════════════════════════════════
    # UTILITIES
    # ═══════════════════════════════════════════

    def _append_log(self, entry: dict):
        """Append to session bridge log."""
        with open(self.session_log, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def session_summary(self, session_id: str = None) -> dict:
        """Get summary of a session."""
        if not session_id:
            session_id = self.current_session_id

        if not session_id:
            return {"error": "No session specified"}

        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            return {"error": f"Session {session_id} not found"}

        with open(session_file) as f:
            snapshot = json.load(f)

        return {
            "session_id": session_id,
            "type": snapshot.get("type"),
            "duration_minutes": round(snapshot.get("session_duration_minutes", 0), 1),
            "aha_moments": len(snapshot.get("aha_moments", [])),
            "unfinished_threads": len(snapshot.get("unfinished_thoughts", [])),
            "projects_touched": list(snapshot.get("progress_by_project", {}).keys()),
            "thermal_state": snapshot.get("thermal_state"),
        }

    def stats(self) -> dict:
        """Statistics on all sessions."""
        sessions = list(self.sessions_dir.glob("session_*.json"))

        total_ahas = 0
        total_threads = 0
        total_time = 0.0

        for session_file in sessions:
            with open(session_file) as f:
                snapshot = json.load(f)
                total_ahas += len(snapshot.get("aha_moments", []))
                total_threads += len(snapshot.get("unfinished_thoughts", []))
                total_time += snapshot.get("session_duration_minutes", 0)

        return {
            "total_sessions": len(sessions),
            "total_aha_moments": total_ahas,
            "total_unfinished_threads": total_threads,
            "total_session_time_hours": round(total_time / 60, 1),
            "avg_session_minutes": round(total_time / max(len(sessions), 1), 1),
        }
