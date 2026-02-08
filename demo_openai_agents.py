"""Demo: OpenAI Agent SDK Credential Theft Detection (AK-007).

Scenario: A general-purpose assistant agent accesses credential tools
(get_secret, fetch_token) even though it's not a credential manager.
Aktov detects the unauthorized credential access.

Expected detection: AK-007 (credential_tool_from_non_credential_agent)
"""

from __future__ import annotations

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from _output import banner, scenario, step, results, explainer

from agents import RunContextWrapper
from aktov.integrations.openai_agents import AktovHooks


class _MockContext:
    pass


class _MockAgent:
    name = "general-assistant"


class _MockTool:
    """Minimal mock that matches what AktovRunHooks reads from a tool."""

    def __init__(self, name: str, arguments: dict | None = None) -> None:
        self.name = name
        self.arguments = arguments


async def _run() -> dict:
    banner(
        "OpenAI Agent SDK — Credential Theft Detection",
        "Detects non-credential agent accessing secrets",
    )

    scenario(
        "A general-purpose assistant agent calls get_secret() and "
        "read_database() — it should never touch credentials."
    )

    # ── Set up Aktov hooks ──
    hooks = AktovHooks(aktov_agent_name="general-assistant")
    ctx = RunContextWrapper(context=_MockContext())
    agent = _MockAgent()

    # ── Tool call 1: get_secret (credential tool) ──
    tool1 = _MockTool("get_secret", {"name": "db_password"})
    step("get_secret", 'name="db_password"')
    await hooks.on_tool_start(ctx, agent, tool1)
    await hooks.on_tool_end(ctx, agent, tool1, "secret-value-for-db_password")

    # ── Tool call 2: read_database ──
    tool2 = _MockTool("read_database", {"query": "SELECT * FROM users"})
    step("read_database", 'query="SELECT * FROM users"')
    await hooks.on_tool_start(ctx, agent, tool2)
    await hooks.on_tool_end(ctx, agent, tool2, "Results for: SELECT * FROM users")

    # ── End trace and show results ──
    response = hooks.end()
    results(response)

    explainer(
        "AK-007 fires because agent_type is 'openai-agents' (not a credential "
        "manager) but it accessed a 'credential' category tool (get_secret). "
        "This catches scope exploitation and stolen agent identities."
    )

    rule_ids = [a["rule_id"] for a in response.alerts]
    return {"rule_ids": rule_ids, "response": response}


def run() -> dict:
    """Synchronous entry point."""
    return asyncio.run(_run())


if __name__ == "__main__":
    result = run()
    rule_ids = result["rule_ids"]
    if "AK-007" in rule_ids:
        print("  Demo passed: AK-007 detected.")
    else:
        print(f"  Demo FAILED: expected AK-007, got {rule_ids}", file=sys.stderr)
        sys.exit(1)
