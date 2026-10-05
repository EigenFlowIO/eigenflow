# Eigenflow Human-Facing Instructional Architecture

## Purpose

The human-facing surface is designed as an inverse problem. We begin with the reader state that would justify successful use of Eigenflow in a neural-network feature-interpretation experiment, then solve backward for the beliefs, distinctions, procedural skills, examples, and evidential judgments a first-encounter reader must acquire.

Documentation is therefore not organized merely as topical coverage. Each section must perform a defined transformation in an epistemological-semantic graph.

## Initial reader state

The intended entry reader is a technically competent neural-network analyst or systems architect who understands ordinary neural-network computation, tensors, layers/modules, model evaluation, and Python tooling, but is not assumed to know Eigenflow, PCSCS, graph filtrations, percolation observables, spectral graph analysis, controlled probe design, or the inferential limits of structural representation analysis.

## Objective reader state

The objective is justified experimental competence. The reader should be able to decide whether an interpretability question is suitable for Eigenflow, design a probe population that bears on explicit competing hypotheses, choose representation/metric/filtration settings for defensible reasons, execute the package, understand the structural observables, interpret them within their intrinsic scope, test alternative explanations and robustness, and produce a human-interpretable account of what the experiment supports about internal neural-network representation.

The intended epistemic chain is:

```text
interpretability question
    ↓
competing latent-feature hypotheses
    ↓
controlled probe population
    ↓
layerwise population representations
    ↓
chosen relational geometry
    ↓
control-parameter filtration
    ↓
structural observables
    ↓
convergent / divergent evidence
    ↓
robustness and alternative explanations
    ↓
bounded human interpretation
```

## Epistemic dependency trajectory

1. **Orientation and indication.** The reader first learns what problem Eigenflow addresses, what it measures, and when the method is or is not indicated.
2. **Population representation model.** Intermediate activations are reframed as representations of an entire probe population, and relational organization—not a single activation trace—is established as the primary object.
3. **Probe design as experimental design.** The reader learns to manipulate semantic factors, construct controls, and formulate contrasts whose predicted structural outcomes differ under competing hypotheses.
4. **Measurement geometry.** Reducers, metrics, and filtrations are introduced as choices that define what relational structure is observable and therefore constrain interpretation.
5. **Multiscale structure.** The control sweep is established before individual statistics; component, percolation, spectral, eigenspace, factor, bridge, core, community, and transition outputs are then introduced as answers to different structural questions.
6. **Execution and result navigation.** Only after the experiment has semantic meaning does the full API become the procedural realization of that design.
7. **Interpretation and triangulation.** Observations are converted into candidate feature interpretations, explicitly separated from alternative explanations and unsupported claims. Cross-metric, reducer, filtration, sample-size, and probe-manipulation comparisons are taught as robustness evidence.
8. **Full demonstrations.** Worked experiments begin with a hypothesis and conclude with a bounded evidence statement, modeling the complete reasoning pattern expected of users.

## Representation tasks

The documentation must enable a reader to demonstrate competence, not merely recognize terminology. Required representation tasks include:

- design a controlled probe experiment that discriminates between competing feature hypotheses;
- justify metric/reducer/filtration choices and state their interpretive assumptions;
- execute an end-to-end Eigenflow experiment and retrieve the relevant outputs;
- interpret component, percolation, spectral, and factor outputs jointly;
- propose alternative explanations and design robustness checks;
- write a concise experimental interpretation that separates observation, inference, uncertainty, and overclaim.

## Backstepping rules

Content is developed backward from the final interpretation task. A reader cannot be asked to interpret an observable before understanding the control-parameter family to which it belongs. The control-parameter family cannot be meaningful before the relational metric and representation reduction are understood. Those choices cannot be justified before the reader understands the probe population and hypothesis. The probe cannot function as an experiment before the reader understands that the unit of analysis is population-level relational organization across network depth.

Thus syntax is never the first explanation of a scientific object. Syntax follows semantic role and experimental indication.

## Interpretation discipline

Every substantial output discussion must contain four distinct elements:

1. **Observation:** what the computation directly reports.
2. **Candidate inference:** what that pattern may indicate about internal representation under the probe design.
3. **Alternative explanations:** other mechanisms, metric choices, sampling effects, or confounds compatible with the observation.
4. **Unsupported claim:** what the result does not establish.

Convergent observables and robustness across legitimate alternative measurement choices can strengthen a conclusion; they do not convert a structural correlation into an automatically causal or uniquely identified latent feature.

## Documentation acceptance criterion

The human-facing surface is complete only when a first-time technically competent reader can complete the representation tasks above using the documentation and actual public API, and can produce an interpretation whose claims are calibrated to the experiment's design and the intrinsic scope of the measurements.
