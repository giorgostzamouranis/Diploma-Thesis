# Reproducibility

## Fixed benchmark and source

- GeoBench-2D population: **5,677** edits
  - move: 1,439
  - rotate: 1,603
  - resize: 2,635
- Frozen exact-affine manifest SHA256:
  `17d971102daca232921d33de91adac58ef0ddbea9c9f814e219148486c9de802`
- Original FreeFine source commit:
  `4c9fdb971572b32edbeac13464659274c28decbb`

## Compute

The thesis runs were performed primarily on Kaggle using **2 × NVIDIA T4** GPUs. The notebooks are intentionally sharded and resumable because Kaggle sessions have a wall-time limit.

## Environments

Two separate environments were used in the experimental workflow:

- Generation: PyTorch 2.1.1 / Diffusers 0.18.x family, matching the pinned FreeFine workflow.
- Metrics: PyTorch 2.6.x for the final evaluation notebooks.

The exact installation cells are preserved inside each executed notebook.

## Required Kaggle inputs for the final full-5,677 run

The final generation notebooks expect datasets equivalent to:

- `freefine-sample-metadata`
- `geobench2d-coarse-img`
- `geobench2d-metrics-subset`
- `freefine-geobench2d-bggen`

The final metric notebooks require the four completed generation-shard outputs plus the first three metric/data inputs above.

## Final execution order

1. `notebooks/05_final_router_selection/freefine-final-geometry-step0-geobench-audit-no-gp (1).ipynb`
2. `notebooks/05_final_router_selection/freefine-final-geometry-step1-deployable-router-pr(1).ipynb`
3. Run all four notebooks in `notebooks/06_final_full5677_generation/`.
4. Use the metric notebooks in `notebooks/07_final_full5677_metrics/`.
5. The canonical completed metric run is `fork-of-09-combined-metric-resume-accounta-t4x2-v2.ipynb`.

Several earlier notebooks intentionally stop and are later resumed. See `metadata/notebook_status.csv` and `EXPERIMENT_INDEX.md`.
