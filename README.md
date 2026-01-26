# Ukko Method

An autonomous coding system that combines iterative task completion (Ralph Loops) with parallel decision-making swarms.

Named after **Ukko** (Finnish: *Ukko ylijumala*), the supreme god of sky, weather, and thunder in Finnish mythology. Just as Ukko ruled over the other gods from above, the Ukko Method places an AI "overseer" in charge of orchestrating autonomous agents.

## How It Works

### The Core Idea

The Ukko Method builds on two existing approaches:

- **Ralph Loops**: Autonomous task completion with hard context resets between generations
- **Boris Method**: Running multiple AI instances in parallel and having a *human* pick the best result

The key insight: Instead of humans comparing **finished implementations** (expensive, slow), we have an AI compare **approaches and ideas** (cheap, fast) at key decision points. This makes the entire system autonomous while maintaining quality through parallel exploration.

```
┌─────────────────────────────────────────────────────────────────┐
│                        PLANNING PHASE                           │
│  User describes goal → Planning Ukko asks questions             │
│  → Swarms for architecture decisions → Creates PRD + Spec       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       EXECUTION PHASE                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    GENERATION LOOP                        │   │
│  │  Ukko reads PRD/Spec → Picks next task                   │   │
│  │        ↓                                                  │   │
│  │  Key decision point?                                      │   │
│  │        ↓ yes                                              │   │
│  │  ┌─────┴─────┐                                            │   │
│  │  ↓     ↓     ↓                                            │   │
│  │  [Agent][Agent][Agent]  ← Parallel swarm                  │   │
│  │  └─────┬─────┘                                            │   │
│  │        ↓                                                  │   │
│  │  Ukko picks best approach (AI decision, not human)        │   │
│  │        ↓                                                  │   │
│  │  Implement → Tick box → Commit → Exit                     │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              ↓                                  │
│                     Next generation...                          │
└─────────────────────────────────────────────────────────────────┘
```

### Key Principles

1. **PRD and Spec are READ-ONLY** during execution (except ticking task boxes)
2. **Hard context reset** between generations (fresh start, no context rot)
3. **Swarms for decisions, not implementations** (compare ideas, not code)
4. **AI picks the best approach** (fully autonomous - no human in the loop after planning)
5. **Decision breadcrumbs in-code** (minimal comments where decisions were made)

## Quick Start

### 1. Setup

Copy the `.ukko/` directory and files to your project:

```bash
cp -r .ukko/ your-project/
cp CLAUDE.md your-project/
cp ukko.sh your-project/
chmod +x your-project/ukko.sh
```

### 2. Planning Phase

```bash
cd your-project
./ukko.sh plan
```

The Planning Ukko will:
- Ask clarifying questions about what you want to build
- Deploy swarms for major architectural decisions
- Create the PRD (requirements + tasks) and technical spec
- Clean up and prepare for execution

### 3. Execution Phase

```bash
# Auto mode (continuous until complete)
./ukko.sh

# Or testing mode (manual trigger each generation)
# First set mode: testing in .ukko/config.yaml
./ukko.sh run
```

### 4. Monitor Progress

```bash
./ukko.sh status
```

## File Structure

```
your-project/
├── CLAUDE.md                    # Bootstrap + execution instructions
├── ukko.sh                      # Orchestrator script
├── .ukko/
│   ├── config.yaml              # User settings (mode, swarm config)
│   ├── PRD.md                   # Requirements + task checkboxes
│   ├── spec.md                  # Technical specification
│   └── planning/                # Deleted after planning complete
│       └── planning-guide.md    # Planning phase instructions
└── src/                         # Your code (created during execution)
```

## Configuration

Edit `.ukko/config.yaml`:

```yaml
# Operation mode
mode: auto          # auto = continuous loop, testing = manual trigger

# Swarm settings
swarm:
  default_agent_model: auto    # auto | opus | sonnet | haiku
  agents_per_swarm: 5          # Number of parallel agents
  target_swarms_per_task: 2-5  # Guidance for swarm frequency
```

## Decision Triggers

Ukkos deploy swarms when facing:
- Architectural approach choices
- Library/dependency selection
- Data model design
- API contract decisions
- Any choice that constrains future implementation

## Stopping & Conflicts

- **Ctrl+C** stops the loop at any time
- If an Ukko detects an unresolvable issue, it creates `.ukko/CONFLICT.md` and exits
- The orchestrator pauses for human review when conflicts are detected

## Credits

Built on:
- **Ralph Loops** - Persistent iteration with hard context resets
- **Boris Method** - Parallel instances with human selection

The Ukko insight: Move selection from human to AI, and apply parallel comparison at the **decision layer** instead of the **implementation layer** for massive cost/time savings while maintaining full autonomy.
