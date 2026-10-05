# Human-facing revision and release task list

Status: **complete**

This task list governs the incremental documentation pass following the visualization implementation. It applies the durable-adjudication rule in `project_state/EDITORIAL_DRAFTING_PROTOCOL.md`: previously adjudicated content is preserved unless its meaning or instructional function changed.

## hf_task_001 — Inventory adjudication state

**Status:** complete

Classify every product-facing root file, documentation page, example, and example README as `adjudicated_unchanged`, `adjudicated_editorial_change`, `requires_re_adjudication`, or `new_unadjudicated`.

## hf_task_002 — Reconcile visualization entry points

**Status:** complete

Incrementally revise `README.md` and `docs/index.md` so the visualization surface is introduced once, placed in the instructional trajectory, and linked to the complete guide/demo without rewriting unrelated adjudicated prose.

## hf_task_003 — Reconcile reference specifications

**Status:** complete

Update only the visualization/runtime-artifact regions of `docs/spec/API_SPEC.md`, `DATA_MODEL_SPEC.md`, and `EXECUTION_SPEC.md` so signatures, persistence boundaries, runtime requirements, and plotting behavior match the implementation exactly.

## hf_task_004 — Re-adjudicate changed visualization ontology regions

**Status:** complete

Review the implementation mapping and any post-adjudication ontology changes while preserving the previously adjudicated question/tier/inference-boundary definitions.

## hf_task_005 — Adjudicate new visualization support documents

**Status:** complete

Review `docs/VISUALIZATION_TASKS.md`, `docs/VISUALIZATION_VALIDATION.md`, and the new release/demo support material for accuracy, scope, and instructional role.

## hf_task_006 — Adjudicate demonstration scripts and reference READMEs

**Status:** complete

Review the human-facing docstrings/comments, execution contract, reproducibility statements, generated-bundle description, and claim boundaries in `examples/complete_visualization_demo.py`, `examples/eigenflow_colab_visualization_demo.py`, and `examples/visualization_demo_reference/*.md`.

## hf_task_007 — Refresh documentation audit and validation records

**Status:** complete

Update the historical audit/validation documents so they distinguish the completed original remediation phase from the visualization-phase additions and do not report already-resolved tasks as open.

## hf_task_008 — Write region-level adjudication ledger and provenance

**Status:** complete

Record which regions were preserved, lightly verified, or fully re-adjudicated; retain four role-separated author reviews and board adjudication for new/materially changed regions; refresh final hashes.

## hf_task_009 — Run repository/documentation validation

**Status:** complete

Run the Python tests, executable examples, compilation checks, local Markdown link/image checks, metadata parsing, visualization reference checksum checks, and source/spec reconciliation.

## hf_task_010 — Reconcile canonical project state

**Status:** complete

Update `project_state/project_state.json` and `execution_manifest.json` with task completion, adjudication ledger location, validation outcome, and the next resume point.

## hf_task_011 — Prepare the complete Git repository ZIP

**Status:** complete

Package the full repository, including `.git`, source, tests, generated documentation assets, editorial provenance, and project state. Preserve compatibility with the user's current remote baseline at commit `9ca109c327f0af3fcd99c79f08451748d2b8c839`.
