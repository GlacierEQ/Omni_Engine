# Operational Recommendations

1. **Establish data drop zones.** Populate `data/fileboss`, `data/pdfs`, and
   `data/transcripts` with synchronized evidence exports so the default
   connectors can ingest new material continuously.
2. **Schedule ingestion cycles.** Run the operator dashboard or invoke
   `OperatorCore.run_cycle()` on an hourly cadence to maintain up-to-date memory
   layers for downstream agents.
3. **Monitor alerts.** Inspect the `ingestion_alerts` layer for PDF parsing or
   transcript errors and remediate corrupted sources immediately.
4. **Expand coverage.** Implement bespoke connectors for calendaring systems,
   case management APIs, or communication archives to extend situational
   awareness across all custodial intelligence feeds.
5. **Automate reporting.** Export the `AuditReport` artefacts to your analytics
   stack to track throughput trends and verify compliance objectives over time.
