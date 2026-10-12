# Benchmark preparation and readiness — 9 October 2026

**No live model benchmark was run. No comparative effectiveness scores are reported.**

Prepared against protocol repository commit `ed1d1e1` (v1.1) and official [ProMediate-Eval](https://github.com/microsoft/ProMediate-Eval/tree/6b4b857d1304a9f18ef100511d53f9694762f597). The next deliverable is evidence, rather than more mediation rules: six public synthetic sequential cases, a comparison plan, and an experimental mediator bridge with offline checks.

## Findings from source inspection

| Location in pinned upstream | Finding | Consequence before benchmarking |
| --- | --- | --- |
| `thoughtful_agents/utils/llm_api.py` | `get_client` passes `api_version` to `OpenAI`; async completion selects a fixed Claude model and 1024-token limit, rather than using the requested model/limit. Sync OpenAI calls omit the supplied temperature and token cap. | Configure the correct client for the selected provider; make settings explicit and log actual models and usage. Do not claim a matched-budget comparison with this wrapper unchanged. |
| `multiparty_conversation_negotiate.py` | Participants use a fixed Claude model; mediator model aliases are separately mapped. | Log all roles, not just the CLI model argument. Fixed participant models can be valid if deliberate and shared across conditions. |
| `thoughtful_agents/models/generic_mediator.py` | Constructor does not forward response mode to the base; some decision calls select a fixed model. | Verify the intended comparison path and model routing; an outer model argument alone is insufficient. |
| Supplied `cases/*.json` and runner | Five of six supplied JSON files lack `topics`. `hmo.json` supplies a list; runner also indexes `issues[case]` using a string case name when calculating turn count. | Resolve schema and turn-count consistency before claiming any supplied case runs. |
| `experiment_example.sh` | Summary evaluation calls `evaluation.py` at root, whereas inspected file is `scripts/evaluation.py`. | Verify command paths and evaluation outputs. |

These are static observations of this commit, not a comprehensive upstream bug report. The project has not been contacted and no issue has been filed.

## Local execution status

No `OPENAI_API_KEY`, `CLAUDE_API_KEY` or `ANTHROPIC_API_KEY` was configured in this environment. No credentials were printed or requested in chat; no paid model calls were attempted. The adapter avoids the upstream mediator wrapper but does not repair the whole simulator. Full dependency installation, provider connectivity, simulation and reference-mediator execution remain unverified.

Four offline unit tests pass: input separation, decision parsing, required history/condition validation, and adapter wiring with a stub. The initial test command was invoked outside the repository and failed to import the package; rerunning from the documented repository root resolved this. Passing these tests is an engineering check, not evidence that the protocol improves mediation.

## Decision

Continue preparing to use the official framework; do not yet rely on its unmodified defaults for fair comparative claims. Run the inexpensive two-turn basic/protocol comparison first once an authorised model runtime and call budget are available. Then repair and pin the upstream runtime consistently for the Generic/Social/protocol simulation comparison. Independently contributed cases and human scoring remain essential.

Contributing a small reproducible interoperability fix or case pack upstream may be useful later. No merger or external outreach is justified by results yet, because results have not been collected.
