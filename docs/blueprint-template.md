# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 0. Current Progress Snapshot
- [x] `validate_logs.py` passes with score 100/100
- [x] Correlation IDs appear in JSON logs
- [x] PII redaction appears in JSON logs
- [x] Langfuse tracing is enabled in the app
- [x] Langfuse trace list screenshot with >= 10 traces
- [x] One full trace waterfall screenshot
- [x] Dashboard screenshot with 6 panels
- [x] Alert rules screenshot with runbook link

## 1. Team Metadata
- [GROUP_NAME]: 04
- [REPO_URL]: https://github.com/trannhatvi-ai/Lab13-Observability.git
- [MEMBERS]:
  - Member A: 2A202600312 Trần Thanh Phong | Role: Logging & PII
  - Member B: 2A202600064 Hoàng Đinh Duy Anh | Role: Tracing & Enrichment
  - Member C: 2A202600497 Trần Nhật Vĩ | Role: SLO & Alerts
  - Member D: 2A202600486 Nguyễn Tiến Huy Hoàng | Role: Load Test & Dashboard
---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: >= 10 (evidence: `extras/langfuse_trace.png`)
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: data/logs.jsonl (request/response correlation example around lines 383-384)
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: data/logs.jsonl (REDACTED example around line 381)
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: extras/waterfall.png
- [TRACE_WATERFALL_EXPLANATION]: Example explanation: the `run` span shows stable agent latency (~150ms baseline), while incident `rag_slow` reproduces a much longer retrieval stage.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: extras/dashboard.png
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 150ms (local run) |
| Error Rate | < 2% | 28d | 0% (local run) |
| Cost Budget | < $2.5/day | 1d | ~$0.0394 per test run snapshot (well below target) |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: extras/alert_rules.png
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md](docs/alerts.md)

Alert validation summary (local drill):
- `rag_slow`: request latency moved from ~0.31s baseline to ~2.6-5.3s.
- `tool_fail`: recent `request_failed` events observed, sample `error_type=RuntimeError`.
- `cost_spike`: cost and output tokens increased faster than baseline.
  - Baseline: `cost/req=0.00235`, `tokens_out/req=150.5`
  - Cost spike: `cost/req=0.00755`, `tokens_out/req=496.4`

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: p95/p99 latency increased significantly during `rag_slow`; baseline requests remained healthy before injection.
- [ROOT_CAUSE_PROVED_BY]: Trace waterfall (slow retrieval span) + correlated logs with same `correlation_id` (example pair lines 383-384 in `data/logs.jsonl`).
- [FIX_ACTION]: Disabled incident toggle and reverted to normal retrieval path.
- [PREVENTIVE_MEASURE]: Keep latency alert on p95, monitor top slow traces, and enforce prompt/retrieval size guardrails.

---

## 5. Individual Contributions & Evidence

### 2A202600312 Tran Thanh Phong
- [TASKS_COMPLETED]: Implemented structured logging context and PII redaction validation.
- [EVIDENCE_LINK]: https://github.com/trannhatvi-ai/Lab13-Observability/commit/82d1d91855df9401d48e1e4d1a4bf62fcb1144b2

### 2A202600064 Hoang Dinh Duy Anh
- [TASKS_COMPLETED]: Enabled Langfuse tracing and trace metadata enrichment.
- [EVIDENCE_LINK]: https://github.com/trannhatvi-ai/Lab13-Observability/commit/8284a58eab8284f9f4229981e8bdbf404d0edec0

### 2A202600497 Tran Nhat Vi
- [TASKS_COMPLETED]: Defined SLO/alert thresholds and runbook mapping.
- [EVIDENCE_LINK]: https://github.com/trannhatvi-ai/Lab13-Observability/commit/bdec42098e1480257dda598c80cdd53d3dca735e

### 2A202600486 Nguyen Tien Huy Hoang
- [TASKS_COMPLETED]: Executed load tests and incident drills for evidence collection.
- [EVIDENCE_LINK]: https://github.com/trannhatvi-ai/Lab13-Observability/commit/c3592b3902140b26a0dbf24b04da8e9359e9a71d

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
