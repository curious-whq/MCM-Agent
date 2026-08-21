from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from typing import Any

from .composition import build_prompt_interface
from .schema import UMCM_SCHEMA_VERSION, candidate_output_schema


WORKFLOW_VERSION = "manual-first-workflow-0.9"
PROMPT_VERSION = "leaf-abstraction-prompt-0.11"
PARENT_PROMPT_VERSION = "parent-synthesis-prompt-0.3"


class TaskKind(str, Enum):
    LEAF_ABSTRACTION = "leaf_abstraction"
    REFINEMENT = "refinement"
    PARENT_SYNTHESIS = "parent_synthesis"
    BUG_ANALYSIS = "bug_analysis"


@dataclass(frozen=True)
class LLMTask:
    task_id: str
    kind: TaskKind
    work_unit_id: str
    schema_version: str
    prompt_version: str
    workflow_version: str
    provider_mode: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "kind": self.kind.value,
            "work_unit_id": self.work_unit_id,
            "schema_version": self.schema_version,
            "prompt_version": self.prompt_version,
            "workflow_version": self.workflow_version,
            "provider_mode": self.provider_mode,
        }


@dataclass(frozen=True)
class PromptPackage:
    task: LLMTask
    static_handoff: dict[str, Any]
    expected_output_schema: dict[str, Any]
    prompt: str


