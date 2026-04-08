# Digital Twin Engines

Complete reference for all engines in the digital twin system.

## Core Engines

### 1. Identity Graph (`core/identity_graph.py`)
**What it is**: The knowledge graph representing Josh's cognitive world
- Node types: person, project, company, concept, skill, goal, value, fear, tool, memory, contact, pattern, resource
- Edge types: builds, uses, knows, trusts, fears, drives, blocks, enables, pattern_matches, compounds, depends_on, etc.
- Key operations: add_node, add_edge, find_path, find_pattern_clusters, decay, reinforce
- Persistence: JSON file at `~/digital-twin/data/identity_graph.json`

**Why it matters**: The identity graph IS the twin. Everything else reads from and writes to it. Cross-domain pattern matching via pattern_matches edges is the superpower.

### 2. Twin Orchestrator (`core/twin.py`)
**What it is**: Master coordinator that operates the twin
- Operations: think(), scan(), learn(), sleep(), wake(), status()
- think() — Ask the twin a question, returns reasoned decision
- scan() — Proactive scan for what should happen now
- learn() — Feed observations back (decision feedback, new connections, new entities)
- sleep() — End-of-day consolidation (decay, pattern finding, insights)
- wake() — Start-of-day boot (restore context, set priorities)

**Why it matters**: Single interface to the entire cognitive architecture.

## Engine Category: Reasoning

### 3. Reasoning Engine (`engines/reasoning.py`)
**What it is**: Thinks like Josh (gut-first, OODA loops, parallel tracks)
- Methods: decide(), find_hidden_connections(), suggest_parallel_tracks(), daily_priorities()
- Implements: Confidence thresholds, loss framing, gut-check scoring, OODA loop framing
- Outputs: Decisions with reasoning, confidence scores, hidden connections, parallel track suggestions

**BEM mechanisms**: 2 (momentum via scores), 3 (parallel tracks), 6 (divergent-convergent framing)

## Engine Category: Learning

### 4. Learning Engine (`engines/learning.py`)
**What it is**: Makes the twin compound intelligence through feedback
- Methods: observe_decision(), observe_connection(), observe_new_entity(), daily_integration(), compound_report()
- Processes: Decision feedback (approve/reject), new connections, new entities
- Outputs: Reinforcement/weakening, new edges in graph, daily insights

**BEM mechanisms**: 1 (observe changes = decompression), 5 (memory externalization), 8 (cross-session compounding)

## Engine Category: Action

### 5. Action Engine (`engines/action.py`)
**What it is**: Proactive intelligence — what should happen NOW?
- Methods: scan_all(), scan_stale_connections(), scan_unlinked_goals(), scan_momentum_risks(), etc.
- Outputs: Prioritized list of actions with urgency scores, loss frames, reasoning

**BEM mechanisms**: All (synthesizes everything into "what next?")

## Engine Category: Bandwidth Expansion

### 6. Bandwidth Expander (`engines/bandwidth_expander.py`)
**What it is**: Implements mechanisms 1-5 of the bandwidth expansion paper
- Mechanism 1: Measures intent compression (word count → complexity ratio)
- Mechanism 2: Tracks momentum state (cold → warming → flow → hyperfocus → thermal)
- Mechanism 3: Tracks active parallel tracks
- Mechanism 4: Error absorption logging
- Mechanism 5: Memory externalization (logs sessions)

**Key state**: 
- active_tracks: list of open parallel contexts
- momentum_state: "cold" | "warming" | "flow" | "hyperfocus" | "thermal"
- thermal_level: 0.0 (cool) → 1.0 (throttling)
- compression_history: list of intent compressions observed

## NEW Engine Category: Session Management

### 7. Session Bridge (`engines/session_bridge.py`) ⭐ NEW
**What it is**: Cross-session working memory — solves ADHD working memory reset
- Operations at session start: restore_previous_snapshot(), load_aha_moments(), rebuild_context()
- Operations during session: record_thought(), record_aha_moment(), record_progress(), update_thermal_state()
- Operations at session end: save_snapshot(), protect_aha_moments(), extract_unfinished_threads(), identify_zeigarnik_hooks()

