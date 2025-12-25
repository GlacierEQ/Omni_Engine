echo -e "slug\tstatus\tdetail" > /home/user/mcp_audit/report.tsv
while read slug; do
  raw="$(mcp "$slug" 2>&1)"
  if echo "$raw" | grep -qi "Unauthorized"; then
    echo -e "${slug}\tUNAUTHORIZED\tOAuth" >> /home/user/mcp_audit/report.tsv
  elif echo "$raw" | grep -qi "500"; then
    echo -e "${slug}\tERROR\t500" >> /home/user/mcp_audit/report.tsv
  elif echo "$raw" | grep -qi "^error:"; then
    echo -e "${slug}\tERROR\tAPI" >> /home/user/mcp_audit/report.tsv
  else
    echo -e "${slug}\tCONNECTED\tOK" >> /home/user/mcp_audit/report.tsv
  fi
done < /home/user/mcp_audit/all_slugs.txt
