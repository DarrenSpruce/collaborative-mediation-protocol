# ProMediate integration preparation

Target: [Microsoft ProMediate-Eval](https://github.com/microsoft/ProMediate-Eval), inspected at commit `6b4b857d1304a9f18ef100511d53f9694762f597` on 9 October 2026. This is an **experimental adapter with offline tests**, not an end-to-end tested runner or reproduction of published results. No upstream source or negotiation case materials are redistributed here.

`bridge.py` constructs basic/protocol messages and validates a shared JSON speak/silence contract. `mediator.py` implements ProMediate's Mediator interface using `prepare`, `act` and `next_utterance`. It keeps the upstream recent-history/memory interface and injects an asynchronous completion callable, avoiding the upstream provider wrapper. The callable accepts `(messages, model=...)`, returns raw JSON text, and must enforce and log model settings, usage, timeouts and budgets. Credentials must stay outside the repository.

The plugin supports combined mode only. Registration in a repaired upstream runner should use a factory that binds `completion` and `condition`; do not merely add the class to `classes`, since a transport is required. Ensure its import path includes this repository. Its inherited memory initialisation and conversation/participant operations still use upstream code and provider calls: injecting a mediator transport alone does not fix the full simulation.

Offline check from repository root:

```sh
python -m unittest integrations.promediate.test_bridge -v
```

Tests check reviewer/future-turn separation, actual prior-response threading, strict decision parsing and plugin state clearing with a stub upstream base. They do **not** establish upstream installation compatibility or model quality.

Before a live comparison, resolve the [readiness report](../../evaluations/results/2026-10-09-readiness.md) for all conditions. Apply infrastructure changes uniformly and record the patch and exact commits. Preserve the reference mediator prompts, identify any implementation changes, and avoid calling a changed system an exact replication.

For the first prompt comparison use the [workplace replay plan](../../evaluations/workplace/README.md). For simulation, create participant role cards and staged-information delivery explicitly: do not put all later disclosures in the public opening context. The public two-turn fixtures are not silently converted into negotiation option grids, because that would change what they test.
