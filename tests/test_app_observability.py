import json
from pathlib import Path

from fastapi.testclient import TestClient

from app import audit
from app import logging_config
from app.metrics import reset
from app.main import app


def test_chat_logs_are_enriched_and_redacted() -> None:
    reset()
    log_path = Path("data/logs.jsonl")
    audit_path = Path("data/audit.jsonl")
    log_path.write_text("", encoding="utf-8")
    audit_path.write_text("", encoding="utf-8")
    logging_config.LOG_PATH = log_path
    audit.AUDIT_LOG_PATH = audit_path
    payload = {
        "user_id": "student@vinuni.edu.vn",
        "session_id": "s-test",
        "feature": "qa",
        "message": "What is your refund policy? My card is 4111 1111 1111 1111",
    }

    with TestClient(app) as client:
        response = client.post("/chat", json=payload, headers={"x-request-id": "req-test1234"})

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "req-test1234"
    assert response.json()["correlation_id"] == "req-test1234"

    raw_logs = logging_config.LOG_PATH.read_text(encoding="utf-8")
    assert "student@vinuni.edu.vn" not in raw_logs
    assert "4111" not in raw_logs

    records = [json.loads(line) for line in raw_logs.splitlines() if line.strip()]
    api_records = [record for record in records if record.get("service") == "api"]

    assert len(api_records) == 2
    assert all(record["correlation_id"] == "req-test1234" for record in api_records)
    assert all(record["feature"] == "qa" for record in api_records)
    assert all(record["model"] == "claude-sonnet-4-5" for record in api_records)
    assert all(record["user_id_hash"] != payload["user_id"] for record in api_records)

    raw_audit = audit.AUDIT_LOG_PATH.read_text(encoding="utf-8")
    assert "student@vinuni.edu.vn" not in raw_audit
    assert "4111" not in raw_audit

    audit_records = [json.loads(line) for line in raw_audit.splitlines() if line.strip()]
    assert audit_records[-1]["event"] == "chat_completed"
    assert audit_records[-1]["status"] == "success"
    assert audit_records[-1]["correlation_id"] == "req-test1234"
    assert audit_records[-1]["user_id_hash"] != payload["user_id"]


def test_dashboard_route_renders_required_panels() -> None:
    with TestClient(app) as client:
        response = client.get("/dashboard")

    assert response.status_code == 200
    for heading in ("Latency", "Traffic", "Error Rate", "Cost", "Tokens", "Quality"):
        assert heading in response.text
