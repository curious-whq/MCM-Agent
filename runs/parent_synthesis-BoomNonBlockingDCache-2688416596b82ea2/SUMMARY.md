# Run Summary — BoomNonBlockingDCache

## Identity

- task: `parent_synthesis-BoomNonBlockingDCache-2688416596b82ea2`
- kind: `parent_synthesis`
- workflow: `manual-first-workflow-0.9`
- prompt: `parent-synthesis-prompt-0.4`
- schema: `umcm-formal-0.5`
- workflow status: `FROZEN_FOR_COMPOSITION`

## Grounding

- valid: `True`
- errors: 0
- warnings: 0

## Candidate µMCM

- occurrences: 15
- predicates: 3
- identity keys: 0
- cases: 0
- candidate axioms: 27
- unresolved: 0

## Validation

- GROUNDED: 0
- PARTIALLY_SUPPORTED: 0
- STRUCTURALLY_SUPPORTED: 0
- FORMALLY_PROVED: 27
- SPEC_PROVED: 0
- REFUTED: 0
- trusted axioms: 27
- formal backend: `explicit-control`

## Axioms

- `A1` [FORMALLY_PROVED] MemAcquire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs::MemAcquire})
- `A2` [FORMALLY_PROVED] MemFinish <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs::MemFinish})
- `A3` [FORMALLY_PROVED] LongLatencyResp <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs::RespHandshake})
- `A4` [FORMALLY_PROVED] LSURelease <=> exactly_one_same_cycle({BoomNonBlockingDCache.lsu_release_arb::OutputFire})
- `A5` [FORMALLY_PROVED] BoomNonBlockingDCache.lsu_release_arb::Input0Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.wb::LSURelease})
- `A6` [FORMALLY_PROVED] BoomNonBlockingDCache.lsu_release_arb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.prober::LSURelease})
- `A7` [FORMALLY_PROVED] BoomNonBlockingDCache.wb::WritebackReq <=> exactly_one_same_cycle({BoomNonBlockingDCache.wbArb::OutputFire})
- `A8` [FORMALLY_PROVED] BoomNonBlockingDCache.wbArb::Input0Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.prober::WBReq})
- `A9` [FORMALLY_PROVED] BoomNonBlockingDCache.wbArb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs::WBReq})
- `A10` [FORMALLY_PROVED] BoomNonBlockingDCache.meta_0::MetadataWrite <=> exactly_one_same_cycle({BoomNonBlockingDCache.metaWriteArb::OutputFire})
- `A11` [FORMALLY_PROVED] BoomNonBlockingDCache.metaWriteArb::Input0Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs::MetaWrite})
- `A12` [FORMALLY_PROVED] BoomNonBlockingDCache.metaWriteArb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.prober::MetaWrite})
- `A13` [FORMALLY_PROVED] BoomNonBlockingDCache.meta_0::ReadRequest <=> exactly_one_same_cycle({BoomNonBlockingDCache.metaReadArb::OutputFire})
- `A14` [FORMALLY_PROVED] BoomNonBlockingDCache.metaReadArb::Input3Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs::MetaRead})
- `A15` [FORMALLY_PROVED] BoomNonBlockingDCache.metaReadArb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.prober::MetaRead})
- `A16` [FORMALLY_PROVED] BoomNonBlockingDCache::region-0-3::MSHRReqFire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs::RequestAccept})
- `A17` [FORMALLY_PROVED] BoomNonBlockingDCache.dataWriteArb::Input1Fire <=> exactly_one_same_cycle({BoomNonBlockingDCache.mshrs::Refill})
- `A18` [FORMALLY_PROVED] ProbeFire <=> exactly_one_same_cycle({BoomNonBlockingDCache::region-0-0::ProbeFire})
- `A19` [FORMALLY_PROVED] StoreAckValid <=> exactly_one_same_cycle({BoomNonBlockingDCache::region-0-3::StoreAckValid})
- `A20` [FORMALLY_PROVED] HitStoreAck <=> exactly_one_same_cycle({BoomNonBlockingDCache::region-0-3::HitStoreAck})
- `A21` [FORMALLY_PROVED] MissAllocatedStoreAck <=> exactly_one_same_cycle({BoomNonBlockingDCache::region-0-3::MissAllocatedStoreAck})
- `A22` [FORMALLY_PROVED] RequestAccept <=> exactly_one_same_cycle({BoomNonBlockingDCache::region-0-4::RequestAccept})
- `A23` [FORMALLY_PROVED] LRSCValid => !ProbeFire
- `A28` [FORMALLY_PROVED] DBeat <=> exactly_one_same_cycle({ReleaseAck, MemGrant})
- `A29` [FORMALLY_PROVED] StoreAckValid <=> exactly_one_same_cycle({HitStoreAck, MissAllocatedStoreAck})
- `A30` [FORMALLY_PROVED] LongLatencyRespPending => !RequestAccept
- `A31` [FORMALLY_PROVED] bits(io.lsu.s1_nack_advisory[0], 0, 0) == 0

## Certified provenance

- `A1` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A10` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A11` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A12` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A13` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A14` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A15` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A16` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A17` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A18` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A19` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A2` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A20` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A21` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A22` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A23` [lifted; trusted-child-lift] <- `BoomNonBlockingDCache::region-0-0::A1`
- `A28` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A29` [emergent; trusted-occurrence-partition-substitution] <- `BoomNonBlockingDCache::region-0-3::A9`
- `A3` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A30` [lifted; trusted-child-lift] <- `BoomNonBlockingDCache::region-0-4::A1`
- `A31` [lifted; trusted-child-value-lift] <- `BoomNonBlockingDCache.data::A5`
- `A4` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A5` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A6` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A7` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A8` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof
- `A9` [parent_local; exact-parent-child-occurrence-partition] <- parent-local proof

## Next action

A higher parent synthesis step may consume frozen_umcm.json; reopen only through counterexample-guided refinement.

## Durable experiment notes

See `EXPERIENCE.md` in this run directory. Keep only lessons that should influence future prompts/schema/validators/synthesis.
