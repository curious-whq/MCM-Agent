# Run Summary — LSU::state-0-9

## Identity

- task: `leaf_abstraction-LSU-state-0-9-943f5c2db0171922`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.14`
- schema: `umcm-formal-0.5`
- workflow status: `VALIDATION_INCOMPLETE`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 0
- predicates: 0
- identity keys: 0
- cases: 0
- candidate axioms: 0
- unresolved: 1

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 0
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 0
- formal backend: `explicit-control`

## Unresolved

- `U1` Grounding gap: the complete priority-guarded next-state relation for ldq_tail cannot be instantiated because the handoff exposes writer 7874 (ldq_tail := io.core.brupdate.b2.uop.ldq_idx) and writer 8104 (ldq_tail := 0) …

## Next action

Review unresolved/partial structural obligations and then run a real formal backend.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
