# Digital Twin Scripts

Overnight and wake cycles for Josh's cognitive architecture.

## Scripts

### `overnight.py` — End-of-day consolidation
**When to run:** 3 AM or manually before sleep  
**Purpose:** Memory consolidation, pattern detection, insights generation

```bash
python3 ~/digital-twin/scripts/overnight.py
```

**What it does:**
1. Runs `twin.sleep()` for daily consolidation (decay, patterns, insights)
2. Saves session state via SessionBridge for context restoration
3. Runs EmergentTheory engine to crystallize new discoveries
4. Generates compound report showing graph growth

**Output:**
- Report: `~/digital-twin/data/overnight_reports/YYYY-MM-DD.json`
- Latest snapshot: `~/digital-twin/data/overnight_reports/latest.json`
- Terminal output: Clean summary with metrics

---

### `morning_wake.py` — Start-of-day boot
**When to run:** Morning or start of work session  
**Purpose:** Restore context, surface priorities, show urgent actions

```bash
python3 ~/digital-twin/scripts/morning_wake.py
```

**What it does:**
1. Runs `twin.wake()` with current energy level detection
2. Loads last night's overnight report
3. Restores session context via SessionBridge
4. Displays top 3 priorities for current energy level
5. Shows urgent actions from proactive scan
6. Displays compound metrics (graph health, growth)

**Output:**
- Terminal display formatted for piping to `/morning-briefing`
- Shows energy level, priorities, urgent actions, graph metrics

---

### `session_save.py` — End-of-session snapshot
**When to run:** End of Claude Code session (via Stop hook)  
**Purpose:** Capture what was done for cross-session compounding

```bash
# Minimal (no args)
python3 ~/digital-twin/scripts/session_save.py

# Full usage
python3 ~/digital-twin/scripts/session_save.py \
  --project "hemp-route" \
  --duration 120 \
  --files "scripts/overnight.py" "scripts/morning_wake.py" \
  --achievements "Built overnight cycle" "Fixed twin.sleep()" \
  --errors "SessionBridge API changed" \
  --quality 0.9
```

**Arguments:**
- `--project TEXT` — Project name (e.g., "digital-twin", "lit-juris")
- `--duration INT` — Session length in minutes
- `--files PATH [PATH ...]` — Space-separated list of files touched
- `--achievements TEXT [TEXT ...]` — Wins/breakthroughs
- `--errors TEXT [TEXT ...]` — Errors encountered
- `--quality FLOAT` — Self-assessed quality score 0-1 (default: 1.0)

**What it does:**
1. Saves session snapshot to `~/digital-twin/data/sessions/YYYY-MM-DD_HH-MM-SS.json`
2. Bridges to twin via SessionBridge (records achievements as aha moments)
3. Appends to session log for cross-session analysis
4. Prints summary

**Output:**
- Session JSON: `~/digital-twin/data/sessions/YYYY-MM-DD_HH-MM-SS.json`
- Log entry: `~/digital-twin/data/session_log.jsonl` (append-only)
- Terminal summary

---

## Data Directories

```
~/digital-twin/data/
├── overnight/              # (deprecated) Legacy overnight reports
├── overnight_reports/      # NEW: Daily consolidation reports (YYYY-MM-DD.json)
├── sessions/               # Session snapshots (session_YYYY-MM-DD_HH-MM-SS.json)
├── snapshots/              # Graph snapshots for emergent theory
├── theory_papers/          # BEM mechanism papers
├── identity_graph.json     # Current graph state
├── session_bridge.jsonl    # Append-only session bridge log
├── session_log.jsonl       # Append-only session log
└── twin_state.json         # Twin metadata (cycles, decisions, learnings)
```

---

## Integration

### Claude Code Stop Hook
Add to `.claude/settings.json` to auto-save sessions:

```json
{
  "hooks": {
    "stop": {
      "command": ["python3", "~/digital-twin/scripts/session_save.py"],
      "args": ["--project", "CURRENT_PROJECT", "--duration", "SESSION_DURATION"],
      "captureOutput": true
    }
  }
}
```

### Cron Job
Add to crontab to auto-run overnight cycle:

```cron
0 3 * * * python3 ~/digital-twin/scripts/overnight.py >> /tmp/overnight.log 2>&1
```

### Morning Briefing
Pipe morning output to Claude Code's `/morning-briefing` skill:

```bash
python3 ~/digital-twin/scripts/morning_wake.py | /morning-briefing
```

---

## Design Principles

1. **Standalone**: All scripts run as `python3 script.py` with no dependencies on Claude Code
2. **Graceful errors**: Never crash on bad data; log errors and continue
3. **Clean output**: Terminal display optimized for human reading
4. **Composable**: Each script can run independently or in sequence
5. **Lightweight**: Use existing engines (twin.py, session_bridge.py, emergent_theory.py)
6. **Persistent**: All data saved to JSON or JSONL for inspection and debugging

---

## Testing

```bash
# Test overnight cycle
python3 ~/digital-twin/scripts/overnight.py

# Test morning wake
python3 ~/digital-twin/scripts/morning_wake.py

# Test session save
python3 ~/digital-twin/scripts/session_save.py --project test --duration 30

# Check latest overnight report
cat ~/digital-twin/data/overnight_reports/latest.json | python3 -m json.tool

# View last 5 sessions
ls -ltr ~/digital-twin/data/sessions/session_*.json | tail -5

# View session log
tail -10 ~/digital-twin/data/session_log.jsonl
```
