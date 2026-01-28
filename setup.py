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

    print("Configuration detected:")
    print(f"  - Agents per swarm: {agents_per_swarm or '5'}")
    print(f"  - Target swarms per task: {target_swarms or '2-5'}")
    print(f"  - Default agent model: {default_model or 'auto'}")
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

    # Write updated content
    CLAUDE_MD.write_text(content, encoding="utf-8")

    print(f"{Colors.GREEN}Setup complete!{Colors.NC}")
    print()
    print("CLAUDE.md has been updated with your configuration.")
    print(f"A backup was saved to {backup_path}")
    print()
    print("Next steps:")
    print("  1. Run 'python ukko.py plan' to start planning phase")
    print("  2. Or 'python ukko.py status' to check current state")


if __name__ == "__main__":
    main()
