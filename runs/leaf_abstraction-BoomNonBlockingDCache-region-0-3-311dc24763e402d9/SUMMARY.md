# Run Summary — BoomNonBlockingDCache::region-0-3

## Identity

- task: `leaf_abstraction-BoomNonBlockingDCache-region-0-3-311dc24763e402d9`
- kind: `leaf_abstraction`
- workflow: `manual-first-workflow-0.9`
- prompt: `leaf-abstraction-prompt-0.11`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 11
- predicates: 5
- identity keys: 0
- cases: 10
- candidate axioms: 30
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 30
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 30
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] S2Invalid => !RespValid
- `A2` [FORMALLY_PROVED] S2Invalid => !NackValid
- `A3` [FORMALLY_PROVED] S2Invalid => !StoreAckValid
- `A4` [FORMALLY_PROVED] S2Invalid => !MSHRReqFire
- `A5` [FORMALLY_PROVED] S2Miss => !RespValid
- `A6` [FORMALLY_PROVED] S2NoNack => !NackValid
- `A7` [FORMALLY_PROVED] S2Nack => !StoreAckValid
- `A8` [FORMALLY_PROVED] S2Hit => !MSHRReqFire
- `A9` [FORMALLY_PROVED] StoreAckValid <=> exactly_one_same_cycle({HitStoreAck, MissAllocatedStoreAck})
- `A10` [FORMALLY_PROVED] RespValid <=> exactly_one_same_cycle({RespFromS3, RespFromS4, RespFromS5, RespFromArray})
- `A11` [FORMALLY_PROVED] s2_data_word[0] = s3_req.data on RespFromS3
- `A12` [FORMALLY_PROVED] s2_data_word[0] = s4_req.data on RespFromS4
- `A13` [FORMALLY_PROVED] s2_data_word[0] = s5_req.data on RespFromS5
- `A14` [FORMALLY_PROVED] s2_data_word[0] = s2_data_word_prebypass[0] on RespFromArray
- `A15` [FORMALLY_PROVED] io.lsu.resp[0].bits.data = s2_sc_fail on SCResponse
- `A16` [FORMALLY_PROVED] io.lsu.nack[0].bits.addr = s2_req[0].addr on NackValid
- `A17` [FORMALLY_PROVED] io.lsu.nack[0].bits.data = s2_req[0].data on NackValid
- `A18` [FORMALLY_PROVED] io.lsu.nack[0].bits.uop.mem_cmd = s2_req[0].uop.mem_cmd on NackValid
- `A19` [FORMALLY_PROVED] io.lsu.nack[0].bits.uop.rob_idx = s2_req[0].uop.rob_idx on NackValid
- `A20` [FORMALLY_PROVED] io.lsu.nack[0].bits.uop.ldq_idx = s2_req[0].uop.ldq_idx on NackValid
- `A21` [FORMALLY_PROVED] io.lsu.nack[0].bits.uop.stq_idx = s2_req[0].uop.stq_idx on NackValid
- `A22` [FORMALLY_PROVED] io.lsu.store_ack[0].bits.addr = s2_req[0].addr on StoreAckValid
- `A23` [FORMALLY_PROVED] io.lsu.store_ack[0].bits.uop.mem_cmd = s2_req[0].uop.mem_cmd on StoreAckValid
- `A24` [FORMALLY_PROVED] io.lsu.store_ack[0].bits.uop.rob_idx = s2_req[0].uop.rob_idx on StoreAckValid
- `A25` [FORMALLY_PROVED] io.lsu.store_ack[0].bits.uop.stq_idx = s2_req[0].uop.stq_idx on StoreAckValid
- `A26` [FORMALLY_PROVED] io.lsu.resp[0].bits.uop.mem_cmd = s2_req[0].uop.mem_cmd on RespValid
- `A27` [FORMALLY_PROVED] io.lsu.resp[0].bits.uop.mem_size = s2_req[0].uop.mem_size on RespValid
- `A28` [FORMALLY_PROVED] io.lsu.resp[0].bits.uop.rob_idx = s2_req[0].uop.rob_idx on RespValid
- `A29` [FORMALLY_PROVED] io.lsu.resp[0].bits.uop.ldq_idx = s2_req[0].uop.ldq_idx on RespValid
- `A30` [FORMALLY_PROVED] io.lsu.resp[0].bits.uop.stq_idx = s2_req[0].uop.stq_idx on RespValid

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
