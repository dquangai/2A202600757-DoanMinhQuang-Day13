from __future__ import annotations


def render_dashboard() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Observability Dashboard</title>
  <style>
    :root {
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #19202a;
      --muted: #687386;
      --border: #dce1e8;
      --accent: #256f6c;
      --warn: #b15d20;
      --danger: #b3261e;
      --ok: #2f7d32;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    main {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      padding: 24px 0 32px;
    }

    header {
      display: flex;
      align-items: flex-end;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 18px;
    }

    h1 {
      margin: 0;
      font-size: 24px;
      font-weight: 700;
      line-height: 1.2;
    }

    .meta {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: flex-end;
      color: var(--muted);
      font-size: 13px;
    }

    .chip {
      border: 1px solid var(--border);
      border-radius: 999px;
      background: #fff;
      padding: 5px 10px;
      white-space: nowrap;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }

    .panel {
      min-height: 170px;
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--panel);
      padding: 16px;
      display: grid;
      grid-template-rows: auto 1fr auto;
      gap: 14px;
    }

    .panel h2 {
      margin: 0;
      font-size: 14px;
      font-weight: 700;
      color: #2b3440;
    }

    .metric {
      display: flex;
      align-items: baseline;
      gap: 8px;
      min-width: 0;
    }

    .value {
      font-size: 34px;
      font-weight: 750;
      line-height: 1;
      overflow-wrap: anywhere;
    }

    .unit {
      color: var(--muted);
      font-size: 13px;
      white-space: nowrap;
    }

    .rows {
      display: grid;
      gap: 7px;
      font-size: 13px;
      color: var(--muted);
    }

    .row {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      border-top: 1px solid #edf0f4;
      padding-top: 7px;
    }

    .row strong { color: var(--text); }
    .ok { color: var(--ok); }
    .warn { color: var(--warn); }
    .danger { color: var(--danger); }
    .accent { color: var(--accent); }

    @media (max-width: 860px) {
      header { align-items: flex-start; flex-direction: column; }
      .meta { justify-content: flex-start; }
      .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (max-width: 560px) {
      main { width: min(100% - 20px, 1180px); padding-top: 16px; }
      .grid { grid-template-columns: 1fr; }
      .panel { min-height: 150px; }
      .value { font-size: 30px; }
    }
  </style>
</head>
<body>
  <main>
    <header>
      <h1>Observability Dashboard</h1>
      <div class="meta">
        <span class="chip">service: day13-observability-lab</span>
        <span class="chip" id="updated">updated: pending</span>
      </div>
    </header>

    <section class="grid" aria-label="Layer 2 metrics">
      <article class="panel">
        <h2>Latency</h2>
        <div class="metric"><span class="value accent" id="latencyP95">0</span><span class="unit">ms P95</span></div>
        <div class="rows">
          <div class="row"><span>P50</span><strong id="latencyP50">0 ms</strong></div>
          <div class="row"><span>P99</span><strong id="latencyP99">0 ms</strong></div>
          <div class="row"><span>SLO</span><strong>&lt; 3000 ms</strong></div>
        </div>
      </article>

      <article class="panel">
        <h2>Traffic</h2>
        <div class="metric"><span class="value" id="traffic">0</span><span class="unit">requests</span></div>
        <div class="rows">
          <div class="row"><span>successful</span><strong id="successCount">0</strong></div>
          <div class="row"><span>failed</span><strong id="failedCount">0</strong></div>
          <div class="row"><span>window</span><strong>runtime</strong></div>
        </div>
      </article>

      <article class="panel">
        <h2>Error Rate</h2>
        <div class="metric"><span class="value ok" id="errorRate">0</span><span class="unit">%</span></div>
        <div class="rows">
          <div class="row"><span>SLO</span><strong>&lt; 2%</strong></div>
          <div class="row"><span>breakdown</span><strong id="errorBreakdown">none</strong></div>
        </div>
      </article>

      <article class="panel">
        <h2>Cost</h2>
        <div class="metric"><span class="value" id="totalCost">0.0000</span><span class="unit">USD</span></div>
        <div class="rows">
          <div class="row"><span>average</span><strong id="avgCost">$0.0000</strong></div>
          <div class="row"><span>daily budget</span><strong>&lt; $2.50</strong></div>
        </div>
      </article>

      <article class="panel">
        <h2>Tokens</h2>
        <div class="metric"><span class="value" id="tokensTotal">0</span><span class="unit">tokens</span></div>
        <div class="rows">
          <div class="row"><span>input</span><strong id="tokensIn">0</strong></div>
          <div class="row"><span>output</span><strong id="tokensOut">0</strong></div>
        </div>
      </article>

      <article class="panel">
        <h2>Quality</h2>
        <div class="metric"><span class="value ok" id="qualityAvg">0.00</span><span class="unit">avg score</span></div>
        <div class="rows">
          <div class="row"><span>SLO</span><strong>&gt;= 0.75</strong></div>
          <div class="row"><span>proxy</span><strong>heuristic</strong></div>
        </div>
      </article>
    </section>
  </main>

  <script>
    const fmtInt = new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 });
    const fmtMoney = new Intl.NumberFormat("en-US", { minimumFractionDigits: 4, maximumFractionDigits: 4 });

    function setText(id, value) {
      document.getElementById(id).textContent = value;
    }

    function statusClass(value, warnAt, dangerAt) {
      if (value >= dangerAt) return "danger";
      if (value >= warnAt) return "warn";
      return "ok";
    }

    async function refresh() {
      const res = await fetch("/metrics", { cache: "no-store" });
      const data = await res.json();
      const totalTokens = (data.tokens_in_total || 0) + (data.tokens_out_total || 0);
      const errorBreakdown = data.error_breakdown && Object.keys(data.error_breakdown).length
        ? Object.entries(data.error_breakdown).map(([k, v]) => `${k}: ${v}`).join(", ")
        : "none";

      setText("latencyP95", fmtInt.format(data.latency_p95 || 0));
      setText("latencyP50", `${fmtInt.format(data.latency_p50 || 0)} ms`);
      setText("latencyP99", `${fmtInt.format(data.latency_p99 || 0)} ms`);
      setText("traffic", fmtInt.format((data.traffic || 0) + (data.total_errors || 0)));
      setText("successCount", fmtInt.format(data.traffic || 0));
      setText("failedCount", fmtInt.format(data.total_errors || 0));
      setText("errorRate", (data.error_rate_pct || 0).toFixed(2));
      setText("errorBreakdown", errorBreakdown);
      setText("totalCost", fmtMoney.format(data.total_cost_usd || 0));
      setText("avgCost", `$${fmtMoney.format(data.avg_cost_usd || 0)}`);
      setText("tokensTotal", fmtInt.format(totalTokens));
      setText("tokensIn", fmtInt.format(data.tokens_in_total || 0));
      setText("tokensOut", fmtInt.format(data.tokens_out_total || 0));
      setText("qualityAvg", (data.quality_avg || 0).toFixed(2));
      setText("updated", `updated: ${new Date().toLocaleTimeString()}`);

      document.getElementById("errorRate").className = `value ${statusClass(data.error_rate_pct || 0, 2, 5)}`;
      document.getElementById("qualityAvg").className = `value ${(data.quality_avg || 0) >= 0.75 ? "ok" : "warn"}`;
      document.getElementById("latencyP95").className = `value ${statusClass(data.latency_p95 || 0, 3000, 5000)}`;
    }

    refresh();
    setInterval(refresh, 20000);
  </script>
</body>
</html>"""
