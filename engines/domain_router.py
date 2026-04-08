"""
DOMAIN ROUTER — Cognitive Domain Thermal Management

Based on BEM Mechanism 10: Parallel Processing as Thermal Management

The key insight: ADHD brains don't fail at focus. They MANAGE THERMAL LOAD.
When one cognitive domain overheats (error rates spike, velocity drops),
the solution isn't to "try harder" — it's to SWITCH DOMAINS.

Different cognitive domains use different neural circuits:
- Code Building: Working memory + spatial reasoning (high thermal cost)
- Writing: Language + narrative flow (low working memory cost)
- Research: Pattern matching + novelty seeking (high engagement)
- Sales: Social reasoning + intuition + persuasion
- Admin: Linear task execution (low cognitive load)
- Creative: Divergent thinking + association (high divergence, low convergence cost)
- Strategic: High-level pattern matching (different thermal signature)

When domain_A is too hot, switch to domain_B to cool A's neural circuits
while keeping total cognitive output constant. This is why parallel tracks
aren't optional for ADHD — they're thermal regulation.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph, Node


class DomainRouter:
    """
    Routes work across cognitive domains based on thermal state.
    Implements Mechanism 10: thermal management via domain switching.
    """

    DOMAINS = {
        "code_building": {
            "description": "Programming, architecture, debugging",
            "thermal_cost": 0.8,  # High working memory usage
            "recovery_time_minutes": 30,
            "error_rate_threshold": 0.15,  # Errors per minute trigger switch
        },
        "writing": {
            "description": "Copy, documentation, narrative",
            "thermal_cost": 0.4,
            "recovery_time_minutes": 15,
            "error_rate_threshold": 0.10,
        },
        "research": {
            "description": "Investigation, pattern discovery, learning",
            "thermal_cost": 0.6,
            "recovery_time_minutes": 20,
            "error_rate_threshold": 0.12,
        },
        "sales": {
            "description": "Outreach, demos, persuasion, negotiation",
            "thermal_cost": 0.5,
            "recovery_time_minutes": 25,
            "error_rate_threshold": 0.10,
        },
        "admin": {
            "description": "Tasks, organization, linear work",
            "thermal_cost": 0.2,
            "recovery_time_minutes": 5,
            "error_rate_threshold": 0.20,
        },
        "creative": {
            "description": "Design, brainstorming, divergent thinking",
            "thermal_cost": 0.7,
            "recovery_time_minutes": 20,
            "error_rate_threshold": 0.08,
        },
        "strategic": {
            "description": "Planning, big-picture thinking, priority alignment",
            "thermal_cost": 0.6,
            "recovery_time_minutes": 25,
            "error_rate_threshold": 0.12,
        },
    }

    def __init__(self, graph: IdentityGraph = None):
        self.graph = graph or IdentityGraph()
        self.data_dir = Path(os.path.expanduser("~/digital-twin/data"))
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.routing_log = self.data_dir / "domain_routing.jsonl"

        # Heat state: domain_id -> {temp: 0-1, cooldown_until: timestamp, error_count: int}
        self.heat_map: dict[str, dict] = {}
        for domain_id in self.DOMAINS.keys():
            self.heat_map[domain_id] = {
                "temp": 0.0,
                "cooldown_until": None,
                "error_count": 0,
                "session_time_minutes": 0,
                "last_accessed": None,
            }

        self.current_domain: Optional[str] = None
        self.active_tracks: list[str] = []

    # ═══════════════════════════════════════════
    # DOMAIN SWITCHING
    # ═══════════════════════════════════════════

    def get_current_domain(self) -> Optional[str]:
        """What domain are we in right now?"""
        return self.current_domain

    def switch_to_domain(self, domain_id: str, reason: str = "") -> dict:
        """
        Switch the active cognitive domain.

        This is how parallel tracks work:
        - Domain A overheats → switch to Domain B
        - Both are being worked, but attention is split for thermal management
        """
        if domain_id not in self.DOMAINS:
            return {"error": f"Unknown domain: {domain_id}"}

        now = datetime.now(timezone.utc)
        previous = self.current_domain

        # Check if domain is in cooldown
        cooldown_until = self.heat_map[domain_id].get("cooldown_until")
        if cooldown_until and datetime.fromisoformat(cooldown_until) > now:
            return {
                "error": f"Domain {domain_id} still cooling. Resume at {cooldown_until}",
                "domain": domain_id,
                "status": "cooling",
                "retry_at": cooldown_until,
            }

        self.current_domain = domain_id
        self.heat_map[domain_id]["last_accessed"] = now.isoformat()

        # Log switch
        entry = {
            "timestamp": now.isoformat(),
            "event": "domain_switch",
            "from_domain": previous,
            "to_domain": domain_id,
            "reason": reason,
            "previous_thermal": self.heat_map[previous]["temp"] if previous else None,
        }
        self._append_log(entry)

        if domain_id not in self.active_tracks:
            self.active_tracks.append(domain_id)

        return {
            "domain": domain_id,
            "description": self.DOMAINS[domain_id]["description"],
            "switched_from": previous,
            "active_tracks": self.active_tracks,
            "current_thermal": self.heat_map[domain_id]["temp"],
        }

    def suggest_domain_switch(self) -> Optional[dict]:
        """
        AI-driven suggestion: should we switch domains right now?

        Returns a domain to switch to, or None if current domain is fine.
        """
        if not self.current_domain:
            return None

        current_heat = self.heat_map[self.current_domain]["temp"]

        # If current domain is hot (> 0.7), find a cool domain
        if current_heat > 0.7:
            cool_domains = [
                (domain_id, info)
                for domain_id, info in self.heat_map.items()
                if domain_id != self.current_domain
                and info["temp"] < 0.5
                and not (info.get("cooldown_until") and
                        datetime.fromisoformat(info["cooldown_until"]) > datetime.now(timezone.utc))
            ]

            if cool_domains:
                # Sort by lowest temp
                cool_domains.sort(key=lambda x: x[1]["temp"])
                suggested = cool_domains[0]

                return {
                    "current_domain": self.current_domain,
                    "current_thermal": current_heat,
                    "suggested_domain": suggested[0],
                    "suggested_thermal": suggested[1]["temp"],
                    "reason": f"Current domain overheating ({current_heat:.2f}). Switch to cool {suggested[0]} ({suggested[1]['temp']:.2f})",
                }

        return None

    # ═══════════════════════════════════════════
    # THERMAL MANAGEMENT
    # ═══════════════════════════════════════════

    def record_work(self, domain_id: str, duration_minutes: float,
                   errors: int = 0, quality_score: float = 1.0) -> dict:
        """
        Record work done in a domain.

        Thermal management:
        - duration × thermal_cost → heat increase
        - quality_score 1.0 = no heat spike, < 1.0 = error = extra heat
        - errors per minute trigger cooldown
        """
        if domain_id not in self.DOMAINS:
            return {"error": f"Unknown domain: {domain_id}"}

        domain_info = self.DOMAINS[domain_id]
        thermal_cost = domain_info["thermal_cost"]

        # Heat increase: time × cost × inverse_quality
        heat_increase = (duration_minutes / 60) * thermal_cost * (1.0 / quality_score)

        old_temp = self.heat_map[domain_id]["temp"]
        new_temp = min(1.0, old_temp + heat_increase)

        # Error tracking
        error_rate = errors / max(duration_minutes, 1)
        self.heat_map[domain_id]["error_count"] += errors
        self.heat_map[domain_id]["session_time_minutes"] += duration_minutes
        self.heat_map[domain_id]["temp"] = new_temp

        # Check if we hit the error threshold
        in_cooldown = False
        if error_rate > domain_info["error_rate_threshold"]:
            # Trigger cooldown
            cooldown_minutes = domain_info["recovery_time_minutes"]
            cooldown_until = datetime.now(timezone.utc)
            from datetime import timedelta
            cooldown_until = cooldown_until + timedelta(minutes=cooldown_minutes)

            self.heat_map[domain_id]["cooldown_until"] = cooldown_until.isoformat()
            in_cooldown = True

        # Log work
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "work_recorded",
            "domain": domain_id,
            "duration_minutes": duration_minutes,
            "errors": errors,
            "quality_score": quality_score,
            "error_rate": round(error_rate, 3),
            "thermal_increase": round(heat_increase, 3),
            "old_temp": round(old_temp, 2),
            "new_temp": round(new_temp, 2),
            "in_cooldown": in_cooldown,
        }
        self._append_log(entry)

        return {
            "domain": domain_id,
            "thermal": round(new_temp, 2),
            "thermal_status": self._thermal_status(new_temp),
            "error_rate": round(error_rate, 3),
            "in_cooldown": in_cooldown,
            "suggestion": self.suggest_domain_switch(),
        }

    def decay_heat(self, minutes_elapsed: float = 1.0) -> dict:
        """
        Cool all domains over time.
        Like a heat sink: without activity, thermal energy dissipates.
        """
        decay_factor = 0.02 * minutes_elapsed  # Cool 2% per minute of idle time

        for domain_id, state in self.heat_map.items():
            # Domains cool faster when not in use
            if domain_id != self.current_domain:
                decay_factor_adjusted = decay_factor * 1.5  # 50% faster cooling
            else:
                decay_factor_adjusted = decay_factor

            old_temp = state["temp"]
            new_temp = max(0.0, old_temp - decay_factor_adjusted)
            state["temp"] = new_temp

        return {
            "decay_factor": decay_factor,
            "thermal_map": {
                domain_id: round(state["temp"], 2)
                for domain_id, state in self.heat_map.items()
            },
        }

    def _thermal_status(self, temp: float) -> str:
        """Describe thermal status as a zone."""
        if temp < 0.3:
            return "cool"
        elif temp < 0.5:
            return "warm"
        elif temp < 0.7:
            return "hot"
        elif temp < 0.9:
            return "critical"
        else:
            return "thermal_throttle"

    # ═══════════════════════════════════════════
    # PARALLEL TRACK MANAGEMENT
    # ═══════════════════════════════════════════

    def open_parallel_track(self, domain_id: str, reason: str = "") -> dict:
        """
        Open a secondary track in a different domain.
        This is how ADHD brains distribute thermal load.

        Working on code_building gets hot → open writing track to cool code region.
        """
        if domain_id in self.active_tracks:
            return {"error": f"{domain_id} already in active_tracks"}

        self.active_tracks.append(domain_id)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "parallel_track_open",
            "domain": domain_id,
            "reason": reason,
            "active_tracks": self.active_tracks,
        }
        self._append_log(entry)

        return {
            "domain": domain_id,
            "description": self.DOMAINS[domain_id]["description"],
            "active_tracks": self.active_tracks,
        }

    def close_parallel_track(self, domain_id: str) -> dict:
        """Close a secondary track."""
        if domain_id not in self.active_tracks:
            return {"error": f"{domain_id} not in active_tracks"}

        self.active_tracks.remove(domain_id)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "parallel_track_close",
            "domain": domain_id,
            "active_tracks": self.active_tracks,
        }
        self._append_log(entry)

        return {
            "closed": domain_id,
            "active_tracks": self.active_tracks,
        }

    def get_thermal_map(self) -> dict:
        """Current thermal state of all domains."""
        now = datetime.now(timezone.utc)

        return {
            "current_domain": self.current_domain,
            "active_tracks": self.active_tracks,
            "domains": {
                domain_id: {
                    "thermal": round(state["temp"], 2),
                    "status": self._thermal_status(state["temp"]),
                    "session_time_minutes": round(state["session_time_minutes"], 1),
                    "error_count": state["error_count"],
                    "in_cooldown": bool(
                        state.get("cooldown_until") and
                        datetime.fromisoformat(state["cooldown_until"]) > now
                    ),
                    "last_accessed": state.get("last_accessed"),
                }
                for domain_id, state in self.heat_map.items()
            },
        }

    # ═══════════════════════════════════════════
    # UTILITIES
    # ═══════════════════════════════════════════

    def _append_log(self, entry: dict):
        """Append to routing log."""
        with open(self.routing_log, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def stats(self) -> dict:
        """Statistics on domain usage and thermal patterns."""
        total_time = sum(
            state["session_time_minutes"] for state in self.heat_map.values()
        )
        total_errors = sum(
            state["error_count"] for state in self.heat_map.values()
        )

        return {
            "total_domain_time_hours": round(total_time / 60, 1),
            "total_errors_across_domains": total_errors,
            "by_domain": {
                domain_id: {
                    "session_time_minutes": round(state["session_time_minutes"], 1),
                    "error_count": state["error_count"],
                    "error_rate": round(
                        state["error_count"] / max(state["session_time_minutes"], 1),
                        3
                    ),
                    "current_thermal": round(state["temp"], 2),
                }
                for domain_id, state in self.heat_map.items()
            },
        }
