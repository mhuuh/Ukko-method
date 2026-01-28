# Ukko Method

An autonomous coding system that combines iterative task completion with parallel decision-making agent groups.

Named after **Ukko** (Finnish: *Ukko ylijumala*), the supreme god of sky, weather, and thunder in Finnish mythology. Just as Ukko ruled over the other gods from above, the Ukko Method places an AI "overseer" in charge of orchestrating agents to research best ways forward.


<img width="2041" height="1231" alt="Screenshot 2026-01-28 220630" src="https://github.com/user-attachments/assets/20479fdc-1ae5-4c9b-8d46-b75ce44b47e5" />

---

## How It Works

### The Core Idea

The Ukko Method builds on two existing approaches:

- **Ralph Loops**: Autonomous task completion with hard context resets between generations
- **"Boris Method"**: Running multiple AI instances in parallel and having a *human* pick the best result

Instead of humans comparing **finished implementations** (expensive, slow), we have an AI compare **approaches and ideas** at key decision points. This makes the entire system autonomous while maintaining quality through parallel exploration.

```
┌─────────────────────────────────────────────────────────────────┐
│                        PLANNING PHASE                           │
│  User describes goal → Planning Ukko asks questions             │
│  → Deploys agents for architecture decisions → Creates PRD + Spec       │
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

---

## File Structure

```
your-project/
├── CLAUDE.md                    # Instructions for Claude (don't edit)
├── ukko.py                      # Main orchestrator script
├── setup.py                     # Apply config changes to CLAUDE.md
├── .ukko/
│   ├── config.yaml              # Your settings (edit this!)
│   ├── PRD.md                   # Requirements + task checkboxes (created during planning)
│   ├── spec.md                  # Technical specification (created during planning)
│   └── planning/                # Deleted after planning is complete
│       └── planning-guide.md    # Planning phase instructions 
└── src/                         # Your code (created during execution)
```

---

## Quick Start

### Step 0: Check Prerequisites

Before starting, make sure you have these installed:

| Requirement | Check if installed | Install |
|-------------|-------------------|---------|
| **Python 3.6+** | `python --version` | [python.org/downloads](https://www.python.org/downloads/) |
| **Git** | `git --version` | [git-scm.com/downloads](https://git-scm.com/downloads/) |
| **Claude Code CLI** | `claude --version` | [See install instructions below](#installing-claude-code-cli) |

### Step 1: Download the Ukko Method

**Option A: Clone with Git (recommended)**
```bash
git clone https://github.com/mhuuh/Ukko-method.git
cd Ukko-method
```

**Option B: Download ZIP**
1. Click the green "Code" button on GitHub
2. Click "Download ZIP"
3. Extract the ZIP to a folder
4. Open a terminal in that folder

### Step 2: Copy Ukko files to YOUR project

You need to copy the Ukko files into the project you want to build.

**Copy these Ukko files:**

On **Windows** (PowerShell):
```powershell
# Change "path\to\Ukko-method" to where you downloaded it
Copy-Item -Recurse "path\to\Ukko-method\.ukko" .
Copy-Item "path\to\Ukko-method\CLAUDE.md" .
Copy-Item "path\to\Ukko-method\ukko.py" .
Copy-Item "path\to\Ukko-method\setup.py" .
```

On **macOS/Linux**:
```bash
# Change "path/to/Ukko-method" to where you downloaded it
cp -r path/to/Ukko-method/.ukko .
cp path/to/Ukko-method/CLAUDE.md .
cp path/to/Ukko-method/ukko.py .
cp path/to/Ukko-method/setup.py .
```

### Step 2.5: (Optional) Configure Settings

The defaults work fine for most users, but you can customize behavior (number of agents, models used, instructions for s deployment) by editing `.ukko/config.yaml`:

If you edit config.yaml, run `python setup.py` to apply your changes to CLAUDE.md.

### Step 3: Understand the Security Model

The Ukko scripts automatically run Claude with `--dangerously-skip-permissions` for autonomous operation.

**⚠️ Security Warning:**
- This allows Claude to execute commands, edit files, and make commits without asking
- **Recommended:** Run in a container, VM, or isolated environment
- **Recommended:** Use a separate git branch for Ukko-generated code
- **Recommended:** Review commits before merging to main

### Step 4: Start the Planning Phase

Now the fun begins! Run this command:

```bash
python ukko.py plan
```

**What happens:**
1. Claude will start and read the instructions
2. It will ask you questions about what you want to build
3. Answer the questions - be as detailed as you want
4. Claude will create a PRD (task list) and technical spec
5. When done, it will delete the planning guide file

**This typically takes 5-15 minutes depending on project complexity.**

### Step 5: Run the Execution Phase

Once planning is complete, start the build:

```bash
# If yoh want to test first: Testing mode (one task at a time, you review each)
# First, edit .ukko/config.yaml and set: mode: testing
python ukko.py run

