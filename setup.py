#!/usr/bin/env python3
"""
Ukko Method - Setup Script

This script reads config.yaml and templates values into CLAUDE.md
Run this after modifying config.yaml to apply your settings.

Usage:
    python setup.py
"""

import os
import re
import shutil
import sys
from pathlib import Path

# Enable ANSI colors on Windows
if sys.platform == "win32":
    os.system("")  # Enables ANSI escape sequences in Windows terminal

# Colors for output
class Colors:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[0;34m"
    NC = "\033[0m"  # No Color


# Paths
UKKO_DIR = Path(".ukko")
CONFIG_FILE = UKKO_DIR / "config.yaml"
CLAUDE_MD = Path("CLAUDE.md")


def get_config(key: str) -> str:
    """Parse a simple key: value from config.yaml"""
    if not CONFIG_FILE.exists():
        return ""

    content = CONFIG_FILE.read_text(encoding="utf-8")
    for line in content.splitlines():
        # Match lines like "key: value" or "  key: value"
        match = re.match(rf'^\s*{re.escape(key)}:\s*(.+)$', line)
        if match:
            value = match.group(1).strip().strip('"').strip("'")
            return value
    return ""


def get_config_list(key: str) -> list:
    """Parse a YAML list from config.yaml (e.g., decision_triggers)"""
    if not CONFIG_FILE.exists():
        return []

    content = CONFIG_FILE.read_text(encoding="utf-8")
    lines = content.splitlines()
    items = []
    in_list = False

    for line in lines:
        # Check if we hit the key
        if re.match(rf'^{re.escape(key)}:\s*$', line):
            in_list = True
            continue

        if in_list:
            # Check for list item (starts with "  - ")
            match = re.match(r'^\s+-\s+"?([^"]+)"?\s*$', line)
            if match:
                items.append(match.group(1).strip())
            # If we hit a non-indented line that's not empty, we're done
            elif line.strip() and not line.startswith(' '):
                break

    return items


def main():
    print(f"{Colors.BLUE}=== Ukko Method Setup ==={Colors.NC}")
    print()

    # Check files exist
    if not CONFIG_FILE.exists():
        print(f"{Colors.RED}Error: {CONFIG_FILE} not found{Colors.NC}")
        sys.exit(1)

    if not CLAUDE_MD.exists():
        print(f"{Colors.RED}Error: {CLAUDE_MD} not found{Colors.NC}")
        sys.exit(1)

    # Read config values
    agents_per_swarm = get_config("agents_per_swarm")
    target_swarms = get_config("target_swarms_per_task")
    default_model = get_config("default_agent_model")
    decision_triggers = get_config_list("decision_triggers")

    # Also read ukko_model (used by ukko.py, not templated)
    ukko_model = get_config("ukko_model")

    print("Configuration detected:")
    print(f"  - Ukko model: {ukko_model or '(default)'}")
    print(f"  - Default agent model: {default_model or 'auto'}")
    print(f"  - Agents per swarm: {agents_per_swarm or '5'}")
    print(f"  - Target swarms per task: {target_swarms or '2-5'}")
    print(f"  - Decision triggers: {len(decision_triggers)} items")
    for trigger in decision_triggers:
        print(f"      - {trigger}")
    print()

    # Backup original
    backup_path = CLAUDE_MD.with_suffix(".md.bak")
    shutil.copy(CLAUDE_MD, backup_path)

    # Read CLAUDE.md content
    content = CLAUDE_MD.read_text(encoding="utf-8")

    # Replace the agents count in swarm instructions
    if agents_per_swarm:
        content = re.sub(
            r'launch \d+ parallel agents',
            f'launch {agents_per_swarm} parallel agents',
            content
        )
        content = re.sub(
            r'Swarm agent 1 of \d+',
            f'Swarm agent 1 of {agents_per_swarm}',
            content
        )

    # Replace target swarms per task
    if target_swarms:
        content = re.sub(
            r'Target: \d+-\d+ swarm launches',
            f'Target: {target_swarms} swarm launches',
            content
        )

    # Replace decision triggers list
    if decision_triggers:
        # Build the new triggers list
        triggers_text = "Launch parallel agents when you encounter:\n"
        for trigger in decision_triggers:
            # Capitalize first letter for display
            display_trigger = trigger[0].upper() + trigger[1:] if trigger else trigger
            triggers_text += f"- {display_trigger}\n"
        triggers_text = triggers_text.rstrip('\n')

        # Match the existing triggers section (from "Launch parallel agents" to the line before "**Do NOT swarm")
        content = re.sub(
            r'Launch parallel agents when you encounter:\n(?:- [^\n]+\n)+',
            triggers_text + '\n',
            content
        )

    # Handle default agent model in swarm instructions
    # Original guidance text (for restoring when set to "auto")
    original_model_guidance = """**Model selection:**
- **haiku**: Simple decisions, clear constraints, speed matters
- **sonnet**: Most decisions, balanced quality/cost
- **opus**: Complex architectural decisions, high uncertainty
"""

    if default_model and default_model.lower() != "auto":
        # Replace the model placeholder in the Task invocation example
        content = re.sub(
            r'<parameter name="model">\[haiku\|sonnet\|opus\]</parameter>',
            f'<parameter name="model">{default_model}</parameter>',
            content
        )
        # Also replace any previously set specific model
        content = re.sub(
            r'<parameter name="model">(haiku|sonnet|opus)</parameter>',
            f'<parameter name="model">{default_model}</parameter>',
            content
        )
        # Update the model selection guidance (from original or from previous config)
        content = re.sub(
            r'\*\*Model selection:\*\*.*?(?=\n\n## Evaluating)',
            f'**Model selection:** Using `{default_model}` (configured in config.yaml)',
            content,
            flags=re.DOTALL
        )
    else:
        # Restore original guidance if set to "auto"
        content = re.sub(
            r'<parameter name="model">(haiku|sonnet|opus)</parameter>',
            '<parameter name="model">[haiku|sonnet|opus]</parameter>',
            content
        )
        content = re.sub(
            r'\*\*Model selection:\*\*.*?(?=\n\n## Evaluating)',
            original_model_guidance.rstrip(),
            content,
            flags=re.DOTALL
        )

    # Write updated content
    CLAUDE_MD.write_text(content, encoding="utf-8")

    print(f"{Colors.GREEN}Setup complete!{Colors.NC}")
    print()
    print("Applied to CLAUDE.md:")
    if agents_per_swarm:
        print(f"  {Colors.GREEN}*{Colors.NC} Agents per swarm: {agents_per_swarm}")
    if target_swarms:
        print(f"  {Colors.GREEN}*{Colors.NC} Target swarms per task: {target_swarms}")
    if decision_triggers:
        print(f"  {Colors.GREEN}*{Colors.NC} Decision triggers: {len(decision_triggers)} items")
    if default_model and default_model.lower() != "auto":
        print(f"  {Colors.GREEN}*{Colors.NC} Default agent model: {default_model}")
    else:
        print(f"  {Colors.GREEN}*{Colors.NC} Default agent model: auto (Ukko chooses per-swarm)")

    if ukko_model:
        print()
        print(f"Note: ukko.py will use --model {ukko_model}")
    print()
    print(f"A backup was saved to {backup_path}")
    print()
    print("Next steps:")
    print("  1. Run 'python ukko.py plan' to start planning phase")
    print("  2. Or 'python ukko.py status' to check current state")


if __name__ == "__main__":
    main()
