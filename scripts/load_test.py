import argparse
import concurrent.futures
import json
import os
import time
from pathlib import Path

import httpx

DEFAULT_BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
QUERIES = Path("data/sample_queries.jsonl")


def send_request(client: httpx.Client, base_url: str, payload: dict) -> None:
    try:
        start = time.perf_counter()
        r = client.post(f"{base_url}/chat", json=payload)
        latency = (time.perf_counter() - start) * 1000
        try:
            body = r.json()
            correlation_id = body.get("correlation_id") or body.get("detail")
        except ValueError:
            correlation_id = r.text[:120].replace("\n", " ")
        print(f"[{r.status_code}] {correlation_id} | {payload['feature']} | {latency:.1f}ms")
    except Exception as e:
        print(f"Error: {e}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=1, help="Number of concurrent requests")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="FastAPI base URL")
    args = parser.parse_args()
    base_url = args.base_url.rstrip("/")

    lines = [line for line in QUERIES.read_text(encoding="utf-8").splitlines() if line.strip()]
    
    with httpx.Client(timeout=30.0) as client:
        if args.concurrency > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
                futures = [executor.submit(send_request, client, base_url, json.loads(line)) for line in lines]
                concurrent.futures.wait(futures)
        else:
            for line in lines:
                send_request(client, base_url, json.loads(line))


if __name__ == "__main__":
    main()
