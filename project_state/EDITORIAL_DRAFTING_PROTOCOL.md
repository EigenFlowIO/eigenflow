# Antagonistic Documentation Drafting Protocol

For each human-facing documentation unit, use a seven-role workflow.

## Independent author round

Each author receives the same canonical project state, document objective, section trajectory map, implementation state, and relevant source files. Authors draft independently.

1. **Technical software developer and documentation writer**
   - optimizes for API fidelity, runnable syntax, codebase consistency, installation and operational usefulness;
   - rejects documentation that promises functionality not implemented.

2. **Academic author for a computational interpretability journal**
   - optimizes for conceptual precision, formal definitions, scholarly framing, claim discipline, and relationship to the interpretability problem.

3. **Research methods author for research practitioners**
   - optimizes for instructional sequence, experiment design, examples, practice decisions, and transfer to real research workflows.

4. **Computational statistics professor with computational research-design background**
   - optimizes for identification, measurement assumptions, robustness, sensitivity, uncertainty, interpretation of results, and alternative explanations.

Authors should disagree when their objectives genuinely conflict. They must not merely paraphrase one another.

## Editorial board

The four drafts are referred to three editors.

1. **Software codebase team lead**
   - checks implementation fidelity, package architecture, exact syntax, version behavior, result access, examples, and maintainability.

2. **Compliance and liability counselor**
   - checks overclaiming, unsupported causal/semantic claims, safety/security boundaries, licensing/compliance implications, and language that could misrepresent scientific certainty.

3. **Clarity and communication editor**
   - checks conceptual chunking, prerequisite order, terminology, cognitive load, examples, redundancy, and whether the document reaches its defined terminal reader state.

## Board decision

The board produces an adjudication record that identifies:

- contributions to retain from each draft;
- conflicts between drafts;
- implementation/doc mismatches;
- epistemic or liability concerns;
- missing prerequisites;
- unnecessary material;
- synthesis order;
- acceptance criteria for the final document.

No individual draft is adopted wholesale unless the board explicitly determines that it satisfies all objectives.

## Final synthesis

The final `.md` is generated from the board decision, not by averaging drafts.

It must satisfy:

- the document terminal reader state;
- all assigned section objectives and trajectory moves;
- implementation fidelity;
- the common instructional section contract where applicable:
  - why the object is needed;
  - what it represents;
  - when it is indicated;
  - how to invoke it;
  - what output it produces;
  - how to read the output;
  - what inference it may support;
  - what alternatives remain;
  - what it does not establish.

## Provenance

Independent drafts and board reports are retained under `project_state/editorial/<unit>/`. They are development provenance, not public instructional material.

Only the synthesized final document is part of the primary human-facing documentation surface.

A documentation unit is complete only after:
1. four independent drafts exist;
2. the board report exists;
3. implementation-facing claims are checked against current source;
4. the final document satisfies its section trajectory map;
5. canonical project state records the unit's completion.

## Incremental adjudication and adjudication state

Editorial adjudication is durable. A later mutation to a human-facing file does **not** automatically invalidate the entire document.

Every human-facing document or section should be classified at the smallest practical semantic unit as one of:

- **adjudicated_unchanged** — content previously passed through the full author/editor protocol and is unchanged in meaning and instructional function;
- **adjudicated_editorial_change** — wording, formatting, links, examples, or references changed without materially changing the proposition, API claim, instructional objective, evidential boundary, or reader task;
- **requires_re_adjudication** — new content or a mutation that changes meaning, implementation claims, scientific interpretation, instructional trajectory, scope, evidential boundary, or user action;
- **new_unadjudicated** — newly added human-facing content that has not yet gone through the protocol.

### Preservation rule

`adjudicated_unchanged` content is preserved verbatim unless a later dependency forces a semantic change.

`adjudicated_editorial_change` content may receive a lightweight editorial verification rather than four new author drafts, provided the change does not alter substantive meaning.

Only `requires_re_adjudication` and `new_unadjudicated` regions require the full antagonistic drafting cycle.

### Change-impact test

A mutation requires full re-adjudication when it changes one or more of:

- the document or section terminal reader state;
- a prerequisite or trajectory move;
- public API syntax, defaults, or behavior;
- a scientific or statistical claim;
- the interpretation of an observable;
- an inference boundary or alternative explanation;
- security, legal, compliance, or release guidance;
- a worked example whose output or meaning changes;
- the recommended user decision or action.

The following ordinarily do **not** require full re-adjudication:

- spelling, punctuation, or grammar corrections;
- link repairs;
- heading renames that preserve conceptual scope;
- relocation of already-adjudicated prose without semantic change;
- addition of navigation links;
- formatting-only code changes whose behavior is identical;
- replacing a placeholder image with the real image generated by the already-adjudicated example, provided caption/interpretation does not change.

### Incremental author/editor workflow

For a partially mutated document:

1. Compute or record the prior adjudicated document/section baseline.
2. Identify changed regions and classify each region by adjudication state.
3. Preserve `adjudicated_unchanged` regions.
4. Route only `requires_re_adjudication` and `new_unadjudicated` regions to the four independent authors.
5. Give authors the unchanged adjudicated context as read-only surrounding context so new prose integrates coherently.
6. The editorial board adjudicates the changed regions and may request local bridging edits to adjacent adjudicated text.
7. Reassemble the document from preserved adjudicated regions plus newly adjudicated regions.
8. Record a new document hash and a region-level adjudication ledger.

### Region-level provenance

Each human-facing artifact should maintain an adjudication ledger containing, where practical:

- file path;
- section heading or stable region ID;
- prior adjudication status;
- current adjudication status;
- reason for mutation;
- semantic impact classification;
- source author-draft/board-report references for newly adjudicated material;
- final content hash or section hash.

The purpose of the ledger is to avoid unnecessary rewriting while still making it clear which content has and has not received substantive review.

### Whole-document re-adjudication

Whole-document re-adjudication is reserved for cases where:

- the document objective changes substantially;
- section ordering or prerequisite structure changes enough that local preservation would create incoherence;
- a major API/architecture change invalidates many sections;
- the editorial board determines that local patches would produce a misleading or internally inconsistent artifact.

Whole-document rewriting is therefore an exception, not the default.

