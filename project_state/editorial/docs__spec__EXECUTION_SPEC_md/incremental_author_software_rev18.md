# Incremental software-author review

**File:** `docs/spec/EXECUTION_SPEC.md`  
**Region:** Runtime artifact retention and visualization execution

Preserve all previously adjudicated surrounding content. For this region, require exact correspondence with the current implementation. No claim of persistent cache or recomputation avoidance beyond the current in-memory run.

Proposed treatment: keep the change local; name the concrete result objects/functions involved; state runtime-versus-persisted behavior explicitly where relevant; avoid implying APIs or persistence mechanisms that are not implemented.

Acceptance: every syntax/behavior claim in the changed region is executable or directly supported by source.
