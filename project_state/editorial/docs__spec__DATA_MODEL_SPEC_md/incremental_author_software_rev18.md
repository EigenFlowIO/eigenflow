# Incremental software-author review

**File:** `docs/spec/DATA_MODEL_SPEC.md`  
**Region:** LayerResult/ExperimentResult runtime artifacts

Preserve all previously adjudicated surrounding content. For this region, require exact correspondence with the current implementation. Dataclass signatures must include artifacts; JSON omission must be explicit.

Proposed treatment: keep the change local; name the concrete result objects/functions involved; state runtime-versus-persisted behavior explicitly where relevant; avoid implying APIs or persistence mechanisms that are not implemented.

Acceptance: every syntax/behavior claim in the changed region is executable or directly supported by source.
