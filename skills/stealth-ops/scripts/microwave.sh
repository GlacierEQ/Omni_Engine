#!/bin/bash
# Microwave Mode - High Speed Execution
TARGET_DIR=$1
shift
COMMANDS="$@"

echo "[☢️] MICROWAVE MODE ACTIVATED"
echo "[☢️] TARGET: $TARGET_DIR"

mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# Parallel execution of passed commands
for CMD in "$COMMANDS"; do
    eval "$CMD" &
done
wait

echo "[☢️] HEATING COMPLETE."
