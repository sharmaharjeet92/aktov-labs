"""Shared pretty-print helpers for Aktov demo lab scripts.

Provides colored terminal output with NO_COLOR env var support.
"""

from __future__ import annotations

import os
import sys

# Respect NO_COLOR convention (https://no-color.org/)
_NO_COLOR = os.environ.get("NO_COLOR") is not None or not sys.stdout.isatty()

# ANSI color codes
_BOLD = "" if _NO_COLOR else "\033[1m"
_DIM = "" if _NO_COLOR else "\033[2m"
_RED = "" if _NO_COLOR else "\033[31m"
_GREEN = "" if _NO_COLOR else "\033[32m"
_YELLOW = "" if _NO_COLOR else "\033[33m"
_CYAN = "" if _NO_COLOR else "\033[36m"
_MAGENTA = "" if _NO_COLOR else "\033[35m"
_RESET = "" if _NO_COLOR else "\033[0m"


def banner(title: str, description: str = "") -> None:
    """Print a colored section header."""
    width = 56
    print()
    print(f"{_CYAN}{_BOLD}{'=' * width}{_RESET}")
    print(f"{_CYAN}{_BOLD}  {title}{_RESET}")
    if description:
        print(f"{_DIM}  {description}{_RESET}")
    print(f"{_CYAN}{_BOLD}{'=' * width}{_RESET}")
    print()


def scenario(text: str) -> None:
    """Print the attack scenario description."""
    print(f"  {_YELLOW}Scenario:{_RESET} {text}")
    print()


def step(tool_name: str, args: str) -> None:
    """Print a tool call step."""
    print(f"  {_DIM}->{_RESET} {_BOLD}{tool_name}{_RESET}({_DIM}{args}{_RESET})")


def results(response: object) -> None:
    """Print detection results from a TraceResponse."""
    status = getattr(response, "status", "unknown")
    rules_evaluated = getattr(response, "rules_evaluated", 0)
    alerts = getattr(response, "alerts", [])

    print()
    print(f"  {_BOLD}Detection Results{_RESET}")
    print(f"  {_DIM}{'─' * 40}{_RESET}")
    print(f"  Status:          {status}")
    print(f"  Rules evaluated: {rules_evaluated}")
    print(f"  Alerts fired:    {len(alerts)}")

    if alerts:
        print()
        for alert in alerts:
            rule_id = alert.get("rule_id", "?")
            severity = alert.get("severity", "?").upper()
            rule_name = alert.get("rule_name", "?")

            color = _RED if severity == "CRITICAL" else _YELLOW if severity == "HIGH" else _RESET
            print(f"  {color}{_BOLD}[{rule_id}] {severity}: {rule_name}{_RESET}")
    print()


def explainer(text: str) -> None:
    """Print a 'what just happened' explanation."""
    print(f"  {_MAGENTA}What happened:{_RESET} {text}")
    print()


def success(msg: str) -> None:
    """Print a success message."""
    print(f"  {_GREEN}{_BOLD}PASS{_RESET} {msg}")


def fail(msg: str) -> None:
    """Print a failure message."""
    print(f"  {_RED}{_BOLD}FAIL{_RESET} {msg}")


def summary_header() -> None:
    """Print the run_all summary header."""
    print()
    print(f"{_CYAN}{_BOLD}{'=' * 56}{_RESET}")
    print(f"{_CYAN}{_BOLD}         Aktov Detection Lab{_RESET}")
    print(f"{_DIM}  See AI agent security detections in action{_RESET}")
    print(f"{_CYAN}{_BOLD}{'=' * 56}{_RESET}")
    print()


def summary_line(
    index: int,
    total: int,
    name: str,
    expected_ids: list[str],
    actual_ids: list[str],
) -> bool:
    """Print one line of the summary table. Returns True if passed."""
    matched = all(eid in actual_ids for eid in expected_ids)
    ids_str = ", ".join(actual_ids) if actual_ids else "none"

    dots = "." * (48 - len(f"[{index}/{total}] {name}"))
    if matched:
        print(f"  [{index}/{total}] {name} {dots} {_GREEN}{ids_str} DETECTED{_RESET}")
    else:
        print(f"  [{index}/{total}] {name} {dots} {_RED}MISSED (got: {ids_str}){_RESET}")
    return matched


def summary_footer(passed: int, total: int, total_rules: int) -> None:
    """Print the final summary stats."""
    missed = total - passed
    print()
    print(f"  {_DIM}{'─' * 50}{_RESET}")
    color = _GREEN if missed == 0 else _RED
    print(f"  {color}{_BOLD}{passed}/{total} scenarios detected    {missed} missed    {total_rules} rules evaluated{_RESET}")
    print()
    print(f"  {_DIM}Install: pip install aktov{_RESET}")
    print(f"  {_DIM}Docs:    https://aktov.io/docs{_RESET}")
    print(f"  {_DIM}GitHub:  https://github.com/sharmaharjeet92/aktov{_RESET}")
    print()
