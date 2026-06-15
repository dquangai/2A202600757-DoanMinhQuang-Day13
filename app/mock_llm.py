from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE
from .tracing import observe


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


class FakeLLM:
    def __init__(self, model: str = "claude-sonnet-4-5") -> None:
        self.model = model

    @observe(as_type="generation")
    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)
        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 180)
        if STATE["cost_spike"]:
            output_tokens *= 4
        answer = self._answer_from_prompt(prompt)
        return FakeResponse(text=answer, usage=FakeUsage(input_tokens, output_tokens), model=self.model)

    def _answer_from_prompt(self, prompt: str) -> str:
        lowered = prompt.lower()
        if "refunds are available within 7 days" in lowered:
            return "Refunds are available within 7 days with proof of purchase."
        if "metrics detect incidents" in lowered or "metrics traces and logs" in lowered:
            return (
                "Metrics detect symptoms, traces localize the slow or failing span, "
                "and logs explain the root cause with correlation IDs."
            )
        if "do not expose pii" in lowered or "what should not appear" in lowered:
            return "PII and sensitive data should not appear in app logs; keep only sanitized summaries."
        if "tail latency" in lowered:
            return "Debug tail latency by checking P95/P99 metrics, opening slow traces, then reading correlated logs."
        if "alerts" in lowered:
            return "Alerts should be symptom-based, tied to SLO thresholds, owned by on-call, and linked to runbooks."
        return "Use retrieved context, concise answers, and sanitized observability data for production debugging."
