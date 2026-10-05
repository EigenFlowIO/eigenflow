# Eigenflow v1 Execution and Caching

Experiment execution is a dependency DAG. Activation extraction is performed once per model/probe/extraction configuration. A metric matrix is computed once per representation site and metric configuration. A filtration is constructed once per relational matrix and filtration configuration. Analyses consume shared graph snapshots/operators.

The initial v1 cache is an in-memory content-addressed cache keyed by stable configuration representations and upstream object identities. Public interfaces do not depend on the cache implementation, permitting later disk or distributed caches.

Invalidation is directional: changing probe inputs invalidates all descendants; changing a metric leaves extracted representations valid; changing only an analysis leaves extraction, metric matrices, and filtrations valid.
