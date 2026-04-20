# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 0. Current Progress Snapshot
- [x] `validate_logs.py` passes with score 100/100
- [x] Correlation IDs appear in JSON logs
- [x] PII redaction appears in JSON logs
- [x] Langfuse tracing is enabled in the app
- [x] Langfuse trace list screenshot with >= 10 traces
- [ ] One full trace waterfall screenshot
- [ ] Dashboard screenshot with 6 panels
- [ ] Alert rules screenshot with runbook link

## 1. Team Metadata
- [GROUP_NAME]: [TODO_FILL]
- [REPO_URL]: [TODO_FILL]
- [MEMBERS]:
  - Member A: [Name] | Role: Logging & PII
  - Member B: [Name] | Role: Tracing & Enrichment
  - Member C: [Name] | Role: SLO & Alerts
  - Member D: [Name] | Role: Load Test & Dashboard
  - Member E: [Name] | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: >= 10 (evidence: `extras/langfuse_trace.png`)
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [TODO_FILL_AFTER_WATERFALL_CAPTURE]
- [TRACE_WATERFALL_EXPLANATION]: Example explanation: the `run` span shows stable agent latency (~150ms baseline), while incident `rag_slow` reproduces a much longer retrieval stage.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 150ms (local run) |
| Error Rate | < 2% | 28d | 0% (local run) |
| Cost Budget | < $2.5/day | 1d | [TODO_FILL_FROM_DASHBOARD] |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [Path to image]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md](docs/alerts.md)

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: (e.g., rag_slow)
- [SYMPTOMS_OBSERVED]: p95/p99 latency increased significantly during `rag_slow`; baseline requests remained healthy before injection.
- [ROOT_CAUSE_PROVED_BY]: Trace waterfall (slow retrieval span) + correlated logs with same `correlation_id` (example pair lines 383-384 in `data/logs.jsonl`).
- [FIX_ACTION]: Disabled incident toggle and reverted to normal retrieval path.
- [PREVENTIVE_MEASURE]: Keep latency alert on p95, monitor top slow traces, and enforce prompt/retrieval size guardrails.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: Implemented structured logging context and PII redaction validation.
- [EVIDENCE_LINK]: (Link to specific commit or PR)

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: Enabled Langfuse tracing and trace metadata enrichment.
- [EVIDENCE_LINK]: 

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: Defined SLO/alert thresholds and runbook mapping.
- [EVIDENCE_LINK]: 

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: Executed load tests and incident drills for evidence collection.
- [EVIDENCE_LINK]: 

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: Compiled dashboard/report artifacts and demo narrative.
- [EVIDENCE_LINK]: 

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)
