# Evidence Collection Sheet

## Current progress snapshot (2026-04-20)
- [x] JSON logs showing correlation_id
- [x] Log line with PII redaction
- [x] Langfuse trace list with >= 10 traces (`extras/langfuse_trace.png`)
- [ ] One full trace waterfall
- [ ] Dashboard with 6 panels
- [ ] Alert rules with runbook link screenshot

Verified from local run:
- validate_logs.py: 100/100
- Missing required fields: 0
- Missing enrichment fields: 0
- Potential PII leaks: 0

## Remaining items to submit
1. Capture one full trace waterfall screenshot.
2. Capture dashboard screenshot with all 6 required panels.
3. Capture alert rule screenshot showing runbook links.

## Required screenshots
- Langfuse trace list with >= 10 traces
- One full trace waterfall
- JSON logs showing correlation_id
- Log line with PII redaction
- Dashboard with 6 panels
- Alert rules with runbook link

## How to collect each required screenshot

### 1) Langfuse traces (>=10)
1. Create `.env` from `.env.example` and set:
	- `LANGFUSE_PUBLIC_KEY`
	- `LANGFUSE_SECRET_KEY`
	- `LANGFUSE_HOST` (default cloud URL is already valid)
2. Start app:
	- `d:/AI_thucchien/Day13/Lab13-Observability/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 1009`
3. Generate traffic:
	- `d:/AI_thucchien/Day13/Lab13-Observability/.venv/Scripts/python.exe scripts/load_test.py --concurrency 3`
4. Open Langfuse UI and capture:
	- Trace list count >= 10
	- One full trace waterfall

### 2) JSON logs with correlation_id
Use one of these as evidence sources:
- Response header screenshot showing `x-request-id`
- Log lines in `data/logs.jsonl` where `request_received` and `response_sent` share same `correlation_id`

Quick command:
- `Get-Content data/logs.jsonl -Tail 30`

### 3) PII redaction evidence
Find one log line with `REDACTED_*` marker.

Quick command:
- `Select-String -Path data/logs.jsonl -Pattern "REDACTED" | Select-Object -First 5`

### 4) Dashboard 6 panels
Open `docs/dashboard-live.html` and use it as screenshot source.

Required panels (from dashboard spec):
- Latency P50/P95/P99
- Traffic (request count or QPS)
- Error rate with breakdown
- Cost over time
- Tokens in/out
- Quality proxy

Also ensure:
- Default time range 1h
- Auto-refresh 15-30s
- SLO/threshold lines visible
- Units labeled

### 5) Alert rules screenshot
Capture `config/alert_rules.yaml` or alert UI showing runbook links:
- `high_latency_p95`
- `high_error_rate`
- `cost_budget_spike`

## Optional screenshots
- Incident before/after fix
- Cost comparison before/after optimization
- Auto-instrumentation proof

## Incident drill commands (PowerShell-safe)
Use `Invoke-RestMethod` instead of `curl` in PowerShell to avoid interactive warning prompts.

1. `Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:1009/incidents/rag_slow/enable"`
2. `d:/AI_thucchien/Day13/Lab13-Observability/.venv/Scripts/python.exe scripts/load_test.py --concurrency 2`
3. `Invoke-RestMethod -Uri "http://127.0.0.1:1009/metrics"`
4. `Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:1009/incidents/rag_slow/disable"`