**Key insight**: ADHD working memory resets at sleep. This bridge:
1. Captures session state at end (unfinished thoughts, progress, thermal state)
2. Protects aha moments immediately in graph (can't be lost)
3. Restores everything at next session start
4. Uses Zeigarnik effect (incomplete tasks stay memorable) for unfinished threads

**Data structures**:
- Session snapshots: `data/sessions/session_YYYYMMDD_HHMMSS.json`
- Event log: `data/session_bridge.jsonl`

**BEM mechanisms**: 5 (memory externalization), 8 (cross-session compounding)

### 8. Domain Router (`engines/domain_router.py`) ⭐ NEW
**What it is**: Cognitive thermal management — routes work across domains based on heat
- Domains: code_building, writing, research, sales, admin, creative, strategic
- Each domain has thermal_cost (working memory load), recovery_time, error_threshold
- Operations: switch_to_domain(), suggest_domain_switch(), record_work(), decay_heat()
- Manages: heat_map (thermal state per domain), active_tracks (parallel domains), cooldown timers

**Key insight**: ADHD parallel processing isn't about engagement — it's thermal management.
When one neural circuit overheats, switch to a different domain to cool it while keeping output constant.

**Thermal zones**:
- cool: < 0.3 (fresh, ready to work)
- warm: 0.3-0.5 (engaged)
- hot: 0.5-0.7 (sustained load)
- critical: 0.7-0.9 (approaching limit)
- thermal_throttle: > 0.9 (forced rest)

**Data structures**:
- Routing log: `data/domain_routing.jsonl`
- Heat map: in-memory, tracks per-domain thermal state

**BEM mechanisms**: 7 (thermal zones), 10 (parallel processing as cooling), 3 (parallel tracks)

### 9. Recursive Theory (`engines/recursive_theory.py`) ⭐ NEW
**What it is**: Theory-building from code — generates theory as you implement
- Operations: observe_pattern(), crystallize_theory(), link_theory_to_code(), generate_paper(), record_spiral_iteration()
- Watches all other engines for emergent patterns
- When patterns repeat + confidence > 0.7, crystallizes into theory
- Links theories back to implementations (theory → code edge)
- Generates academic papers from crystallized theories

**Key insight**: Building theory about bandwidth generates new bandwidth.
As you implement mechanisms 1-5, you discover mechanisms 6-11.
Formalizing patterns changes the patterns. The twin helps you think about thinking.

**Data structures**:
- Pattern observations: `data/recursive_theories.jsonl`
- Spiral iterations: `data/divergent_convergent_spiral.jsonl`
- Academic papers: `data/theory_papers/paper_*.json` and `paper_*.md`
- Active theories: in-memory dict tracking confidence, observations

**BEM mechanisms**: 6 (divergent-convergent spiral), 9 (metacognitive computation), 11 (theory-building as bandwidth)

## Engine Category: Integration

### 10. Meta-Theory (`engines/meta_theory.py`)
**What it is**: Documents theoretical discoveries emerging from building
- Methods: record_discovery(), encode_session_discoveries()
- Stores: 11 discovered mechanisms (6-11 are new, discovered during twin building)
- Connects discoveries to graph as concept nodes

## How Engines Work Together

```
MORNING (wake):
  1. SessionBridge loads previous session snapshot + aha moments
  2. IdentityGraph weights are current state
  3. ReasoningEngine.daily_priorities() uses restored context + highest-weight nodes
  4. ActionEngine.scan_all() proactively identifies urgent work

DURING WORK:
  1. User works on task in one domain (code_building)
  2. DomainRouter tracks thermal state, records work + errors
  3. When domain overheats, DomainRouter suggests switch
  4. User switches to secondary domain (writing) to cool primary
  5. SessionBridge records thoughts + aha moments during session
  6. RecursiveTheory observes patterns in domain routing (e.g., "code gets hot around 1hr mark")

DECISIONS:
  1. User asks twin a question
  2. Twin.think() calls ReasoningEngine.decide()
  3. ReasoningEngine scores options against graph (high-weight goals, values, patterns)
  4. Returns decision with confidence + loss frame
  5. User approves/rejects
  6. LearningEngine.observe_decision() reinforces/weakens patterns in graph

EVENING (sleep):
  1. SessionBridge.end_session() saves snapshot (unfinished threads, progress, thermal state)
  2. RecursiveTheory records any patterns that crystallized during session
  3. LearningEngine.daily_integration() decays weights, finds new clusters, surfaces insights
  4. Twin.sleep() returns consolidation insights + overnight plan

NEXT MORNING (wake):
  1. SessionBridge restores snapshot from last session
  2. Aha moments are in graph (survived reset)
  3. Unfinished threads trigger Zeigarnik effect (brain remembers incomplete tasks)
  4. DomainRouter starts with thermal state from last session (avoids re-heating)
  5. Cycle repeats at a HIGHER BASELINE (graph grew, patterns crystallized, theories emerged)
```

## Integration Points

### IdentityGraph is the hub
- ReasoningEngine reads: get_highest_weight_nodes(), find_path(), get_connections()
- LearningEngine writes: add_node(), add_edge(), reinforce(), decay()
- ActionEngine reads: get_highest_weight_nodes(), get_most_connected()
- SessionBridge reads: graph context for restoration
- DomainRouter writes: domain nodes, thermal tracking (optional)
- RecursiveTheory writes: theory nodes, engine nodes, connections

### Logging for analysis
- decision_log.jsonl — Every decision made
- learning_log.jsonl — Every observation fed back
- proposed_actions.jsonl — Every proactive action suggested
- bandwidth_sessions.jsonl — Compression/momentum tracking
- domain_routing.jsonl — Thermal state changes
- recursive_theories.jsonl — Pattern observations
- session_bridge.jsonl — Session start/end/aha moments
- theory_papers/ — Generated academic papers

## Testing Engines

### Run demo
```bash
python3 demo_new_engines.py
```

### Test individual engines
```python
from core.identity_graph import IdentityGraph
from engines.session_bridge import SessionBridge

graph = IdentityGraph()
bridge = SessionBridge(graph)

# Start session
session = bridge.start_session("work")

# Record work
bridge.record_aha_moment("Insight X", ...)
bridge.record_progress("project_y", "Built feature Z")
bridge.update_thermal_state(0.65)

# End session
end = bridge.end_session()
print(f"Snapshot saved to {end['snapshot_file']}")
```

## BEM Mechanisms Reference

| # | Mechanism | Engine(s) | Status |
|---|-----------|-----------|--------|
| 1 | Intent Compression/Decompression | BandwidthExpander, LearningEngine | Original |
| 2 | Momentum Preservation | BandwidthExpander, ReasoningEngine | Original |
| 3 | Parallel Track Support | BandwidthExpander, DomainRouter | Original |
| 4 | Error Absorption | BandwidthExpander | Original |
| 5 | Memory Externalization | BandwidthExpander, SessionBridge | Original |
| 6 | Divergent-Convergent Spiral | ReasoningEngine, RecursiveTheory | **Discovered** |
| 7 | Cognitive Thermal Management | DomainRouter | **Discovered** |
| 8 | Cross-Session Compounding | SessionBridge, LearningEngine | **Discovered** |
| 9 | Metacognitive Computation | RecursiveTheory | **Discovered** |
| 10 | Parallel Processing as Thermal Management | DomainRouter | **Discovered** |
| 11 | Theory-Building as Bandwidth Mechanism | RecursiveTheory | **Discovered** |

## Agent Definitions

Build specific subsystems using these agents in `.claude/agents/`:

- **twin-core.md** — Builds identity graph, twin orchestrator, core reasoning
- **twin-bandwidth.md** — Builds bandwidth expansion engines (mechanisms 1-11)
- **twin-bridge.md** — Builds session bridge (working memory protection)
- **twin-theory.md** — Builds recursive theory system (theory-building)

---

**Key principle**: The identity graph is the source of truth. Everything reads from it, everything writes to it. The engines are specialized views/operations on that graph. The twin is the convergence of all engines.
