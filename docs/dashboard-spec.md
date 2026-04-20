# Dashboard Spec

## Quick start (local live dashboard)
1. Start API on port 1009:
	- `d:/AI_thucchien/Day13/Lab13-Observability/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 1009`
2. Generate requests:
	- `py scripts/load_test.py --concurrency 3`
3. Open the dashboard file in browser:
	- `docs/dashboard-live.html`
4. Keep auto refresh at 15-30s and time range at 1h when taking screenshot.

Required Layer-2 panels:
1. Latency P50/P95/P99
2. Traffic (request count or QPS)
3. Error rate with breakdown
4. Cost over time
5. Tokens in/out
6. Quality proxy (heuristic, thumbs, or regenerate rate)

Quality bar:
- default time range = 1 hour
- auto refresh every 15-30 seconds
- visible threshold/SLO line
- units clearly labeled
- no more than 6-8 panels on the main layer
