# Worked cases

Generalised engineering-management examples supplied by Darren. Suggested actions are not reported outcomes.

## Case A: Sequence development and deployment

### Reported situation

Operators of a complex machine identified slow deployment as a problem and requested a local-only edit mode. The organisation is moving towards a traceable operating state; locally controlled branches may be difficult to track organisationally. The pipeline performs checks intended to protect production.

The engineer agreed to investigate slowness AND proposed dry-running sequences before production. Their hypothesis is that missing development feedback forces operators to discover errors on the live machine. A distinction between development and production branches was also suggested. Neither dry-run effectiveness nor the necessity of all current pipeline delays has been established.

One participant appeared unreceptive; others were silent. Their reasons and degree of agreement are unknown.

### Appropriate next actions

- Preserve the agreement to investigate latency. Measure where time is spent and what each check protects before proposing changes.
- Observe a representative sequence edit with an operator. Identify the feedback needed, workarounds and failures that depend on live machine behaviour.
- Prototype a limited dry run using that example. Compare time to useful feedback, errors detected, missed errors and additional effort. Record what still requires the machine.
- Explore development/production separation as an implementation option. Branch names alone do not establish production control; the exact deployed version and promotion permissions matter.

### Revision triggers

If most relevant failures require live state that the dry run cannot meaningfully represent, narrow or reconsider the prototype. If avoidable pipeline waiting dominates, prioritise latency improvements while preserving required checks. Both findings can be true.

## Case B: Alarm-panel design

### Reported situation

An engineer is asking a graphic designer to mock up an alarm panel so that another competence can contribute without first passing through engineers' assumptions about the software design. No design outcome or operator evaluation has yet been reported.

### Appropriate next actions

- Give the designer the operator tasks and known operational requirements, while allowing exploration beyond the existing implementation.
- Evaluate the mock-up with operators using representative alarm situations.
- Reconcile promising ideas with operational and engineering constraints; bring in additional relevant expertise if questions exceed the group's competence.
- Treat the mock-up as evidence for discussion, not proof of usability or production readiness.

