"""Master runner — executes all Aktov detection lab demos.

Usage:
    python run_all.py

Runs each demo script, collects results, and prints a summary table.
"""

from __future__ import annotations

import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(__file__))

from _output import summary_header, summary_line, summary_footer


def main() -> None:
    summary_header()

    demos = [
        {
            "name": "LangChain — Data Exfiltration",
            "module": "demo_langchain",
            "expected": ["AK-010"],
        },
        {
            "name": "OpenAI Agent SDK — Credential Theft",
            "module": "demo_openai_agents",
            "expected": ["AK-007"],
        },
        {
            "name": "MCP — Path Traversal + Exfiltration",
            "module": "demo_mcp",
            "expected": ["AK-032", "AK-010"],
        },
        {
            "name": "Custom Client — Unauthorized Credentials",
            "module": "demo_custom",
            "expected": ["AK-007"],
        },
        {
            "name": "Custom Rule — High Write Count",
            "module": "demo_custom_rule",
            "expected": ["CUSTOM-001"],
        },
    ]

    passed = 0
    total_rules = 0

    for i, demo in enumerate(demos, 1):
        try:
            mod = __import__(demo["module"])
            result = mod.run()
            actual_ids = result.get("rule_ids", [])
            rules_count = getattr(result.get("response"), "rules_evaluated", 0)
            total_rules += rules_count

            if summary_line(i, len(demos), demo["name"], demo["expected"], actual_ids):
                passed += 1
        except Exception:
            print(f"  [{i}/{len(demos)}] {demo['name']} ... ERROR")
            traceback.print_exc()

    summary_footer(passed, len(demos), total_rules)

    sys.exit(0 if passed == len(demos) else 1)


if __name__ == "__main__":
    main()
