# Run Summary — LSU::region-0-6

## Identity

- task: `leaf_abstraction-LSU-region-0-6-664eff0e43733fd6`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.11`
- schema: `umcm-formal-0.5`
- workflow status: `FORMALLY_VALIDATED`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 7
- predicates: 5
- identity keys: 0
- cases: 0
- candidate axioms: 20
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 20
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 20
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] DCacheRequest <=> exactly_one_same_cycle({LoadExecuteRequest, LoadRetryRequest, StoreCommitRequest, LoadWakeupRequest, HellaIncomingRequest, HellaWakeupRequest})
- `A2` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = exe_tlb_paddr[0] on LoadExecuteRequest
- `A3` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = exe_tlb_paddr[0] on LoadRetryRequest
- `A4` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = stq_execute_queue.io.deq.bits.addr.bits on StoreCommitRequest
- `A5` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = ldq_wakeup_e.bits.addr.bits on LoadWakeupRequest
- `A6` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = exe_tlb_paddr[0] on HellaIncomingRequest
- `A7` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.addr = hella_paddr on HellaWakeupRequest
- `A8` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 0 on LoadExecuteRequest
- `A9` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 0 on LoadRetryRequest
- `A10` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 0 on StoreCommitRequest
- `A11` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 0 on LoadWakeupRequest
- `A12` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 1 on HellaIncomingRequest
- `A13` [FORMALLY_PROVED] bits(io.dmem.req.bits[0].bits.is_hella, 0, 0) == 1 on HellaWakeupRequest
- `A14` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.uop.mem_cmd = hella_req.cmd on HellaIncomingRequest
- `A15` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.uop.mem_cmd = hella_req.cmd on HellaWakeupRequest
- `A16` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.uop.mem_size = hella_req.size on HellaIncomingRequest
- `A17` [FORMALLY_PROVED] io.dmem.req.bits[0].bits.uop.mem_size = hella_req.size on HellaWakeupRequest
- `A18` [FORMALLY_PROVED] RetryOrderBlock => !LoadRetryRequest
- `A19` [FORMALLY_PROVED] WakeupOrderBlock => !LoadWakeupRequest
- `A20` [FORMALLY_PROVED] UncacheableWakeupOrderBlocked => !LoadWakeupRequest

## Next action

The formally proved axioms may be frozen into the trusted leaf µMCM.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
