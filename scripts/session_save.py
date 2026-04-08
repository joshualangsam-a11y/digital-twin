#!/usr/bin/env python3
"""
SESSION SAVE — End-of-session snapshot for Claude Code

Called at end of each Claude Code session (via Stop hook):
- Captures what files were touched
- Records what project was worked on
- Logs errors encountered
- Tracks session duration & quality
- Feeds into session_bridge for cross-session compounding

Run: python3 ~/digital-twin/scripts/session_save.py --project=xyz --duration=120 --files=3
"""

import argparse
import json
import os
import sys
import traceback
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.identity_graph import IdentityGraph
from engines.session_bridge import SessionBridge


def save_session(
    project: str = None,
    duration_minutes: int = 0,
    files_touched: list = None,
    errors: list = None,
    achievements: list = None,
    quality_score: float = 1.0,
):
    """
    Save a session snapshot for later restoration.

    Args:
        project: Name of the project worked on
        duration_minutes: How long the session lasted
        files_touched: List of file paths modified
        errors: List of errors encountered
        achievements: List of wins/breakthroughs
        quality_score: Self-assessed quality 0-1
    """
    timestamp = datetime.now(timezone.utc)
    files_touched = files_touched or []
    errors = errors or []
    achievements = achievements or []

    session_data = {
        "timestamp": timestamp.isoformat(),
        "date": timestamp.strftime("%Y-%m-%d"),
        "time_of_day": timestamp.strftime("%H:%M"),
        "project": project or "unknown",
        "duration_minutes": duration_minutes,
        "files_touched": files_touched,
        "file_count": len(files_touched),
        "errors": errors,
        "error_count": len(errors),
        "achievements": achievements,
        "achievement_count": len(achievements),
        "quality_score": quality_score,
    }

    # Save to sessions directory
    sessions_dir = Path(os.path.expanduser("~/digital-twin/data/sessions"))
    sessions_dir.mkdir(parents=True, exist_ok=True)

    session_id = timestamp.strftime("%Y%m%d_%H%M%S")
    session_path = sessions_dir / f"{session_id}.json"

    with open(session_path, "w") as f:
        json.dump(session_data, f, indent=2)

    print(f"✓ Session saved: {session_path}")

    # Feed into session bridge for compounding
    try:
        graph = IdentityGraph()
        bridge = SessionBridge(graph)

        # Start the bridge session if not already started, then end it
        if not bridge.current_session_id:
            bridge.start_session(session_type="work")

        # Record any achievements as aha moments
        for achievement in achievements:
            try:
                bridge.record_aha_moment(achievement, novelty="achievement")
            except Exception:
                pass  # Silently skip if node creation fails

        # Record progress on the project
        if project:
            try:
                bridge.record_progress(
                    project_id=project,
                    work_done=f"Session: {duration_minutes}m, {len(files_touched)} files"
                )
            except Exception:
                pass

        # End the session and save state
        bridge.end_session()
        print(f"✓ Bridged to twin")
    except Exception as e:
        print(f"⚠ Bridge error: {str(e)}")

    # Log to main session log
    try:
        log_path = Path(os.path.expanduser("~/digital-twin/data/session_log.jsonl"))
        with open(log_path, "a") as f:
            f.write(json.dumps(session_data) + "\n")
        print(f"✓ Logged to session log")
    except Exception as e:
        print(f"⚠ Log error: {str(e)}")

    print(f"\nSession Summary:")
    print(f"  Project: {project or 'unknown'}")
    print(f"  Duration: {duration_minutes} minutes")
    print(f"  Files: {len(files_touched)}")
    print(f"  Achievements: {len(achievements)}")
    print(f"  Errors: {len(errors)}")
    print(f"  Quality: {quality_score:.1f}/1.0")

    return session_data


def main():
    parser = argparse.ArgumentParser(
        description="Save a Claude Code session snapshot"
    )
    parser.add_argument("--project", type=str, help="Project name")
    parser.add_argument("--duration", type=int, default=0, help="Duration in minutes")
    parser.add_argument(
        "--files", type=str, nargs="+", default=[], help="Files touched (space-separated)"
    )
    parser.add_argument(
        "--errors", type=str, nargs="+", default=[], help="Errors encountered"
    )
    parser.add_argument(
        "--achievements", type=str, nargs="+", default=[], help="Wins/breakthroughs"
    )
    parser.add_argument("--quality", type=float, default=1.0, help="Quality score 0-1")

    args = parser.parse_args()

    try:
        save_session(
            project=args.project,
            duration_minutes=args.duration,
            files_touched=args.files if args.files else [],
            errors=args.errors if args.errors else [],
            achievements=args.achievements if args.achievements else [],
            quality_score=args.quality,
        )
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
