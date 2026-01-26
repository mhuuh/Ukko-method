#!/bin/bash
#
# Ukko Method - Setup Script
#
# This script reads config.yaml and templates values into CLAUDE.md
# Run this after modifying config.yaml to apply your settings.
#
# Usage:
#   ./setup.sh
#

set -e

UKKO_DIR=".ukko"
CONFIG_FILE="$UKKO_DIR/config.yaml"
CLAUDE_MD="CLAUDE.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse config value (handles nested YAML simply)
get_config() {
    local key=$1
    grep -E "^\s*$key:" "$CONFIG_FILE" 2>/dev/null | sed 's/^[^:]*: *//' | tr -d '"' | xargs
}

# Parse array values from config
get_config_array() {
    local key=$1
    local in_section=false
    local result=""

    while IFS= read -r line; do
        if [[ "$line" =~ ^${key}: ]]; then
            in_section=true
            continue
        fi
        if $in_section; then
            if [[ "$line" =~ ^[a-z] ]] || [[ -z "$line" ]]; then
                break
            fi
            if [[ "$line" =~ ^[[:space:]]*-[[:space:]]*(.*) ]]; then
                item="${BASH_REMATCH[1]}"
                item=$(echo "$item" | tr -d '"')
                result+="- $item\n"
            fi
        fi
    done < "$CONFIG_FILE"

    echo -e "$result"
}

echo -e "${BLUE}=== Ukko Method Setup ===${NC}"
echo ""

# Check files exist
if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}Error: $CONFIG_FILE not found${NC}"
    exit 1
fi

if [ ! -f "$CLAUDE_MD" ]; then
    echo -e "${RED}Error: $CLAUDE_MD not found${NC}"
    exit 1
fi

# Read config values
AGENTS_PER_SWARM=$(get_config "agents_per_swarm")
TARGET_SWARMS=$(get_config "target_swarms_per_task")
DEFAULT_MODEL=$(get_config "default_agent_model")

echo "Configuration detected:"
echo "  - Agents per swarm: ${AGENTS_PER_SWARM:-5}"
echo "  - Target swarms per task: ${TARGET_SWARMS:-2-5}"
echo "  - Default agent model: ${DEFAULT_MODEL:-auto}"
echo ""

# Template values into CLAUDE.md
# We use placeholder patterns that can be replaced

# Backup original
cp "$CLAUDE_MD" "$CLAUDE_MD.bak"

# Replace the agents count in swarm instructions
if [ -n "$AGENTS_PER_SWARM" ]; then
    sed -i "s/launch [0-9]* parallel agents/launch $AGENTS_PER_SWARM parallel agents/g" "$CLAUDE_MD"
    sed -i "s/Swarm agent 1 of [0-9]*/Swarm agent 1 of $AGENTS_PER_SWARM/g" "$CLAUDE_MD"
fi

# Replace target swarms per task
if [ -n "$TARGET_SWARMS" ]; then
    sed -i "s/Target: [0-9]*-[0-9]* swarm launches/Target: $TARGET_SWARMS swarm launches/g" "$CLAUDE_MD"
fi

echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "CLAUDE.md has been updated with your configuration."
echo "A backup was saved to CLAUDE.md.bak"
echo ""
echo "Next steps:"
echo "  1. Run './ukko.sh plan' to start planning phase"
echo "  2. Or './ukko.sh status' to check current state"
