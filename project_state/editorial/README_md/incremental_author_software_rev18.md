# Incremental software-author review

**File:** `README.md`  
**Region:** Visualization section

Preserve all previously adjudicated surrounding content. For this region, require exact correspondence with the current implementation. Public API calls, runtime-artifact persistence boundary, and links to real generated examples must match implementation.

Proposed treatment: keep the change local; name the concrete result objects/functions involved; state runtime-versus-persisted behavior explicitly where relevant; avoid implying APIs or persistence mechanisms that are not implemented.

Acceptance: every syntax/behavior claim in the changed region is executable or directly supported by source.
