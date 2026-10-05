# VGG16 probe experiment

With torchvision VGG16, provide preprocessed image tensors as a `ProbePopulation`. Use `PyTorchExtractor.available_sites()` to inspect names and choose block endpoints, or use the default leaf-module capture policy. For convolutional outputs, `flatten` reproduces PCSCS-style behavior; `global_average` gives channel-level vectors. Downstream metric and filtration analysis is independent of VGG16.
