#!/bin/bash
# HAWAII JEFS BULK eFILING PIPELINE
BATCH_ID=JEFS-$(date +%Y%m%d-%H%M)

echo "🚀 HAWAII JEFS BULK PIPELINE"
echo "Batch: $BATCH_ID"

# 1. Generate TRO batch
mcp overleaf bulk_tro_factory "{\"cases\":[...],\"batch_id\":\"$BATCH_ID\"}" > tro-batch.json

# 2. Compile PDFs
for project in $(jq -r '.projects[].project_id' tro-batch.json); do
  mcp overleaf compile_pdf "{\"project_id\":\"$project\"}" &
done
wait

# 3. JEFS Bulk eFiling
mcp overleaf bulk_jefs_efiling '{
  "documents": ["tro-001.pdf", "tro-002.pdf"],
  "hawaii_case_no": "FC-DA-24-XXXX",
  "attorney_bar": "12345"
}' > jefs-confirmation.json

echo "✅ JEFS Batch $BATCH_ID COMPLETE"
cat jefs-confirmation.json
