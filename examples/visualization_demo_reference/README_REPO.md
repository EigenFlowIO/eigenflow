# Reference outputs for the complete visualization demo

These files are a checked-in reference run of `examples/complete_visualization_demo.py`.

The 22 generated PNG figures are stored once under `docs/assets/visualization_demo/` so documentation can render them without duplicating binary files. The full script-generated archive includes those figures and is created as `eigenflow_visualization_demo_outputs.zip`.

The numerical tables, native JSON result, trained model state, exact generator, environment/configuration metadata, and machine-readable visualization catalog are retained here so documentation statements can be audited against concrete output.

These reference files are evidence for the documented demonstration, not a guarantee of pixel-identical rendering across Matplotlib/platform versions. Regression tests target callable behavior and required data/annotations rather than brittle image-byte equality.