def _stable_task_id(
    kind: TaskKind,
    handoff: dict[str, Any],
    *,
    prompt_version: str = PROMPT_VERSION,
) -> str:
    payload = json.dumps(
        {
            "kind": kind.value,
            "schema": UMCM_SCHEMA_VERSION,
            "prompt": prompt_version,
            "handoff": handoff,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:16]
    safe = handoff["work_unit"]["id"].replace("::", "-").replace("/", "-")
    return f"{kind.value}-{safe}-{digest}"


def _render_source_evidence(handoff: dict[str, Any]) -> str:
    evidence = handoff["source_evidence"]
    if evidence["resolved"]:
        chunks = []
        for snippet in evidence["resolved"]:
            chunks.append(
                "\n".join(
                    [
                        f"### {snippet['logical_file']}:{snippet['start_line']}-{snippet['end_line']}",
                        "```scala",
                        snippet["text"].rstrip(),
                        "```",
                    ]
                )
            )
        if evidence["unresolved"]:
            chunks.append(
                "Unresolved source-locator spans remain available in static_handoff.json; "
                "do not invent their source text."
            )
        return "\n\n".join(chunks)

    # The task must remain usable in a fresh conversation even when the local
    # Scala checkout is unavailable. FIRRTL statements plus exact locators are
    # therefore always a complete fallback evidence representation.
    return (
        "No source root was supplied/resolved. Use the FIRRTL statement ledger "
        "below and its exact source locators; do not guess missing Scala text."
    )


def _render_statement_ledger(handoff: dict[str, Any]) -> str:
    lines = []
    for statement in handoff["statements"]:
        source = statement["source"]
        if source is None:
            source_text = "<no-source-locator>"
        else:
            column = f":{source['column']}" if source.get("column") is not None else ""
            source_text = f"{source['file']}:{source['line']}{column}"
        lines.append(
            f"[{statement['id']}] FIRRTL:{statement['firrtl_line']} "
            f"SRC:{source_text} KIND:{statement['kind']} :: {statement['text']}"
        )
    return "\n".join(lines)


def _render_event_table(handoff: dict[str, Any]) -> str:
    chunks = []
    cones = {cone["event_id"]: cone for cone in handoff["semantic_event_cones"]}
    for event in handoff["events"]:
        cone = cones.get(event["id"], {})
        chunks.append(
            "\n".join(
                [
                    f"- `{event['id']}`",
                    f"  - predicate: `{event['predicate']}`",
                    f"  - direction/protocol: `{event['direction']}` / `{event['protocol']}`",
                    f"  - payload leaves: {event['payload']}",
                    f"  - immediate registers: {cone.get('immediate_registers', [])}",
                    f"  - historical registers: {cone.get('historical_registers', [])}",
                ]
            )
        )
    return "\n".join(chunks)



def _render_child_summaries(handoff: dict[str, Any]) -> str:
    composition = handoff.get("composition", {})
    summaries = composition.get("child_summaries", []) if isinstance(composition, dict) else []
    chunks: list[str] = []
    parent_work_unit_id = str(handoff.get("work_unit", {}).get("id", ""))
    for child in summaries:
        if not isinstance(child, dict):
            continue
        child_id = child.get("child_id", "<unknown-child>")
        interface = build_prompt_interface(
            child,
            parent_work_unit_id=parent_work_unit_id,
        )
        chunks.append(
            "\n".join(
                [
                    f"### Child `{child_id}`",
                    "This is the complete LLM-visible semantic contract for this child. "
                    "Opaque imports are typed atoms referenced by a direct trusted theorem; "
                    "do not infer their hidden definitions or proof history.",
                    "```json",
                    json.dumps(
                        interface,
                        ensure_ascii=False,
                        separators=(",", ":"),
                        sort_keys=True,
                    ),
                    "```",
                ]
            )
        )
    return "\n\n".join(chunks)

def _output_template(task: LLMTask) -> dict[str, Any]:
    return {
        "schema_version": UMCM_SCHEMA_VERSION,
        "task_id": task.task_id,
        "work_unit_id": task.work_unit_id,
        "occurrences": [],
        "predicates": [],
        "identity_keys": [],
        "cases": [],
        "axioms": [],
        "assumptions": [],
        "unresolved": [],
        "rationale": [],
        "extensions": {},
    }


def render_leaf_abstraction_prompt(
    task: LLMTask,
    handoff: dict[str, Any],
) -> str:
    unit = handoff["work_unit"]
    complexity = handoff["complexity"]
    state_ids = [state["id"] for state in handoff["state"]]
    frontier_ids = [entry["id"] for entry in handoff["frontier"]]
    template = json.dumps(_output_template(task), indent=2, sort_keys=False)

    return f"""# MCM-Agent manual semantic task: leaf µMCM abstraction

You are performing one experimental semantic-abstraction step in MCM-Agent.
This prompt is self-contained and may be used in a fresh conversation.

## Research status

The static hierarchical planner is already complete. Do **not** repartition RTL.
This is a manual-first experiment, but "manual" only means that a human transports
the exported prompt and returned result between the workflow and the LLM. The
human is **not** expected to co-design each leaf abstraction. Analyze this WorkUnit
autonomously and derive the most conservative grounded candidate abstraction that
preserves information potentially relevant to microarchitectural memory ordering.
The µMCM language remains experimental and may be revised when new RTL/formal
evidence exposes a real reusable gap.

Task ID: `{task.task_id}`
Workflow version: `{task.workflow_version}`
Prompt version: `{task.prompt_version}`
Output schema version: `{task.schema_version}`

## WorkUnit

- id: `{unit['id']}`
- module: `{unit['module']}`
- kind: `{unit['kind']}`
- instance path: `{unit['instance_path']}`
- leaf: `{unit['is_leaf']}`
- coverage complete: `{unit['coverage_complete']}`
- raw statements: {complexity['raw']['statements']}
- logical statements: {complexity['logical']['statements']}
- mapped/logical source lines: {complexity['logical']['source_loc']}
- registers: {complexity['registers']}
- physical boundary events: {complexity['events']}

## Non-negotiable grounding rules

1. Distinguish occurrences from persistent predicates. A boundary occurrence
   must reference one or more physical event IDs listed below. A derived
   occurrence may have no physical event ID only when it has an exact RTL
   definition, concrete grounding, and statement evidence. If one semantic
   occurrence depends on a multi-bit comparison, record it in grounding as
   `value_tests`, for example
   `{{"expr":{{"op":"signal","name":"io.source"}},"relation":"eq","value":3}}`;
   prose in `definition` is not formal grounding.
   occurrence repeats over a finite hardware index (beat/entry/bank/etc.), use
   the optional occurrence `index` metadata instead of inventing N separate IDs. Do not turn ordinary
   FSM staging states into milestones unless deleting the milestone would lose
   memory/coherence ordering, path, visibility, identity, or exclusion facts.
2. Persistent predicates describe facts that can remain true across cycles. They
   must have a grounded RTL definition/source signal or explicit state set.
3. Every candidate case/axiom/predicate/identity claim must cite supporting
   FIRRTL statement IDs from the ledger. If evidence is insufficient, put the
   issue in `unresolved` rather than guessing.
4. Distinguish an RTL guarantee from an environment assumption. In particular,
   do not claim eventual progress from a ready/valid interface without stating
   the fairness/readiness assumption required for it.
5. Preserve transaction/object identity when an ordering claim is only true for
   the same request/cache line/source/transaction.
6. Do not dump every FSM transition. Keep predicates/cases only when they affect which
   memory/coherence event can occur, object identity, exclusion/conservation, or
   ordering/visibility-relevant paths.
7. Every axiom must be expressed in the structured `formal` AST defined by
   `expected_output_schema.json`. The formal AST is the only semantic source of
   truth. Do **not** provide a separate natural-language `formula` or an LLM-authored
   `validation` program; both the human rendering and proof obligations are
   generated deterministically from the AST.
8. Use only formal axiom forms supported by the schema. The language includes
   generic `join` and `indexed_complete` forms for unordered prerequisites and
   finite indexed occurrence sets. For exact same-cycle event routing or merging,
   use `occurrence_partition`: `whole` is equivalent to the disjunction of `parts`,
   and the parts are pairwise mutually exclusive in that cycle. Its exact shape is:
   `{{"type":"occurrence_partition","whole":"OutputFire","parts":["Input0Fire","Input1Fire"],"relation":"same_cycle_exactly_one","scope_identity":null}}`.
   The `relation` field is required and must not be omitted. `parts` may contain
   one occurrence for an exact 1-to-1 passthrough; pairwise exclusion is then
   vacuous and the relation reduces to same-cycle equivalence. Existing relation axioms may additionally use
   `scope_index: {{name: <index>, relation: same}}` to state that the relation is
   pointwise over the same finite index (beat/entry/bank/etc.). Formal expressions
   may use `index_var` and `lookup` to refer to the bound index and an indexed
   storage element. These constructs are protocol-agnostic and must not be
   specialized to a particular module. For a synchronous mutable array whose
   read returns the latest prior same-key write, use `indexed_storage_flow`.
   It binds address/lane keys, masked writes, sampled reads, initialization, and
   the stored value layout, and exports the standard relations: `rf` selects the
   co-latest prior same-key write, `co` is a strict total order over writes to
   each key, and `fr` is derived as `rf^-1 ; co`. Relation names must be distinct;
   do not state `rf`, `co`, and `fr` as unrelated ordering approximations.
   Use `initialization.kind: explicit` only for a grounded initialization sweep,
   with `initial_value` on every value field. For RAM without a specified
   power-up/reset value, use `initialization: {{"kind":"implicit_unconstrained"}}`
   and omit every `initial_value`; this creates one fresh unconstrained initial
   write per key while preserving the same `rf/co/fr` definitions. The optional
   `read_write_collision` is `exclusive` by default; use
   `implicit_unconstrained` only when same-key synchronous read/write collision
   is possible and the RAM result is unspecified. This introduces a transient
   unconstrained abstract write as the collision read's `rf` source, immediately
   before the colliding real write in `co`. If a semantic property that you judge
   **necessary** for a sound/useful parent-facing abstraction cannot be faithfully
   represented by the current Formal AST, do not approximate it with a different
   or weaker axiom. Report a `MCM-AGENT LANGUAGE GAP` using the procedure below.
   A limitation of the current formal prover is **not** a language gap: if the AST
   can express the property, emit the candidate axiom and let `semantic-validate`
   determine whether the backend can certify it.
9. This stage proposes **candidate** axioms. Do not assert that formal validation
   has already proved them.
10. Do not treat every potentially useful strengthening as a blocker. If omitting
    a constraint merely makes the candidate µMCM a safer over-approximation, you
    may omit it and record the deliberate omission in `rationale` as a possible
    later CEGAR refinement. Reserve `unresolved` for genuine grounding/semantic
    uncertainty that prevents you from making a responsible candidate claim.

## Physical boundary events

{_render_event_table(handoff)}

## Concrete local state

{state_ids}

## Environment/frontier signals

{frontier_ids}

## Source evidence

{_render_source_evidence(handoff)}

## Grounded FIRRTL statement ledger

Every statement ID below is allowed evidence for this WorkUnit. Statements not
in this ledger must not be cited.

```text
{_render_statement_ledger(handoff)}
```

## Autonomous decision procedure

Analyze the entire WorkUnit autonomously. Do **not** stop after proposing a
semantic decomposition, and do **not** ask the human to choose occurrences,
predicates, identities, cases, axioms, or assumptions. When several abstractions
are plausible, choose the most conservative one that is grounded by the supplied
RTL evidence.

There are exactly two expected outcomes for this task:

1. **Current language is sufficient.** Build the complete candidate with the
   current schema and emit `FINAL MCM-AGENT RESULT` in this same response. Do this
   even when you are unsure whether the current prover can certify every candidate
   axiom; prover capability is decided later by `semantic-validate`.
2. **Current language has a real gap.** Use this outcome only when a
   memory/coherence-relevant semantic property is necessary for the abstraction
   but cannot be faithfully expressed by any current Formal AST form. Emit a
   section named `MCM-AGENT LANGUAGE GAP` and state:
   - the missing semantic concept;
   - the grounded RTL behavior that requires it;
   - why the current AST cannot express it without changing meaning;
   - the minimal **generic/reusable** extension you propose;
   - representative other hardware patterns that could reuse the extension.
   Do not emit an approximate candidate axiom just to avoid reporting the gap.

While analyzing, answer questions such as:

- Which physical events correspond to meaningful boundary occurrences, and is
  any RTL-grounded internal milestone needed to preserve an ordering fact?
- Which facts are persistent predicates rather than instantaneous occurrences?
- What stored state carries request/cache-line/transaction identity across cycles?
- Which case distinctions change the event path or ordering constraints?
- Which ordering, exclusion, flow, or conservation properties are actually
  supported by RTL?
- Which apparent liveness properties require environment assumptions?
- Which RTL details can be dropped without losing bug-relevant behavior?

## Formal axiom rule

Each `axioms[].formal` object is the axiom itself. The workflow derives its
human-readable formula, references, checker, and proof obligation from that AST.
This prevents a prose axiom from silently diverging from what the verifier proves.
Consult `expected_output_schema.json` for the exact allowed AST variants.

## Final machine result

If the current language is sufficient, this response **must** include a final
section named `FINAL MCM-AGENT RESULT` followed by one fenced JSON object. Do not
wait for another human turn before emitting it. The object must match
`expected_output_schema.json`. Use this exact envelope as the starting shape.

If and only if the current language has a necessary semantic gap, emit
`MCM-AGENT LANGUAGE GAP` instead of fabricating an approximate final JSON. A
formal-backend proof limitation alone never selects this path.

```json
{template}
```

IDs inside each list must be unique and stable within this result. Physical
references must use the exact IDs from this prompt. Evidence must use integer
statement IDs from the ledger.
"""



def render_parent_synthesis_prompt(
    task: LLMTask,
    handoff: dict[str, Any],
) -> str:
    unit = handoff["work_unit"]
    complexity = handoff["replacement_complexity"]
    state_ids = [state["id"] for state in handoff["state"]]
    frontier_ids = [entry["id"] for entry in handoff["frontier"]]
    template = json.dumps(_output_template(task), indent=2, sort_keys=False)

    return f"""# MCM-Agent manual semantic task: parent µMCM synthesis

You are performing one bottom-up semantic-composition step in MCM-Agent.
This prompt is self-contained and may be used in a fresh conversation.

## Research status

The static hierarchical planner is already complete. Do **not** repartition RTL.
This is a parent-synthesis task. Every direct child listed below is already
`FROZEN_FOR_COMPOSITION`. Child RTL is **not an input** to this task and must not
be reconstructed, guessed, or re-read. Treat each frozen child µMCM as a trusted
semantic component and combine it only with the parent-local RTL evidence below.

The human is transport-only. Analyze the parent autonomously. If the current
µMCM Formal AST is sufficient, emit the complete candidate in this response. If
a necessary parent-level semantic concept cannot be represented faithfully,
report `MCM-AGENT LANGUAGE GAP`. If the AST can express a property but the current
formal backend may not prove a relation spanning imported child semantics, still
emit the candidate; that is a composition-prover gap, not a language gap.

Task ID: `{task.task_id}`
Workflow version: `{task.workflow_version}`
Prompt version: `{task.prompt_version}`
Output schema version: `{task.schema_version}`

## Parent WorkUnit

- id: `{unit['id']}`
- module: `{unit['module']}`
- kind: `{unit['kind']}`
- instance path: `{unit['instance_path']}`
- leaf: `{unit['is_leaf']}`
- coverage complete: `{unit['coverage_complete']}`
- parent-local raw statements after child replacement: {complexity['raw']['statements']}
- parent-local logical statements after child replacement: {complexity['logical']['statements']}
- parent-local registers: {complexity['registers']}
- parent-local physical boundary events: {complexity['events']}

## Composition rules

1. Frozen child axioms are already trusted and remain imported automatically when
   this parent is frozen. Do **not** mechanically copy every child axiom into the
   parent candidate. Grounding signals/state/evidence stored inside a frozen child
   summary are provenance only: do not treat them as parent-local RTL evidence or
   infer new child behavior beyond the trusted frozen semantics.
2. Child semantic objects may be referenced only by the exact qualified IDs in
   each compact child interface's `exported_ids`. A direct theorem's Formal AST
   uses child-local IDs for local declarations; use their `qualified_id` from the
   interface when referencing them in the parent candidate. Opaque imports are
   usable only as typed semantic atoms: do not infer their hidden definitions.
   Do not redeclare an imported occurrence, predicate, identity, or axiom.
3. New boundary occurrences may reference parent-local physical events and the
   exposed child boundary events. New derived occurrences must be grounded only
   in parent-local RTL; child internal state/signals are not available.
4. `evidence_statement_ids` in this result may cite only the parent-local statement
   ledger below. Child provenance belongs in `extensions`, not in fabricated
   parent statement evidence.
5. For every new parent axiom, fill:
   `extensions.parent_synthesis.axiom_provenance[<axiom-id>]` with:
   - `kind`: one of `parent_local`, `reexported`, `lifted`, `emergent`;
   - `source_axioms`: zero or more exact qualified IDs from the imported child
     `exported_ids.axioms` lists;
   - `note`: a short explanation.
   `parent_local` normally has no child source axioms. `lifted`, `emergent`, or
   `reexported` must cite at least one imported source axiom.
6. It is valid for this parent to declare **zero new axioms** when the wrapper adds
   no additional memory/coherence-relevant constraint. The frozen parent will
   still retain the frozen child imports. Do not invent redundant axioms merely
   to avoid an empty parent-local candidate.
7. The trusted child summaries are not assumed complete forever. Omitting an
   optional strengthening is a safe over-approximation and may be recorded in
   `rationale` for later CEGAR refinement.
8. Do not claim liveness without an explicit environment assumption.
9. Candidate axioms remain candidates until deterministic/formal validation.

## Parent-local physical events

{_render_event_table(handoff)}

## Parent-local concrete state

{state_ids}

## Parent frontier signals

{frontier_ids}

## Frozen child summaries

{_render_child_summaries(handoff)}

## Parent-local source evidence

{_render_source_evidence(handoff)}

## Parent-local FIRRTL statement ledger

Only these parent-local statement IDs may appear in `evidence_statement_ids`.

```text
{_render_statement_ledger(handoff)}
```

## Autonomous decision procedure

Synthesize the most conservative parent-facing abstraction that preserves
memory/coherence ordering, visibility, identity, exclusion, conservation, and
path facts contributed by the combination of frozen children plus parent-local
RTL.

There are exactly two expected outcomes:

1. **Current language is sufficient.** Emit `FINAL MCM-AGENT RESULT` followed by
   one fenced JSON object matching `expected_output_schema.json` in this response.
2. **Current language has a real gap.** Emit `MCM-AGENT LANGUAGE GAP` and explain
   the grounded missing concept, why existing AST forms change its meaning, and
   the minimal reusable extension. A missing composition proof capability is not
   a language gap.

For the normal JSON outcome, use this exact envelope:

```json
{template}
```

For a parent result, `extensions` should normally have this shape:

```json
{{
  "parent_synthesis": {{
    "axiom_provenance": {{
      "A1": {{
        "kind": "parent_local",
        "source_axioms": [],
        "note": "..."
      }}
    }}
  }}
}}
```

IDs inside each list must be unique and stable. Physical references and
parent-local evidence must use exact IDs from this prompt.
"""


def build_parent_synthesis_task(handoff: dict[str, Any]) -> PromptPackage:
    if handoff["work_unit"]["is_leaf"]:
        raise ValueError(
            f"ParentSynthesisTask requires a non-leaf WorkUnit, got {handoff['work_unit']['id']}"
        )
    if not handoff["work_unit"]["coverage_complete"]:
        raise ValueError("ParentSynthesisTask requires complete static coverage")
    composition = handoff.get("composition", {})
    children = handoff.get("children", [])
    summaries = composition.get("child_summaries", []) if isinstance(composition, dict) else []
    if len(summaries) != len(children) or not summaries:
        raise ValueError(
            "ParentSynthesisTask requires one frozen child summary for every direct child"
        )

    kind = TaskKind.PARENT_SYNTHESIS
    task = LLMTask(
        task_id=_stable_task_id(
            kind,
            handoff,
            prompt_version=PARENT_PROMPT_VERSION,
        ),
        kind=kind,
        work_unit_id=handoff["work_unit"]["id"],
        schema_version=UMCM_SCHEMA_VERSION,
        prompt_version=PARENT_PROMPT_VERSION,
        workflow_version=WORKFLOW_VERSION,
        provider_mode="manual_conversation",
    )
    schema = candidate_output_schema()
    return PromptPackage(
        task=task,
        static_handoff=handoff,
        expected_output_schema=schema,
        prompt=render_parent_synthesis_prompt(task, handoff),
    )


def build_leaf_abstraction_task(handoff: dict[str, Any]) -> PromptPackage:
    if not handoff["work_unit"]["is_leaf"]:
        raise ValueError(
            f"LeafAbstractionTask requires a leaf WorkUnit, got {handoff['work_unit']['id']}"
        )
    if not handoff["work_unit"]["coverage_complete"]:
        raise ValueError("LeafAbstractionTask requires complete static coverage")

    kind = TaskKind.LEAF_ABSTRACTION
    task = LLMTask(
        task_id=_stable_task_id(kind, handoff),
        kind=kind,
        work_unit_id=handoff["work_unit"]["id"],
        schema_version=UMCM_SCHEMA_VERSION,
        prompt_version=PROMPT_VERSION,
        workflow_version=WORKFLOW_VERSION,
        provider_mode="manual_conversation",
    )
    schema = candidate_output_schema()
    return PromptPackage(
        task=task,
        static_handoff=handoff,
        expected_output_schema=schema,
        prompt=render_leaf_abstraction_prompt(task, handoff),
    )
