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
