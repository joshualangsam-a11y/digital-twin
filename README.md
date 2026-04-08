# Digital Twin — Cognitive Architecture for Neurodivergent Founders

A living AI system that thinks like you, not just works for you.

Built by a 21-year-old ADHD/dyslexic founder who turned his brain's "weaknesses" into a computational architecture. This isn't a chatbot. It's a cognitive twin — a knowledge graph + reasoning engine + learning loop that mirrors how a specific brain actually works.

## What This Is

Most AI tools are built for neurotypical, sequential thinkers. This one isn't.

This cognitive architecture is designed around:
- **Parallel processing** — always 3+ tracks running, never single-thread
- **Gut-first decisions** — confidence > 80% = act, don't deliberate
- **Cross-domain pattern matching** — finding connections others miss
- **Loss framing** — "what you lose by not acting" is 2.5x more motivating
- **Momentum protection** — detecting stalls and prescribing track switches
- **Energy-aware routing** — different capabilities at different times of day

## Architecture

```
┌─────────────────────────────────────────┐
│           DIGITAL TWIN                  │
│                                         │
│  Identity Graph ← → Reasoning Engine    │
│       ↕                    ↕            │
│  Semantic Memory ← → Action Engine      │
│       ↕                    ↕            │
│  Claude Reasoning ← → Learning Engine   │
│                                         │
│         All engines feed back           │
│         into the graph.                 │
│         The twin compounds.             │
└─────────────────────────────────────────┘
```

### 5 Engines

| Engine | What It Does |
|--------|-------------|
| **Identity Graph** | Knowledge graph with typed nodes (person, project, goal, fear, value, pattern) and weighted edges. Your cognitive world, structured. |
| **Reasoning Engine** | Decisions modeled on ADHD cognitive patterns — gut scoring, parallel track management, OODA loops, loss framing. |
| **Learning Engine** | Memory decay (use it or lose it), reinforcement (approve = strengthen), pattern cluster detection, daily consolidation. |
| **Action Engine** | Proactive scanning — finds stale contacts, unlinked goals, compound opportunities, and missing patterns before you ask. |
| **Semantic Memory** | Vector embeddings over the graph. Search your mind by meaning, not keywords. Find hidden connections. |
| **Claude Reasoning** | LLM reasons over the graph with your cognitive constraints injected. Deep think, pattern discovery, flash translation. |

### Overnight Cycle

The twin runs at 3 AM:
1. Re-ingest new memory files
2. Decay unused nodes (memories fade like real brains)
3. Detect new pattern clusters
4. Scan for urgent actions
5. Generate morning briefing

### Feedback Loop

Every approval strengthens related nodes. Every rejection weakens them. Over time, the twin's judgment converges on yours.

## Quick Start

```bash
# Install dependencies
pip install anthropic numpy

# Bootstrap the graph from your memory files
python scripts/ingest_memories.py

# Boot the twin
python core/twin.py

# Morning briefing
python scripts/morning_wake.py

# Proactive scan
python engines/action.py

# Teach the twin
python scripts/feedback.py approve "description"
python scripts/feedback.py reject "description" "reason"
python scripts/feedback.py connect "Node A" "Node B" "relationship"
```

## Customization

The twin is built around one person's brain. To make it yours:

1. **Edit `scripts/ingest_memories.py`** — point it at your memory/knowledge files
2. **Edit `engines/reasoning.py`** — adjust the scoring to match YOUR decision patterns
3. **Edit the system prompt in `engines/claude_reasoning.py`** — inject YOUR cognitive constraints
4. **Feed it** — the more you approve/reject, the more it learns your judgment

## The Neurodivergent Angle

This project started from a brain mapping session. The key insight:

> ADHD isn't a disorder in the right environment. It's a different instruction set.

The twin is designed around that instruction set:
- **Parallel processing** instead of forced linearity
- **Momentum protection** instead of "take a break"
- **Energy-aware routing** instead of fighting your natural cycle
- **Pattern matching across domains** instead of siloed thinking
- **Loss framing** instead of gain framing (2.5x more effective for ADHD brains)

## Built With

- Python 3
- [Anthropic Claude API](https://docs.anthropic.com) for semantic embeddings and reasoning
- [Claude Code](https://claude.ai/code) as the development environment
- NumPy for vector similarity
- JSON knowledge graph (portable, inspectable, no database required)

## License

MIT

---

*Built in one session by a neurodivergent founder who was told his brain was broken. It wasn't. It was just waiting for the right architecture.*
