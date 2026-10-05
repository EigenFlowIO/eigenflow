# Technical software developer and documentation writer draft — `docs/guides/vgg16_probe_experiment.md`

Prioritize exact implemented syntax, public interfaces, runnable examples, navigation, failure behavior, and consistency with source.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Question and hypothesis

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Suppose the question is: > Does a pretrained VGG16 representation become more organized by object class than by background as depth increases? Construct competing hypotheses. - \(H_1\): later sites become increasingly organized by class, relatively invariant to background. - \(H_2\): background remains a dominant organizing factor. The experiment must contain probe combinations that distinguish these hypotheses.

## Build a crossed probe population

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Assume you have images spanning two classes and two backgrounds: | class | background | |---|---| | wolf | snow | | wolf | grass | | husky | snow | | husky | grass | Use equal or at least well-documented counts where possible. If a factorial cell is absent in the original material, this helper cannot create it. The design is then confounded for the corresponding contrast.

## Load VGG16 reproducibly

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Apply the same preprocessing to every probe. Store or report: - weight/checkpoint identity; - preprocessing; - image source; - probe construction; - random seed used for sampling.

## Inspect representation sites

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: PyTorch exposes the module hierarchy. VGG16's `features` stack contains convolution, ReLU, and pooling modules. A useful first analysis often chooses endpoints of major convolutional stages rather than every individual ReLU. For example, inspect the actual model and choose explicit names: These names are examples for the canonical torchvision VGG16 layout. Verify them against `available_sites()` for the installed model. The choice of sites determines which computational stages are compared.

## Choose a representation reducer

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: A VGG convolutional activation has shape \[ N\times C\times H\times W. \]

## Flatten

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Flatten preserves all activation values but treats the spatially arranged tensor as one long vector.

## Global average pooling

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Global average pooling summarizes each channel over spatial positions. This can reduce dimensionality substantially and changes the measurement question. Neither reducer is universally correct. If the substantive conclusion depends strongly on reducer choice, report that dependence.

## Choose metric and filtration

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: For the first run, use cosine similarity and edge density. Why edge density? The graph begins sparse and progressively admits more pairwise relations. If you later compare cosine with Euclidean distance, matching edge density supplies a common graph-sparsity coordinate. Why cosine? It provides one reasonable angular relation for high-dimensional activation vectors. It is a measurement choice, not the ground-truth geometry of VGG16.

## Run complementary analyses

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: The same population is now analyzed at each selected VGG16 site.

## Navigate the result

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Inspect factor alignment at each site: Inspect class structure: Inspect percolation: Inspect spectral trajectories:

## Visualize layer × control behavior

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: The heatmap makes the two-dimensional object explicit: network site on one axis, relational scale on the other.

## Interpret the experiment

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Imagine the results show: - early sites: moderate background NMI and weak class NMI; - middle sites: both factors visible; - late sites: class NMI high over a broad density interval while background NMI falls; - late sites: within-class density exceeds external density over the same interval; - late sites: a stable low-dimensional spectral regime appears; - bridge analysis identifies a few visually ambiguous probes connecting the final groups. A disciplined conclusion is: **Observation.** Multiple structural observables become more class-aligned and less background-aligned across depth. **Candidate inference.** Within this factorial probe population, later VGG16 representations provide stron

## Stress-test the interpretation

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Repeat the experiment with an alternative reducer: Repeat with Euclidean distance at the same edge-density grid: If the main conclusion persists, the evidence is less dependent on one geometry. If it changes, that difference is itself informative. Report the dependence rather than selecting only the favorable configuration.

## Device and batching

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: Pass a device explicitly if needed: The extractor temporarily switches the model to evaluation mode, runs under `torch.no_grad()`, and restores the model's previous training state after extraction. Large probe populations and full spectra can be expensive. Reduce the number of sites, use pooling, reduce filtration steps, or configure partial spectral analysis for exploratory work.

## Save the result

Draft move: state the implemented object or action precisely, then show valid syntax or an exact result path. Source-grounded content to preserve: The current implementation serializes a JSON representation to `result.json`. Eigenvectors are omitted from the serialized representation. Record the complete experimental specification alongside any reported conclusion: probe construction, checkpoint, preprocessing, sites, reducer, metric, filtration, analyses, and robustness checks.