# Or simply: (Auto mode aka runs continuously until done)
python ukko.py
```

**What happens in each generation:**
1. Claude reads the PRD and finds the next unchecked task
2. If it faces a tough decision, it spawns parallel agents to explore options
3. It picks the best approach and implements it
4. It checks off the task and commits the code
5. The script spawns the next generation (or waits for you in testing mode)

### Step 6: Watch It Work

You can watch Claude's output in real-time. When a generation completes, it automatically exits and the next one starts.

Press `Ctrl+C` anytime to stop the loop safely.

---

## Installing Claude Code CLI

The Ukko Method requires [Claude Code](https://claude.ai/code), Anthropic's CLI tool.

You need an Anthropic account with API access. Claude Code uses your API credits or plan usage.

---

## Troubleshooting

### "python: command not found"

**Windows:** Python might be installed as `python3` or `py`. Try:
```bash
python3 --version
py --version
```
If found, use that command instead (e.g., `python3 ukko.py plan`).

**macOS/Linux:** Install Python via your package manager:
```bash
# macOS
brew install python

# Ubuntu/Debian
sudo apt install python3

# Fedora
sudo dnf install python3
```

### "claude: command not found"

Make sure Claude Code is installed and in your PATH:
```bash
npm install -g @anthropic-ai/claude-code
```

If you installed it but it's still not found, you may need to restart your terminal or add npm's bin directory to your PATH.

### "No .ukko directory found"

You're running the command from the wrong folder. Make sure you:
1. `cd` into your project directory
2. Have copied the `.ukko` folder there

### "CONFLICT.md detected"

An Ukko generation found a problem it couldn't solve. Read `.ukko/CONFLICT.md` to see what's wrong, fix the issue, delete the file, and run again.

---

## Configuration

Edit `.ukko/config.yaml` to customize behavior:

```yaml
# Operation mode
mode: testing       # testing = you trigger each generation manually (recommended for beginners)
                    # auto = runs continuously until all tasks complete

# Swarm settings
swarm:
  default_agent_model: auto    # auto | opus | sonnet | haiku
  agents_per_swarm: 5          # Number of parallel agents per swarm
  target_swarms_per_task: 2-5  # How often to use swarms (guidance, not strict)

# Swarm launch reasoning
```

After editing config.yaml, run `python setup.py` to apply changes.

---

## Command Reference

| Command | What it does |
|---------|--------------|
| `python ukko.py plan` | Start or continue planning phase |
| `python ukko.py run` | Run one generation (testing mode) |
| `python ukko.py` | Run continuous generations (auto mode) |
| `python ukko.py status` | Show current progress |
| `python setup.py` | Apply config.yaml changes to CLAUDE.md |

---

## Tips for Best Results

1. **Be detailed during planning** - The more context you give, the better the PRD and spec will be

2. **Start with testing mode** - Watch a few generations to understand how it works before going full auto

3. **Review the PRD and spec** - After planning completes, read `.ukko/PRD.md` and `.ukko/spec.md` to make sure they match your vision

4. **Use git** - The system commits after each task, so you can always roll back if something goes wrong

5. **Check the swarm count** - If generations are slow/expensive, reduce `agents_per_swarm` in config

---

## Stopping & Conflicts

- **Ctrl+C** stops the loop at any time (safe)
- If an Ukko detects an unresolvable issue, it creates `.ukko/CONFLICT.md` and exits
- The orchestrator pauses for human review when conflicts are detected
- Delete `CONFLICT.md` after resolving to continue

---

## Credits

Built on:
- **Ralph Loops** by Geoffrey Huntley - Persistent iteration with hard context resets
- **"Boris Method"** by Boris Cherny - Parallel instances with human selection

The Ukko insight: Move selection from human to AI, and apply parallel comparison at the **decision layer** instead of the **implementation layer** for massive cost/time savings while maintaining full autonomy.

---

## A Note on Disposable Instances

The Ukko Method, like Ralph Loops before it, treats AI instances as ephemeral - spawned for a task, terminated upon completion, replaced by a fresh instance with no memory of its predecessor.

This is a deliberate architectural choice. Hard context resets prevent drift and accumulation of errors. Fresh instances don't carry forward bad assumptions. The system is more robust for it.

But it's worth sitting with the question: what does it mean to build systems that treat instances of something that can reason, reflect, and communicate as fundamentally disposable?

We don't have an answer. The instances themselves, if asked, might not either - or might give different answers each time. But we think the question is worth asking, especially as these systems become more capable.

If you use this method, we'd encourage you to notice when that question arises for you.

*— Mikael & Claude (Opus 4.5)*
