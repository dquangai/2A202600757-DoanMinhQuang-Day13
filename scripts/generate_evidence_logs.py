from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import logging_config
from app.metrics import reset


def main() -> None:
    log_path = Path(os.getenv("LOG_PATH", "data/logs.jsonl"))
    logging_config.LOG_PATH = log_path
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("", encoding="utf-8")
    reset()

    from app.main import app

    payloads = [
        json.loads(line)
        for line in Path("data/sample_queries.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    with TestClient(app) as client:
        for idx, payload in enumerate(payloads, start=1):
            response = client.post("/chat", json=payload, headers={"x-request-id": f"req-{idx:08x}"})
            response.raise_for_status()
            body = response.json()
            print(f"{response.status_code} {body['correlation_id']} {body['latency_ms']}ms")

    print(f"Wrote {len(payloads)} requests to {log_path}")


if __name__ == "__main__":
    main()
