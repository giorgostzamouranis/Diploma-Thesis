# Reproducibility

## Fixed benchmark and source

- GeoBench-2D population: **5,677** edits
  - move: 1,439
  - rotate: 1,603
  - resize: 2,635
- Frozen exact-affine manifest SHA256:
  `17d971102daca232921d33de91adac58ef0ddbea9c9f814e219148486c9de802`
- Original FreeFine source commit used by the final pipeline:
  `4c9fdb971572b32edbeac13464659274c28decbb`

## Compute

The thesis runs were performed primarily on Kaggle using **2 × NVIDIA T4** GPUs across four Kaggle accounts. The notebooks are intentionally sharded and resumable because Kaggle sessions have a wall-time limit.

A recovery audit of Accounts A–D is recorded in `metadata/ACCOUNT_RECOVERY_AUDIT.md`.

## Environments

Two separate environments were used in the later/final experimental workflow:

- Generation: PyTorch 2.1.1 / Diffusers 0.18.x family, matching the pinned FreeFine workflow.
- Metrics: PyTorch 2.6.x for the final evaluation notebooks.

The exact installation cells are preserved inside each executed notebook. Earlier June notebooks may reflect the environment state at the time of those historical runs; they are retained as execution artifacts rather than rewritten to match the later final environment.

## Historical reproduction and ablation chain

The executed notebooks behind the June Phase 0–B4 results are preserved in:

`notebooks/00_reproduction_diagnosis_and_june_ablation/`

They include the full baseline reproduction, per-group diagnosis, controllability sweep, AA-Warp/Adaptive-ES, IP-Adapter, geometry-aware TCA/KV, and refinement-preservation experiments.

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

## Known archival gaps

The four Kaggle account ZIP exports contained only zero-byte placeholders for the historical W2A/W2B/W2C/W2D no-GPU merge notebooks and the Wave-1B three-shard merge notebook. These files are not reconstructed. The W2 merged result JSON files are preserved under `results/`.

The executed final qualitative notebook is preserved in repository-sized form with embedded image payloads removed; its original SHA256 is documented in the notebook and recovery audit.

See `metadata/notebook_status.csv`, `metadata/account_recovery_audit.csv`, and `EXPERIMENT_INDEX.md` for the complete execution/provenance map.
