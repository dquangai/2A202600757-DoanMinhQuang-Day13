# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: 2A202600757 - Doan Minh Quang - Day 13
- [REPO_URL]: Local submission repository
- [MEMBERS]:
  - Member A: Doan Minh Quang | Role: Logging & PII
  - Member B: Doan Minh Quang | Role: Tracing & Enrichment
  - Member C: Doan Minh Quang | Role: SLO & Alerts
  - Member D: Doan Minh Quang | Role: Load Test & Dashboard
  - Member E: Doan Minh Quang | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: 100/100
- [TOTAL_TRACES_COUNT]: 10 expected after running `python scripts/load_test.py --concurrency 5` with `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` configured
- [PII_LEAKS_FOUND]: 0

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: `data/logs.jsonl` contains `req-00000001` through `req-0000000a`
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: `data/logs.jsonl` shows `[REDACTED_EMAIL]`, `[REDACTED_PHONE_VN]`, and `[REDACTED_CREDIT_CARD]`
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: Capture from Langfuse after keys are configured
- [TRACE_WATERFALL_EXPLANATION]: The agent trace contains the top-level `LabAgent.run` span plus nested `retrieve` and `FakeLLM.generate` observations, so `rag_slow` can be localized to retrieval while normal generation remains stable.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: Open `http://127.0.0.1:8000/dashboard`
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 151ms local sample |
| Error Rate | < 2% | 28d | 0.00% local sample |
| Cost Budget | < $2.5/day | 1d | $0.0212 local sample |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: `config/alert_rules.yaml`
- [SAMPLE_RUNBOOK_LINK]: `docs/alerts.md#1-high-latency-p95`

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: P95 latency rises above the normal ~150ms baseline when retrieval delay is injected.
- [ROOT_CAUSE_PROVED_BY]: Trace waterfall should show the nested `retrieve` span consuming most latency; logs retain the same `correlation_id` for request and response.
- [FIX_ACTION]: Disable `rag_slow`, inspect retrieval backend, and fall back to a cached or smaller retrieval set.
- [PREVENTIVE_MEASURE]: Keep the `high_latency_p95` alert and use trace span tags to separate RAG latency from LLM latency.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: Implemented recursive PII scrubbing and log processor redaction.
- [EVIDENCE_LINK]: Local diff in `app/pii.py` and `app/logging_config.py`

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: Added request context enrichment and nested trace observations for RAG and LLM steps.
- [EVIDENCE_LINK]: Local diff in `app/main.py`, `app/mock_rag.py`, and `app/mock_llm.py`

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: Finalized SLO and alert runbook configuration.
- [EVIDENCE_LINK]: Local diff in `config/slo.yaml`, `config/alert_rules.yaml`, and `docs/alerts.md`

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: Added `/dashboard` with latency, traffic, error-rate, cost, token, and quality panels.
- [EVIDENCE_LINK]: Local diff in `app/dashboard.py` and `docs/dashboard-spec.md`

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: Added test coverage and ran `pytest` plus `scripts/validate_logs.py`.
- [EVIDENCE_LINK]: Local diff in `tests/test_app_observability.py`, `tests/test_metrics.py`, and `tests/test_pii.py`

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Not claimed
- [BONUS_AUDIT_LOGS]: Not claimed
- [BONUS_CUSTOM_METRIC]: Error-rate percentage and total error count added to `/metrics`
