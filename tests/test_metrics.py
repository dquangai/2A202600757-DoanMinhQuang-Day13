from app.metrics import percentile, record_error, record_request, reset, snapshot


def test_percentile_basic() -> None:
    assert percentile([100, 200, 300, 400], 50) >= 100


def test_snapshot_includes_error_rate() -> None:
    reset()
    record_request(latency_ms=100, cost_usd=0.01, tokens_in=10, tokens_out=20, quality_score=0.8)
    record_request(latency_ms=200, cost_usd=0.02, tokens_in=15, tokens_out=25, quality_score=0.9)
    record_error("RuntimeError")

    data = snapshot()

    assert data["traffic"] == 2
    assert data["total_errors"] == 1
    assert data["error_rate_pct"] == 33.33
    assert data["error_breakdown"] == {"RuntimeError": 1}
