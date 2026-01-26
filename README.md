# Overlord Method

An autonomous coding system that combines iterative task completion (Ralph Loops) with parallel decision-making swarms (Boris Method).

## How It Works

### The Core Idea

Instead of comparing **finished implementations** (expensive), the Overlord Method compares **approaches and ideas** (cheap) at key decision points.

```
┌─────────────────────────────────────────────────────────────────┐
│                        PLANNING PHASE                           │
│  User describes goal → Planning Overlord asks questions         │
│  → Swarms for architecture decisions → Creates PRD + Spec       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       EXECUTION PHASE                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    GENERATION LOOP                        │   │
│  │  Overlord reads PRD/Spec → Picks next task               │   │
│  │        ↓                                                  │   │
│  │  Key decision point?                                      │   │
│  │        ↓ yes                                              │   │
│  │  ┌─────┴─────┐                                            │   │
│  │  ↓     ↓     ↓                                            │   │
│  │  [Agent][Agent][Agent]  ← Parallel swarm                  │   │
│  │  └─────┬─────┘                                            │   │
│  │        ↓                                                  │   │
│  │  Overlord picks best approach                             │   │
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
4. **No user input during execution** (fully autonomous after planning)
5. **Decision breadcrumbs in-code** (minimal comments where decisions were made)

## Quick Start

### 1. Setup

Copy the `.overlord/` directory and files to your project:

```bash
cp -r .overlord/ your-project/
cp CLAUDE.md your-project/
cp overlord.sh your-project/
```

### 2. Planning Phase

```bash
cd your-project
./overlord.sh plan
```

The Planning Overlord will:
- Ask clarifying questions about what you want to build
- Deploy swarms for major architectural decisions
- Create the PRD (requirements + tasks) and technical spec
- Clean up and prepare for execution

### 3. Execution Phase

```bash
# Auto mode (continuous until complete)
./overlord.sh

# Or testing mode (manual trigger each generation)
# First set mode: testing in .overlord/config.yaml
./overlord.sh run
```

### 4. Monitor Progress

```bash
./overlord.sh status
```

## File Structure

```
your-project/
├── CLAUDE.md                    # Bootstrap - tells Overlord what to read
├── overlord.sh                  # Orchestrator script
├── .overlord/
│   ├── config.yaml              # User settings (mode, swarm config)
│   ├── PRD.md                   # Requirements + task checkboxes
│   ├── spec.md                  # Technical specification
│   ├── overlord-guide.md        # Execution phase instructions
│   └── planning/                # Deleted after planning complete
│       └── planning-guide.md    # Planning phase instructions
└── src/                         # Your code (created during execution)
```

## Configuration

Edit `.overlord/config.yaml`:

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

Overlords deploy swarms when facing:
- Architectural approach choices
- Library/dependency selection
- Data model design
- API contract decisions
- Any choice that constrains future implementation

## Stopping & Conflicts

- **Ctrl+C** stops the loop at any time
- If an Overlord detects an unresolvable issue, it creates `.overlord/CONFLICT.md` and exits
- The orchestrator pauses for human review when conflicts are detected

## Credits

Built on:
- **Ralph Loops** - Persistent iteration with hard context resets
- **Boris Method** - Parallel instances, pick the best result

The insight: Apply Boris at the **decision layer** instead of the **implementation layer** for massive cost/time savings.
