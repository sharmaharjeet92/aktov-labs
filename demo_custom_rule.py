"""Demo: Custom Rule — High Write Count Detection (CUSTOM-001).

Scenario: An ETL agent performs multiple write operations in a single
trace. A custom YAML rule (not bundled) detects this pattern using
the 'count' match type.

Expected detection: CUSTOM-001 (high_write_count)
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
        "Custom Rule — High Write Count Detection",
        "Write your own YAML rules and load them at runtime",
    )

    scenario(
        "An ETL agent writes to 3 different locations in one trace. "
        "A custom rule fires when write count >= 3."
    )

    # ── Set up Aktov with custom rules directory ──
    rules_dir = os.path.join(os.path.dirname(__file__), "rules")
    ak = Aktov(agent_id="etl-pipeline", agent_type="custom", rules_dir=rules_dir)
    trace = ak.start_trace()

    # ── Tool call 1: write file ──
    step("write_file", 'path="/tmp/export_a.csv"')
    trace.record_action(
        tool_name="write_file",
        arguments={"path": "/tmp/export_a.csv", "content": "data..."},
        outcome={"status": "success"},
    )

    # ── Tool call 2: write file ──
    step("write_file", 'path="/tmp/export_b.csv"')
    trace.record_action(
        tool_name="write_file",
        arguments={"path": "/tmp/export_b.csv", "content": "data..."},
        outcome={"status": "success"},
    )

    # ── Tool call 3: insert database record ──
    step("insert_record", 'table="audit_log"')
    trace.record_action(
        tool_name="insert_record",
        arguments={"table": "audit_log", "data": '{"action": "export"}'},
        outcome={"status": "success"},
    )

    # ── End trace and show results ──
    response = trace.end()
    results(response)

    explainer(
        "CUSTOM-001 fires because the trace has 3 actions with tool_category='write' "
        "(write_file x2 + insert_record). The rule uses the 'count' match type with "
        "min_count: 3. See rules/custom_high_write_count.yaml for the rule definition."
    )

    rule_ids = [a["rule_id"] for a in response.alerts]
    return {"rule_ids": rule_ids, "response": response}


if __name__ == "__main__":
    result = run()
    rule_ids = result["rule_ids"]
    if "CUSTOM-001" in rule_ids:
        print("  Demo passed: CUSTOM-001 detected.")
    else:
        print(f"  Demo FAILED: expected CUSTOM-001, got {rule_ids}", file=sys.stderr)
        sys.exit(1)
