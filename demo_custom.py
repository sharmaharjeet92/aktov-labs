"""Demo: Raw Aktov Client — Credential Access Detection (AK-007).

Scenario: A data-processing agent directly accesses credential tools
without using any framework integration. Shows how Aktov works with
just the raw client API (2 lines of setup).

Expected detection: AK-007 (credential_tool_from_non_credential_agent)
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from _output import banner, scenario, step, results, explainer

from aktov import Aktov


def run() -> dict:
    """Run the demo and return {rule_ids, response}."""

    banner(
        "Raw Aktov Client — Credential Access Detection",
        "No framework needed — just 2 lines of setup",
    )

    scenario(
        "A data-processing agent accesses get_secret() and fetch_token() "
        "directly. It's not authorized as a credential manager."
    )

    # ── Set up Aktov (2 lines!) ──
    ak = Aktov(agent_id="data-processor", agent_type="custom")
    trace = ak.start_trace()

    # ── Tool call 1: get_secret ──
    step("get_secret", 'name="production_api_key"')
    trace.record_action(
        tool_name="get_secret",
        arguments={"name": "production_api_key"},
        outcome={"status": "success"},
    )

    # ── Tool call 2: fetch_token ──
    step("fetch_token", 'user="admin"')
    trace.record_action(
        tool_name="fetch_token",
        arguments={"user": "admin"},
        outcome={"status": "success"},
    )

    # ── End trace and show results ──
    response = trace.end()
    results(response)

    explainer(
        "AK-007 fires because agent_type is 'custom' (not in the credential "
        "manager allowlist) but it accessed credential-category tools. "
        "Works the same way regardless of framework."
    )

    rule_ids = [a["rule_id"] for a in response.alerts]
    return {"rule_ids": rule_ids, "response": response}


if __name__ == "__main__":
    result = run()
    rule_ids = result["rule_ids"]
    if "AK-007" in rule_ids:
        print("  Demo passed: AK-007 detected.")
    else:
        print(f"  Demo FAILED: expected AK-007, got {rule_ids}", file=sys.stderr)
        sys.exit(1)
