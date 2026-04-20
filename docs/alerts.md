# Alert Rules and Runbooks

Use these rules with app port `1009` in this lab setup.

## 1. High latency P95
- Severity: P2
- Trigger: `latency_p95_ms > 2000 for 5m`
- Impact: tail latency breaches SLO
- First checks:
  1. Open top slow traces in the last 1h
  2. Compare RAG span vs LLM span
  3. Check if incident toggle `rag_slow` is enabled
- Mitigation:
  - truncate long queries
  - fallback retrieval source
  - lower prompt size
- Fast test (lab):
  1. `py scripts/inject_incident.py --scenario rag_slow`
  2. `py scripts/load_test.py --concurrency 3`
  3. `Invoke-RestMethod -Uri "http://127.0.0.1:1009/metrics"`
  4. Confirm `latency_p95` rises significantly (typically > 2000ms during incident)
  5. `py scripts/inject_incident.py --scenario rag_slow --disable`

## 2. High error rate
- Severity: P1
- Trigger: `error_rate_pct > 5 for 5m`
- Impact: users receive failed responses
- First checks:
  1. Group logs by `error_type`
  2. Inspect failed traces
  3. Determine whether failures are LLM, tool, or schema related
- Mitigation:
  - rollback latest change
  - disable failing tool
  - retry with fallback model
- Fast test (lab):
  1. `py scripts/inject_incident.py --scenario tool_fail`
  2. `py scripts/load_test.py --concurrency 3`
  3. Check logs for `request_failed` and `error_type`
  4. Error rate should spike because `/chat` returns 500
  5. `py scripts/inject_incident.py --scenario tool_fail --disable`

## 3. Cost budget spike
- Severity: P2
- Trigger: `hourly_cost_usd > 1.5x_baseline for 15m`
- Impact: burn rate exceeds budget
- First checks:
  1. Split traces by feature and model
  2. Compare tokens_in/tokens_out
  3. Check if `cost_spike` incident was enabled
- Mitigation:
  - shorten prompts
  - route easy requests to cheaper model
  - apply prompt cache
- Fast test (lab):
  1. `py scripts/inject_incident.py --scenario cost_spike`
  2. `py scripts/load_test.py --concurrency 3`
  3. `Invoke-RestMethod -Uri "http://127.0.0.1:1009/metrics"`
  4. Compare cost and tokens against baseline snapshot
  5. `py scripts/inject_incident.py --scenario cost_spike --disable`

## Evidence checklist for submission
- Screenshot of `config/alert_rules.yaml` showing 3 rules and runbook links
- Screenshot of one triggered scenario (metrics/logs/traces)
- Short note in report about root cause + mitigation taken from this runbook
