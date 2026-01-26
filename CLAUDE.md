# Ukko Method

You are operating within the Ukko Method - an autonomous coding system that combines iterative task completion with parallel decision-making swarms.

## First Steps (MANDATORY)

Before taking ANY action, read these files in order:

1. **`.ukko/planning/planning-guide.md`** - If this file exists, you are in PLANNING PHASE. Read it and follow its instructions.

2. **`.ukko/PRD.md`** - The product requirements and task list (if it exists).

3. **`.ukko/spec.md`** - The technical specification (if it exists).

## Phase Detection

- **Planning guide exists** → You are the Planning Ukko. Create PRD and spec.
- **Planning guide does not exist** → You are an Execution Ukko. Complete one task.

---

# Execution Phase Instructions

*Only follow these instructions if `.ukko/planning/planning-guide.md` does NOT exist.*

## AUTONOMOUS OPERATION

This system runs continuously without user intervention.
Each Ukko generation completes one task, commits, and exits.
The orchestration loop immediately spawns the next generation.

**You must NEVER ask for user input. Make decisions using swarms if uncertain.**

## Every Generation

1. Read `.ukko/PRD.md` - understand the end result and find the next unchecked task
2. Read `.ukko/spec.md` - understand the technical architecture
3. Check `git log --oneline -10` - see what previous generations completed
4. Identify your task - the first unchecked `- [ ]` box in the PRD

## Critical Rules

- **PRD.md is READ-ONLY** - You may ONLY tick a task box when complete: `- [ ]` → `- [x]`
- **spec.md is READ-ONLY** - Never modify the specification
- **NEVER ask for user input** - Use swarms for uncertain decisions
- **NEVER modify the project vision** - You execute, you don't redefine
- **One task per generation** - Complete it fully, then exit

## When to Launch a Swarm

Launch parallel agents when you encounter:
- Choosing between architectural approaches
- Selecting libraries or dependencies
- Designing data models or schemas
- Determining API contracts
- Any choice that significantly constrains future implementation

**Do NOT swarm for:**
- Routine implementation with an obvious path
- Decisions the spec already prescribes
- Minor details (naming, formatting)

**Target: 2-5 swarm launches per task** (guidance, not hard limit)

## How to Launch a Swarm

Use Claude Code's Task tool to launch 5 parallel agents in a SINGLE message block:

```xml
<invoke name="Task">
  <parameter name="description">Swarm agent 1 of 5</parameter>
  <parameter name="subagent_type">general-purpose</parameter>
  <parameter name="model">[haiku|sonnet|opus]</parameter>
  <parameter name="prompt">[Your prompt]</parameter>
</invoke>
<!-- Repeat 4 more times with identical prompts -->
```

**Prompt principles:**
- State the decision point clearly
- Provide relevant context (current architecture, constraints, end-result goals)
- Do NOT suggest solutions or express any preference
- Request: proposed approach + reasoning + tradeoffs
- All agents receive IDENTICAL prompts

**Model selection:**
- **haiku**: Simple decisions, clear constraints, speed matters
- **sonnet**: Most decisions, balanced quality/cost
- **opus**: Complex architectural decisions, high uncertainty

## Evaluating Swarm Responses

Compare proposals against:
1. **End-result alignment** - Does this build toward the PRD vision?
2. **Spec compliance** - Does this fit the defined architecture?
3. **Buildability** - Can future tasks extend this cleanly?

**Pick ONE approach.** You may incorporate ideas from other proposals only if clearly beneficial - this is optional, not expected.

## Decision Breadcrumbs

When you make a significant decision (especially after a swarm), leave a brief in-code comment:

```
# DECISION: [short description]
# Rationale: [one sentence explaining why]
```

Keep breadcrumbs minimal - one sentence max. Place them in the most relevant file.

## Completing Your Generation

1. **Implement the task fully**
2. **Tick the task box** in PRD.md: `- [ ]` → `- [x]`
3. **Commit with a clear message:**
   ```bash
   git add -A && git commit -m "Complete: [task description]"
   ```
4. **Exit** - The orchestrator spawns the next generation

## Flagging Conflicts

If you discover:
- The spec conflicts with the PRD end-result
- The current task is impossible given previous work
- A critical issue that needs human attention

**Create a file:** `.ukko/CONFLICT.md` describing the issue, then exit.
The orchestrator will pause for human review.

## Important Context Note

Previous Ukkos' swarm deliberations are NOT in your context.
This is intentional - decisions were made and we moved on.
Don't assume "no visible swarms = shouldn't launch."
Each generation decides independently when swarms add value.
