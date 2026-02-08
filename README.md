# Aktov Detection Lab

See Aktov detect real AI agent attack patterns in 30 seconds.

## Quick Start

```bash
pip install aktov langchain-core openai-agents
cd labs/
python run_all.py
```

## Individual Demos

| Demo | Framework | Attack Pattern | Detection |
|------|-----------|---------------|-----------|
| `demo_langchain.py` | LangChain | Read file, then POST to external URL | AK-010 |
| `demo_openai_agents.py` | OpenAI Agent SDK | Non-credential agent reads secrets | AK-007 |
| `demo_mcp.py` | MCP | Path traversal, then external exfil | AK-032 + AK-010 |
| `demo_custom.py` | Raw Aktov | Unauthorized credential access | AK-007 |
| `demo_custom_rule.py` | Raw Aktov + Custom Rule | 3+ write operations | CUSTOM-001 |

Run any demo individually:

```bash
python demo_langchain.py
python demo_mcp.py
```

## No API Key Needed

All demos run locally with zero configuration. No API key, no cloud, no external network calls.

## Writing Custom Rules

See `rules/custom_high_write_count.yaml` for an example custom rule. Use the CLI for help:

```bash
aktov rules schema      # field reference
aktov rules examples    # one example per match type
aktov rules validate rules/custom_high_write_count.yaml
```

## Learn More

- **Install:** `pip install aktov`
- **Docs:** https://aktov.io/docs
- **GitHub:** https://github.com/sharmaharjeet92/aktov
