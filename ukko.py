#!/usr/bin/env python3
"""
Ukko Method - Orchestrator Script

Usage:
    python ukko.py          - Run in mode specified by config (auto or testing)
    python ukko.py run      - Run a single generation (for testing mode)
    python ukko.py plan     - Start planning phase
    python ukko.py status   - Show current progress
"""

import os
import re
import subprocess
import sys
import time
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
PRD_FILE = UKKO_DIR / "PRD.md"
CONFLICT_FILE = UKKO_DIR / "CONFLICT.md"
PLANNING_GUIDE = UKKO_DIR / "planning" / "planning-guide.md"


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


def is_planning_phase() -> bool:
    """Check if planning phase is needed"""
    return PLANNING_GUIDE.exists()


def has_conflict() -> bool:
    """Check for conflicts"""
    return CONFLICT_FILE.exists()


def get_progress() -> str:
    """Count completed and total tasks"""
    if not PRD_FILE.exists():
        return "0/0"

    content = PRD_FILE.read_text(encoding="utf-8")
    total = len(re.findall(r'^- \[.\]', content, re.MULTILINE))
    done = len(re.findall(r'^- \[x\]', content, re.MULTILINE))
    return f"{done}/{total}"


def all_tasks_complete() -> bool:
    """Check if all tasks are complete"""
    if not PRD_FILE.exists():
        return False

    content = PRD_FILE.read_text(encoding="utf-8")
    remaining = len(re.findall(r'^- \[ \]', content, re.MULTILINE))
    return remaining == 0


def run_claude(prompt: str) -> int:
    """Run Claude Code with the given prompt"""
    try:
        cmd = ["claude", "--print"]

        # Add model flag if configured
        ukko_model = get_config("ukko_model")
        if ukko_model:
            cmd.extend(["--model", ukko_model])

        cmd.append(prompt)

        result = subprocess.run(cmd, check=False)
        return result.returncode
    except FileNotFoundError:
        print(f"{Colors.RED}Error: 'claude' command not found.{Colors.NC}")
        print("Make sure Claude Code CLI is installed and in your PATH.")
        return 1


def run_generation():
    """Run a single Ukko generation"""
    print(f"{Colors.BLUE}Starting Ukko generation...{Colors.NC}")

    # Check for conflicts first
    if has_conflict():
        print(f"{Colors.RED}CONFLICT DETECTED{Colors.NC}")
        print("A previous Ukko flagged an issue that needs human review:")
        print("---")
        print(CONFLICT_FILE.read_text(encoding="utf-8"))
        print("---")
        print(f"Resolve the conflict and delete {CONFLICT_FILE} to continue.")
        sys.exit(1)

    # Run Claude Code
    run_claude("You are Ukko. Read CLAUDE.md and proceed with your phase.")

    print(f"{Colors.GREEN}Generation complete.{Colors.NC}")


def show_status():
    """Show current status"""
    print(f"{Colors.BLUE}=== Ukko Method Status ==={Colors.NC}")
    print()

    if is_planning_phase():
        print(f"Phase: {Colors.YELLOW}PLANNING{Colors.NC}")
        print("Run 'python ukko.py plan' to start planning.")
    else:
        print(f"Phase: {Colors.GREEN}EXECUTION{Colors.NC}")
        print(f"Progress: {get_progress()} tasks complete")

        if all_tasks_complete():
            print(f"{Colors.GREEN}All tasks complete!{Colors.NC}")

    if has_conflict():
        print()
        print(f"{Colors.RED}CONFLICT: Review {CONFLICT_FILE}{Colors.NC}")

    print()
    print(f"Mode: {get_config('mode')}")


def main():
    # Ensure we're in a project with Ukko setup
    if not UKKO_DIR.exists():
        print(f"{Colors.RED}Error: No {UKKO_DIR} directory found.{Colors.NC}")
        print("Are you in the right directory?")
        sys.exit(1)

    command = sys.argv[1] if len(sys.argv) > 1 else ""
    mode = get_config("mode")

    if command == "plan":
        if not is_planning_phase():
            print(f"{Colors.YELLOW}Planning already complete. Nothing to do.{Colors.NC}")
            sys.exit(0)
        print(f"{Colors.BLUE}Starting planning phase...{Colors.NC}")
        run_claude("You are the Planning Ukko. Read CLAUDE.md and begin planning.")

    elif command == "run":
        if is_planning_phase():
            print(f"{Colors.YELLOW}Still in planning phase. Run 'python ukko.py plan' first.{Colors.NC}")
            sys.exit(1)
        run_generation()

    elif command == "status":
        show_status()

    elif command == "":
        # Default behavior based on mode
        if is_planning_phase():
            print(f"{Colors.YELLOW}Planning phase not complete.{Colors.NC}")
            print("Run 'python ukko.py plan' to start planning.")
            sys.exit(0)

        if mode == "testing":
            print(f"{Colors.YELLOW}Testing mode: Run 'python ukko.py run' for each generation.{Colors.NC}")
            show_status()
        else:
            # Auto mode - continuous loop
            print(f"{Colors.BLUE}=== Ukko Method - Auto Mode ==={Colors.NC}")
            print("Running continuous generations until complete.")
            print("Press Ctrl+C to stop at any time.")
            print()

            try:
                while True:
                    if all_tasks_complete():
                        print(f"{Colors.GREEN}All tasks complete! Exiting.{Colors.NC}")
                        break

                    if has_conflict():
                        print(f"{Colors.RED}Conflict detected. Pausing for human review.{Colors.NC}")
                        break

                    print(f"Progress: {get_progress()}")
                    run_generation()

                    # Brief pause between generations
                    time.sleep(2)
            except KeyboardInterrupt:
                print()
                print(f"{Colors.YELLOW}Stopped by user.{Colors.NC}")

    else:
        print("Usage: python ukko.py [command]")
        print()
        print("Commands:")
        print("  plan     Start planning phase")
        print("  run      Run a single generation (testing mode)")
        print("  status   Show current progress")
        print("  (none)   Run based on config mode (auto/testing)")


if __name__ == "__main__":
    main()
