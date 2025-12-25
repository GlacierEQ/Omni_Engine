#!/usr/bin/env bash
set -euo pipefail
OUT_DIR="/home/user/mcp_audit"
mkdir -p "$OUT_DIR"
SLUGS="$OUT_DIR/slugs.txt"
REPORT="$OUT_DIR/report.tsv"
: > "$SLUGS"
: > "$REPORT"

for page in $(seq 1 20); do
  json="$(mcp --json --page "$page" 2>/dev/null || true)"
  [[ -z "$json" ]] && break
  count="$(echo "$json" | jq -r '.servers | length' 2>/dev/null || echo 0)"
  if [[ "$count" == "0" ]]; then break; fi
  echo "$json" | jq -r '.servers[].slug' >> "$SLUGS"
done

sort -u "$SLUGS" -o "$SLUGS"
echo -e "slug\tstatus\tdetail" >> "$REPORT"

while IFS= read -r slug; do
  raw="$(mcp "$slug" 2>&1 || true)"
  if echo "$raw" | grep -qi "Unauthorized"; then
    echo -e "${slug}\tUNAUTHORIZED\tOAuth needed" >> "$REPORT"
  elif echo "$raw" | grep -qi "500 Internal Server Error"; then
    echo -e "${slug}\tERROR\t500 down" >> "$REPORT"
  elif echo "$raw" | grep -qi "^error:"; then
    msg="$(echo "$raw" | sed -n 's/^message:\s*//p' | head -n 1)"
    [[ -z "$msg" ]] && msg="error"
    echo -e "${slug}\tERROR\t${msg}" >> "$REPORT"
  else
    echo -e "${slug}\tCONNECTED\tOK" >> "$REPORT"
  fi
done < "$SLUGS"
echo "DONE"
