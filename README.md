
# EffLint

**A local-first efficiency linter for LLM and agent workloads.**

EffLint analyzes GenAI execution traces and identifies patterns that may contribute to unnecessary token consumption, cost, latency, or agent work.

It is designed to answer:

> Where might my AI application be doing unnecessary work, and what evidence supports that conclusion?

## Why EffLint?

Most LLM observability tools tell you:

```text
Tokens: 18,420
Cost: $0.14
Latency: 4.2s
```

EffLint aims to tell you:

```text
EFF003

5 tools were registered.
Only 3 were used.

2 unused tool schemas contributed
920 tokens of available context.

Confidence: DETERMINISTIC
```

or:

```text
EFF004

search_customer was invoked
4 times with identical arguments.

Confidence: DETERMINISTIC
```

## Philosophy

EffLint follows one important principle:

> Observation is not the same as waste.

A large context window is not automatically wasteful.

A large model is not automatically oversized.

Repeated context is not automatically unnecessary.

EffLint therefore assigns confidence levels to findings:

| Confidence | Meaning |
|---|---|
| EXACT | Directly reported or mathematically derived |
| DETERMINISTIC | Directly observable execution pattern |
| HEURISTIC | Potential inefficiency requiring investigation |
| REPLAY_REQUIRED | Requires evaluation or counterfactual replay |

## v0.1 Rules

| Rule | Description |
|---|---|
| EFF001 | Rapid context growth |
| EFF002 | Repeated context |
| EFF003 | Unused tools |
| EFF004 | Repeated tool invocation |
| EFF005 | Low cache reuse |

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/efflint.git

cd efflint
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

macOS/Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Install:

```bash
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Run the sample

```bash
efflint analyze examples/sample_trace.jsonl
```

You should see findings for:

```text
EFF001
EFF002
EFF003
EFF004
EFF005
```

## Export JSON

```bash
efflint analyze \
    examples/sample_trace.jsonl \
    --output-json report.json
```

## Run tests

```bash
pytest -v
```

## Architecture

```text
Provider / Framework
        │
        ▼
Telemetry Adapter
        │
        ▼
Canonical LLMCall
        │
        ▼
┌────────────────────┐
│ Efficiency Rules   │
├────────────────────┤
│ Context            │
│ Cache              │
│ Tools              │
│ Agent loops        │
└─────────┬──────────┘
          │
          ▼
       Findings
          │
          ▼
┌────────────────────┐
│ CLI                │
│ JSON               │
│ Future: SARIF      │
└────────────────────┘
```

## Canonical trace format

EffLint intentionally separates telemetry ingestion from analysis.

Provider-specific telemetry:

```text
OpenAI
Anthropic
Gemini
OpenTelemetry
OpenInference
LiteLLM
Langfuse
```

can eventually be normalized into:

```python
LLMCall
```

Rules operate only on the canonical representation.

This keeps the analysis engine provider-neutral.

## Example JSONL record

```json
{
  "trace_id": "agent-run-001",
  "span_id": "span-001",
  "provider": "openai",
  "model": "example-model",
  "usage": {
    "input_tokens": 1000,
    "output_tokens": 180,
    "cache_read_tokens": 0,
    "cache_write_tokens": 600
  }
}
```

## Roadmap

### v0.1

- canonical schema
- JSONL ingestion
- context-growth detection
- repeated-context detection
- unused-tool detection
- tool-loop detection
- cache-efficiency detection
- Rich CLI
- JSON report

### v0.2

- OpenTelemetry adapter
- OpenInference adapter
- baseline comparison
- Markdown reporter
- SARIF reporter
- GitHub Actions integration

### v0.3

- provider-aware pricing
- cache economics
- prompt composition
- token attribution

### v0.4

- MCP tool analysis
- tool ROI
- privacy-preserving context fingerprints

### v0.5

- RAG context ablation
- model right-sizing replay
- quality-aware optimization

## Contributing

EffLint is intentionally rule-driven.

A new efficiency check can be implemented by extending:

```python
Rule
```

Example:

```python
class MyRule(Rule):

    rule_id = "EFF101"
    title = "My efficiency rule"

    def analyze(self, calls):
        ...
```

Potential contribution areas:

- Gemini adapter
- Anthropic adapter
- OpenTelemetry adapter
- OpenInference adapter
- Langfuse importer
- LiteLLM importer
- SARIF reporter
- MCP analysis
- new efficiency rules
- synthetic trace generators

## Privacy

EffLint is designed to support local analysis.

The canonical schema supports fingerprints so repeated context can be detected without storing raw prompts.

Future versions will provide configurable HMAC-based fingerprints and redaction hooks.

## Non-goals

EffLint is not intended to become:

- an LLM gateway
- another observability dashboard
- a hosted tracing platform
- a prompt-management system
- a model router

The focus is:

> Explainable analysis of GenAI execution efficiency.

## License

MIT