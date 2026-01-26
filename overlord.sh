#!/bin/bash
#
# Overlord Method - Orchestrator Script
#
# Usage:
#   ./overlord.sh          - Run in mode specified by config (auto or testing)
#   ./overlord.sh run      - Run a single generation (for testing mode)
#   ./overlord.sh plan     - Start planning phase
#   ./overlord.sh status   - Show current progress
#

set -e

OVERLORD_DIR=".overlord"
CONFIG_FILE="$OVERLORD_DIR/config.yaml"
PRD_FILE="$OVERLORD_DIR/PRD.md"
CONFLICT_FILE="$OVERLORD_DIR/CONFLICT.md"
PLANNING_GUIDE="$OVERLORD_DIR/planning/planning-guide.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse config value
get_config() {
    local key=$1
    grep "^$key:" "$CONFIG_FILE" 2>/dev/null | sed 's/^[^:]*: *//' | tr -d '"'
}

# Check if planning phase is needed
is_planning_phase() {
    [ -f "$PLANNING_GUIDE" ]
}

# Check for conflicts
has_conflict() {
    [ -f "$CONFLICT_FILE" ]
}

# Count completed and total tasks
get_progress() {
    if [ -f "$PRD_FILE" ]; then
        local total=$(grep -c '^\- \[.\]' "$PRD_FILE" 2>/dev/null || echo 0)
        local done=$(grep -c '^\- \[x\]' "$PRD_FILE" 2>/dev/null || echo 0)
        echo "$done/$total"
    else
        echo "0/0"
    fi
}

# Check if all tasks complete
all_tasks_complete() {
    if [ -f "$PRD_FILE" ]; then
        local remaining=$(grep -c '^\- \[ \]' "$PRD_FILE" 2>/dev/null || echo 0)
        [ "$remaining" -eq 0 ]
    else
        return 1
    fi
}

# Run a single Overlord generation
run_generation() {
    echo -e "${BLUE}Starting Overlord generation...${NC}"

    # Check for conflicts first
    if has_conflict; then
        echo -e "${RED}CONFLICT DETECTED${NC}"
        echo "A previous Overlord flagged an issue that needs human review:"
        echo "---"
        cat "$CONFLICT_FILE"
        echo "---"
        echo "Resolve the conflict and delete $CONFLICT_FILE to continue."
        exit 1
    fi

    # Run Claude Code
    # The CLAUDE.md file will instruct it to read the appropriate guides
    claude --print "You are an Overlord. Read CLAUDE.md and proceed with your phase."

    echo -e "${GREEN}Generation complete.${NC}"
}

# Show status
show_status() {
    echo -e "${BLUE}=== Overlord Method Status ===${NC}"
    echo ""

    if is_planning_phase; then
        echo -e "Phase: ${YELLOW}PLANNING${NC}"
        echo "Run './overlord.sh plan' to start planning."
    else
        echo -e "Phase: ${GREEN}EXECUTION${NC}"
        echo -e "Progress: $(get_progress) tasks complete"

        if all_tasks_complete; then
            echo -e "${GREEN}All tasks complete!${NC}"
        fi
    fi

    if has_conflict; then
        echo ""
        echo -e "${RED}CONFLICT: Review $CONFLICT_FILE${NC}"
    fi

    echo ""
    echo "Mode: $(get_config 'mode')"
}

# Main execution
main() {
    # Ensure we're in a project with Overlord setup
    if [ ! -d "$OVERLORD_DIR" ]; then
        echo -e "${RED}Error: No $OVERLORD_DIR directory found.${NC}"
        echo "Are you in the right directory?"
        exit 1
    fi

    local command=${1:-""}
    local mode=$(get_config 'mode')

    case $command in
        "plan")
            if ! is_planning_phase; then
                echo -e "${YELLOW}Planning already complete. Nothing to do.${NC}"
                exit 0
            fi
            echo -e "${BLUE}Starting planning phase...${NC}"
            claude --print "You are the Planning Overlord. Read CLAUDE.md and begin planning."
            ;;

        "run")
            if is_planning_phase; then
                echo -e "${YELLOW}Still in planning phase. Run './overlord.sh plan' first.${NC}"
                exit 1
            fi
            run_generation
            ;;

        "status")
            show_status
            ;;

        "")
            # Default behavior based on mode
            if is_planning_phase; then
                echo -e "${YELLOW}Planning phase not complete.${NC}"
                echo "Run './overlord.sh plan' to start planning."
                exit 0
            fi

            if [ "$mode" = "testing" ]; then
                echo -e "${YELLOW}Testing mode: Run './overlord.sh run' for each generation.${NC}"
                show_status
            else
                # Auto mode - continuous loop
                echo -e "${BLUE}=== Overlord Method - Auto Mode ===${NC}"
                echo "Running continuous generations until complete."
                echo "Press Ctrl+C to stop at any time."
                echo ""

                while true; do
                    if all_tasks_complete; then
                        echo -e "${GREEN}All tasks complete! Exiting.${NC}"
                        break
                    fi

                    if has_conflict; then
                        echo -e "${RED}Conflict detected. Pausing for human review.${NC}"
                        break
                    fi

                    echo -e "Progress: $(get_progress)"
                    run_generation

                    # Brief pause between generations
                    sleep 2
                done
            fi
            ;;

        *)
            echo "Usage: ./overlord.sh [command]"
            echo ""
            echo "Commands:"
            echo "  plan     Start planning phase"
            echo "  run      Run a single generation (testing mode)"
            echo "  status   Show current progress"
            echo "  (none)   Run based on config mode (auto/testing)"
            ;;
    esac
}

main "$@"
