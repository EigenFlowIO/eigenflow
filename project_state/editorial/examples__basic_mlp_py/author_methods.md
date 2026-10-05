# Research methods author writing training materials for research practitioners draft — `examples/basic_mlp.py`

Prioritize prerequisite order, experimental decisions, examples, transfer tasks, confounds, and explicit guidance for designing a defensible study.

This draft is intentionally role-specific. It covers the complete unit structure but weights the material according to the author's disciplinary responsibility.

## Executable unit

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: """Basic Eigenflow experiment. The example is deliberately small. It demonstrates the complete population-level pipeline and prints outputs that can be interpreted without treating Eigenflow as a black box. """ torch.manual_seed(7)

## it is the relational organization of the probe population at its internal sites.

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: model = torch.nn.Sequential( torch.nn.Linear(4, 8), torch.nn.ReLU(), torch.nn.Linear(8, 2), )

## deliberately manipulated/controlled factors rather than arbitrary labels.

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: inputs = [] metadata = [] for i in range(16): inputs.append(torch.randn(4) * 0.35 + torch.tensor([1.0, 0.0, 0.0, 0.0])) metadata.append({"class": "A"}) for i in range(16): inputs.append(torch.randn(4) * 0.35 + torch.tensor([-1.0, 0.0, 0.0, 0.0])) metadata.append({"class": "B"}) probes = ef.ProbePopulation.from_items( inputs, metadata=metadata, name="two_group_demo", ) print("Available PyTorch capture sites:") print(ef.PyTorchExtractor(model).available_sites()) experiment = ef.Experiment( model=m

## Interpretation discipline:

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: #

## actually changed.

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: #

## Connect that pattern to the controlled feature hypothesis.

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: #

## Consider metric/reducer/probe dependence.

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: #

## mechanism.

Draft move: connect this section to a practitioner decision, prerequisite, or transfer task. Use a concrete research choice or worked contrast. Instructional content to preserve: #
