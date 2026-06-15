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
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: `docs/evidence/correlation_id.png`
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: `docs/evidence/REDACTED_EMAIL.png`, `docs/evidence/REDACTED_PHONE_VN.png`, `docs/evidence/REDACTED_CREDIT_CARD.png`
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: `docs/evidence/langfuse-trace-waterfall.png`
- [TRACE_WATERFALL_EXPLANATION]: The agent trace contains the top-level `LabAgent.run` span plus nested `retrieve` and `FakeLLM.generate` observations, so `rag_slow` can be localized to retrieval while normal generation remains stable.

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: `docs/evidence/Dashboard bình thường.png`
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | 151ms local sample |
| Error Rate | < 2% | 28d | 0.00% local sample |
| Cost Budget | < $2.5/day | 1d | $0.0212 local sample |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: `docs/evidence/alert_rules_yaml.png`, `docs/evidence/alerts_md.png`
- [SAMPLE_RUNBOOK_LINK]: `docs/alerts.md#1-high-latency-p95`

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: P95 latency rises above the normal ~150ms baseline when retrieval delay is injected.
- [ROOT_CAUSE_PROVED_BY]: `docs/evidence/incident-rag-slow-load-test.png`, `docs/evidence/Dashboard sau khi bật rag_slow.png`, and `docs/evidence/langfuse-trace-waterfall.png`
- [FIX_ACTION]: Disable `rag_slow`, inspect retrieval backend, and fall back to a cached or smaller retrieval set.
- [PREVENTIVE_MEASURE]: Keep the `high_latency_p95` alert and use trace span tags to separate RAG latency from LLM latency.

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: Implemented recursive PII scrubbing and log processor redaction.
- [EVIDENCE_LINK]: `docs/evidence/git-commit.png`

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: Added request context enrichment and nested trace observations for RAG and LLM steps.
- [EVIDENCE_LINK]: `docs/evidence/git-commit.png`

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: Finalized SLO and alert runbook configuration.
- [EVIDENCE_LINK]: `docs/evidence/git-commit.png`

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: Added `/dashboard` with latency, traffic, error-rate, cost, token, and quality panels.
- [EVIDENCE_LINK]: `docs/evidence/git-commit.png`

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: Added test coverage and ran `pytest` plus `scripts/validate_logs.py`.
- [EVIDENCE_LINK]: `docs/evidence/git-commit.png`

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: Not claimed
- [BONUS_AUDIT_LOGS]: Not claimed
- [BONUS_CUSTOM_METRIC]: Error-rate percentage and total error count added to `/metrics`
