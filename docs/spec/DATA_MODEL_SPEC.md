# Eigenflow v1 Data Model

The canonical in-package path is:

`ProbePopulation -> RepresentationCollection -> RelationalMatrix -> GraphFiltration -> AnalysisResult -> ExperimentResult`.

Every stage preserves probe ordering and probe IDs. Filtration snapshots contain the parameter value, edge density, sparse adjacency matrix, and optional native threshold. Analysis results contain named numerical observables and structured records. Provenance records configuration, package/runtime versions, model class, capture sites, reducers, metric orientation, filtration configuration, and random seed where relevant.

Large numerical payloads are not required to be embedded in JSON. `ExperimentResult.save()` writes JSON metadata and NPZ arrays to a directory; `load()` reconstructs the portable result representation.
