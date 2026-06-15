# Evidence Collection Sheet

## Required screenshots
- Langfuse trace list with >= 10 traces
- One full trace waterfall
- JSON logs showing correlation_id
- Log line with PII redaction
- Dashboard with 6 panels
- Alert rules with runbook link

## Local verification
- `python scripts/validate_logs.py` => 100/100 after running the sample queries.
- `data/logs.jsonl` contains 10 unique request IDs and redacted sample PII.
- `GET /dashboard` renders the 6 required Layer-2 panels from `/metrics`.
- `config/alert_rules.yaml` contains 3 alert rules with runbook links to `docs/alerts.md`.
- Langfuse screenshots require `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` in `.env`, then running `python scripts/load_test.py --concurrency 5`.

## Optional screenshots
- Incident before/after fix
- Cost comparison before/after optimization
- Auto-instrumentation proof
