# Manual-first µMCM workflow

## Purpose

The final MCM-Agent should run bottom-up µMCM abstraction and synthesis with an
LLM provider. During the BOOM research phase, the workflow is already real but
the provider is manual: every semantic task is exported as a self-contained
prompt package, discussed in a ChatGPT conversation, then imported back into the
same deterministic validation path.

The manual and future API modes therefore share the same boundary:

```text
Static WorkUnit
    -> Static Handoff
    -> LLMTask / PromptPackage
    -> provider
       current: manual ChatGPT conversation
       future : API provider
    -> candidate µMCM JSON with Formal Axiom ASTs
    -> deterministic grounding validation
    -> formal-axiom compiler
    -> grounding validation
    -> deterministic structural/control/dataflow support checks
    -> bit-level RTL formal backend
    -> trusted µMCM (formal/spec-proved axioms only)
```

No API call exists in this stage.

## Current formal schema

`umcm-formal-0.3` keeps the v0.2 distinction between instantaneous occurrences
and persistent predicates, but changes the axiom layer fundamentally:

- `occurrences`: grounded boundary occurrences plus strictly grounded internal milestones;
- `predicates`: persistent interface/control facts;
- identity keys and guarded cases;
- `axioms[].formal`: a structured Formal AST and the **only** semantic source of truth;
- environment assumptions, unresolved questions, rationale and extensions.

The LLM no longer supplies a free-form `formula` plus a separate `validation`
object. The workflow deterministically derives the human-readable formula,
semantic references, checker type and proof-obligation arguments from the Formal
AST. Unsupported AST forms fail closed.

## Create the first leaf task

For the real BOOM ProbeUnit:

```bash
python3 -m workflow.cli leaf-task SmallBoomV4Config.fir \
  --root-module BoomProbeUnit \
  --source-root /path/to/chipyard \
  --run-root runs
```

The task directory contains:

```text
task.json
prompt.md
static_handoff.json
expected_output_schema.json
status.json
```

`prompt.md` is self-contained. It can be pasted into the current conversation or
into a fresh ChatGPT conversation without replaying the project history.

If `--source-root` resolves FIRRTL source locators, grounded Scala snippets are
embedded. Otherwise the prompt falls back to the exact FIRRTL statement ledger
and source locators instead of guessing unavailable source text.

## Import a converged manual answer

Save the final conversation response to a file and run:

```bash
python3 -m workflow.cli manual-import \
  runs/<task-id> response.md
```

or pipe it on stdin:

```bash
cat response.md | python3 -m workflow.cli manual-import runs/<task-id> -
```

The deterministic grounding validator checks:

- task / WorkUnit / schema identity;
- unique result IDs;
- boundary occurrences reference physical WorkUnit events;
- derived occurrences have explicit state/signal grounding and evidence;
- predicates and identity carriers reference concrete WorkUnit state/signals;
- every evidence statement ID is inside the WorkUnit;
- cases and Formal AST axioms reference defined semantic IDs/signals;
- legacy axiom `formula` / `validation` fields are rejected;
- axioms are still marked `candidate`.

Then collect structural evidence and invoke the configured formal backend:

```bash
python3 -m workflow.cli semantic-validate runs/<task-id> --formal-backend none
```

The command writes `semantic_validation.json`, `property_obligations.json`, and
`trusted_umcm.json`.

The formal-axiom compiler turns each Formal AST axiom into one of the
currently supported deterministic proof obligations; the LLM does not choose
the checker separately: finite-control history ordering,
transaction-path exclusion, occurrence-vs-predicate exclusion, identity-carrier
stability/dataflow, exact same-cycle one-hot occurrence partition, direct signal
aliasing, and static constant-bit checks.
The finite-control graph over-approximates data-dependent FSM branches and does
not assume ready/valid progress.

These checks now produce evidence levels rather than a generic PASS:

- `GROUNDED`: the candidate references concrete WorkUnit evidence;
- `PARTIALLY_SUPPORTED`: deterministic analysis supports only part of the claim;
- `STRUCTURALLY_SUPPORTED`: the extracted control/dataflow model supports the encoded obligation;
- `FORMALLY_PROVED`: a bit-level RTL formal backend proves the obligation;
- `SPEC_PROVED`: the RTL property is also proved against an external/reference protocol spec;
- `REFUTED`: a counterexample refutes the candidate obligation.

Only `FORMALLY_PROVED` and `SPEC_PROVED` axioms may enter `trusted_umcm.json`.
Structural support is intentionally insufficient. With `--formal-backend explicit-control`, the current real BoomProbeUnit result is
7 `FORMALLY_PROVED` + 1 `SPEC_PROVED`, so all eight declared axioms enter the
trusted/frozen summary. The backend remains fail-closed outside its certified
control, exact-symbolic and selected finite-reference proof domains.

## Why this is not temporary glue

The future API provider will consume the same `LLMTask` and produce the same
candidate envelope. Static handoff, parsing, grounding, refinement history, and
all downstream validators do not need to be rewritten when the provider changes.
