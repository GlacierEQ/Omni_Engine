#!/bin/bash
BATCH_ID=$(date +%Y%m%d-%H%M)
CASES=100
for i in $(seq 1 $CASES); do
  mcp overleaf bulk_tro_factory '{
    "cases": [{"petitioner": "Petitioner'$i'","respondent": "Respondent'$i'"}],
    "batch_id": "'$BATCH_ID'"
  }'
done
echo "Generated $CASES TROs - Batch: $BATCH_ID"
