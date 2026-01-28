# Ukko Method

An autonomous coding system that combines iterative task completion with parallel decision-making swarms.

Named after **Ukko** (Finnish: *Ukko ylijumala*), the supreme god of sky, weather, and thunder in Finnish mythology. Just as Ukko ruled over the other gods from above, the Ukko Method places an AI "overseer" in charge of orchestrating autonomous agents.

---

## Quick Start (5 minutes)

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

**If you're starting a new project:**
```bash
# Create your project folder
mkdir my-awesome-project
cd my-awesome-project
git init
```

**Copy the Ukko files:**

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

**Verify you have the files:**
```bash
# You should see: .ukko/  CLAUDE.md  ukko.py  setup.py
ls -la
```

### Step 3: Start the Planning Phase

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

### Step 4: Run the Execution Phase

Once planning is complete, start the build:

```bash
# Recommended: Testing mode (one task at a time, you review each)
# First, edit .ukko/config.yaml and set: mode: testing
python ukko.py run

# Or: Auto mode (runs continuously until done)
python ukko.py
```

**What happens in each generation:**
1. Claude reads the PRD and finds the next unchecked task
2. If it faces a tough decision, it spawns parallel "swarm" agents to explore options
3. It picks the best approach and implements it
4. It checks off the task and commits the code
5. The script spawns the next generation (or waits for you in testing mode)

### Step 5: Monitor Progress

Check how things are going:

```bash
python ukko.py status
```

You'll see:
- Current phase (planning or execution)
- How many tasks are complete
- Any conflicts that need your attention

---

## Installing Claude Code CLI

The Ukko Method requires [Claude Code](https://claude.ai/code), Anthropic's CLI tool.

**Install via npm:**
```bash
npm install -g @anthropic-ai/claude-code
```

**Verify it's installed:**
```bash
claude --version
```

**First-time setup:**
```bash
claude
# Follow the prompts to authenticate with your Anthropic account
```

You need an Anthropic account with API access. Claude Code uses your API credits.

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

### Colors look weird / show escape codes

Your terminal might not support ANSI colors. The scripts will still work, just without pretty colors. Try using:
- Windows: Windows Terminal (not cmd.exe)
- macOS: Terminal.app or iTerm2
- Linux: Most modern terminals work fine

### "CONFLICT.md detected"

An Ukko generation found a problem it couldn't solve. Read `.ukko/CONFLICT.md` to see what's wrong, fix the issue, delete the file, and run again.

---

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

- **Ctrl+C** stops the loop at any time (safe, won't corrupt anything)
- If an Ukko detects an unresolvable issue, it creates `.ukko/CONFLICT.md` and exits
- The orchestrator pauses for human review when conflicts are detected
- Delete `CONFLICT.md` after resolving to continue

---

## Credits

Built on:
- **Ralph Loops** - Persistent iteration with hard context resets
- **Boris Method** - Parallel instances with human selection

The Ukko insight: Move selection from human to AI, and apply parallel comparison at the **decision layer** instead of the **implementation layer** for massive cost/time savings while maintaining full autonomy.
