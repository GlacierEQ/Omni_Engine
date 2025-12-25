#!/bin/bash
# Stealth Mode - Silent Execution
LOG_FILE="/tmp/stealth_ops.log"
echo "[🥷] STEALTH MODE ENGAGED" >> $LOG_FILE

# Run command in background with output suppressed
nohup "$@" > /dev/null 2>&1 &
PID=$!

echo "[🥷] OPERATION BACKGROUNDED (PID: $PID). LOGS AT $LOG_FILE"
