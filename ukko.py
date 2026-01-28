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
import shutil
import subprocess
import sys
import threading
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


def get_completed_count() -> int:
    """Count completed tasks in PRD.md"""
    if not PRD_FILE.exists():
        return 0
    content = PRD_FILE.read_text(encoding="utf-8")
    return len(re.findall(r'^- \[x\]', content, re.MULTILINE))


def watch_for_completion(process, initial_count: int, stop_event: threading.Event):
    """Watch PRD.md for task completion and terminate Claude when done."""
    while not stop_event.is_set() and process.poll() is None:
        time.sleep(2)  # Check every 2 seconds
        current_count = get_completed_count()
        if current_count > initial_count:
            # A task was completed! Wait for commit to finish, then terminate
            print(f"\n{Colors.GREEN}Task completed! Terminating session...{Colors.NC}")
            time.sleep(3)  # Give time for git commit
            process.terminate()
            break


def run_claude(prompt: str, interactive: bool = False) -> int:
    """Run Claude Code with the given prompt.

    Args:
        prompt: The prompt to send to Claude
        interactive: If True, run interactive session (for planning).
                     If False, run interactive but watch for task completion.
    """
    # Find claude executable
    claude_path = shutil.which("claude")
    if not claude_path:
        print(f"{Colors.RED}Error: 'claude' command not found.{Colors.NC}")
        print("Make sure Claude Code CLI is installed and in your PATH.")
        return 1

    cmd = [claude_path, "--dangerously-skip-permissions"]

    # Add model flag if configured
    ukko_model = get_config("ukko_model")
    if ukko_model:
        cmd.extend(["--model", ukko_model])

    cmd.append(prompt)

    if interactive:
        # Pure interactive mode for planning - no watching
        process = subprocess.Popen(cmd)
        process.wait()
        return process.returncode
    else:
        # Interactive mode with file watching for auto-termination
        initial_count = get_completed_count()
        stop_event = threading.Event()

        process = subprocess.Popen(cmd)

        # Start watcher thread
        watcher = threading.Thread(
            target=watch_for_completion,
            args=(process, initial_count, stop_event)
        )
        watcher.daemon = True
        watcher.start()

        try:
            process.wait()
        except KeyboardInterrupt:
            stop_event.set()
            process.terminate()
            raise

        stop_event.set()
        return process.returncode


def run_generation() -> bool:
    """Run a single Ukko generation.

    Returns:
        True if generation completed successfully, False on error.
    """
    print(f"{Colors.BLUE}Starting Ukko generation...{Colors.NC}")

    # Check for conflicts first
    if has_conflict():
        print(f"{Colors.RED}CONFLICT DETECTED{Colors.NC}")
        print("A previous Ukko flagged an issue that needs human review:")
        print("---")
        print(CONFLICT_FILE.read_text(encoding="utf-8"))
        print("---")
        print(f"Resolve the conflict and delete {CONFLICT_FILE} to continue.")
        return False

    # Run Claude Code
    exit_code = run_claude("You are Ukko. Read CLAUDE.md and proceed with your phase.")

    if exit_code != 0:
        print(f"{Colors.RED}Generation failed (exit code {exit_code}).{Colors.NC}")
        print("This may be due to API limits, network issues, or an error.")
        print("Check the output above for details.")
        return False

    print(f"{Colors.GREEN}Generation complete.{Colors.NC}")
    return True


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
        run_claude("You are the Planning Ukko. Read CLAUDE.md and begin planning.", interactive=True)

    elif command == "run":
        if is_planning_phase():
            print(f"{Colors.YELLOW}Still in planning phase. Run 'python ukko.py plan' first.{Colors.NC}")
            sys.exit(1)
        success = run_generation()
        sys.exit(0 if success else 1)

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
                    success = run_generation()

                    if not success:
                        print(f"{Colors.YELLOW}Stopping due to error. Fix the issue and run again.{Colors.NC}")
                        break

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
