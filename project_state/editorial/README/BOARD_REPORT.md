# Editorial board report — README.md

## Board roles

- Software codebase team lead
- Compliance and liability counselor
- Clarity and communication editor

## Adjudication

### 1. Software codebase team lead

Draft A is the strongest source for concrete API syntax and result navigation. Drafts B–D correctly frame the method but occasionally speak at a level more abstract than a first-contact README should sustain.

Required constraints for the final README:

- Only advertise APIs that exist in the current repository.
- Do not imply `ExperimentResult.load()` exists.
- Do not imply caching, a user-configurable operator list on `Experiment`, or a full automatic model-semantic layer selector exists.
- State accurately that default extraction captures leaf `nn.Module` tensor outputs and uses the configured reducer, currently `flatten` by default.
- Keep `result.layers[site].analyses[...]` examples explicit because this is the first place users learn the result hierarchy.
- Explain that analysis keywords instantiate default configurations; advanced customized analysis objects belong in API/reference material.
- Installation should be from the repository at this stage, not PyPI.

### 2. Compliance and liability counselor

Drafts B–D best protect the method from overclaiming. The final document must make the following boundaries prominent rather than burying them at the end:

- structural correlation is not causal attribution;
- factor alignment does not prove unique semantic encoding;
- a poorly identified probe design cannot be repaired by sophisticated analysis;
- metric/reducer/filtration choices define the measurement and may affect conclusions;
- percolation-style transition statistics are descriptive unless stronger criticality evidence is supplied;
- use of untrusted PyTorch model artifacts has security implications, which should be delegated to SECURITY.md rather than expanded in the README.

Avoid language such as "reveals what the network learned" without qualification. Prefer "provides evidence about how the probe population is organized under the chosen measurement."

### 3. Clarity and communication editor

Draft C provides the best instructional sequence for a first-time reader. Draft A supplies necessary syntax. Draft B provides the cleanest formal statement of the inverse problem. Draft D provides the clearest explanation that the measurement configuration conditions the conclusion.

The final README should:

1. open with the interpretability question before the software architecture;
2. define the probe population early;
3. establish the population-level object before formulas;
4. give a single minimal runnable example;
5. immediately show how to inspect the result;
6. explain the meaning of the major configuration choices;
7. include one concrete four-stage interpretation example;
8. end with task-oriented documentation routing.

Avoid exhaustive catalogs in the first half. Detailed lists can be compactly retained after the reader understands the model.

## Synthesis decision

The final README will use Draft C's pedagogical progression, Draft B's inverse-problem framing, Draft D's measurement-design and robustness language, and Draft A's API syntax/result access.

The README's terminal reader state is: a first-time analyst can decide whether Eigenflow is indicated, understand the experimental object, run a minimal study, retrieve outputs, and make a bounded first interpretation while knowing what documentation is required next.

No draft is accepted wholesale.
