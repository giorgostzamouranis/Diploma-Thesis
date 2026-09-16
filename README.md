# FreeFine-SGR: Diploma Thesis Experiments

This repository is the reproducibility archive for a diploma thesis on **training-free 2D geometric image editing**, built on top of FreeFine.

The work follows a full research cycle:

1. reproduce the original FreeFine baseline,
2. diagnose failure modes on GeoBench-2D,
3. test multiple alternative hypotheses,
4. develop a selective transform-aware refinement strategy,
5. validate the final method on the complete **5,677-edit** GeoBench-2D population.

A September 2026 recovery audit across all four Kaggle accounts restored the executed notebooks behind the early reproduction/diagnosis/ablation phases as well as several missing later lineage notebooks. See `metadata/ACCOUNT_RECOVERY_AUDIT.md`.

## Final method: SGR-EPSREC

The final method is **not a newly trained network**. It is a training-free inference policy on top of the frozen FreeFine / Stable Diffusion 1.5 pipeline.

| Edit | Final branch |
|---|---|
| Move | FreeFine + **RING4** post-preservation |
| Rotate | **Original FreeFine** fallback |
| Resize, non-severe | FreeFine + **RING8** post-preservation |
| Resize, severe | object prompt + **CFG 10 + EPSREC** |

For resize, the deployable router uses only the requested affine scale:

`scale = sqrt(sx * sy)`

Severe resize is defined as `scale >= 1.5` or `scale <= 0.6`. Benchmark difficulty labels are **not** used at inference.

## Final full-set results

All arrows indicate the desired direction.

| Metric | FreeFine baseline | SGR-EPSREC |
|---|---:|---:|
| SUBC ↑ | 0.9113 | **0.9144** |
| BGC ↑ | 0.9670 | **0.9671** |
| WRAP_E ↓ | 0.0474 | **0.0292** |
| MD ↓ | 8.5024 | **8.1779** |
| FID ↓ | 35.0439 | **34.7793** |
| FID_DINO ↓ | 487.8231 | **487.3580** |
| FID_KD ↓ | 0.1433 | **0.1417** |

Thus, on the complete 5,677-edit population, SGR-EPSREC numerically improves the reproduced baseline on **7/7 aggregate metrics**. The largest aggregate changes are approximately **−38.4% WRAP_E** and **−3.82% MD**.

`SGR_MIDHF_EPSREC` is retained as an ablation. It is almost identical globally, but the simpler SGR-EPSREC has a clearer severe-resize advantage in MD and is the recommended final method.

## Repository layout

- `notebooks/00_reproduction_diagnosis_and_june_ablation/` — recovered executed Phase 0–B4 notebooks behind the June progress report
- `notebooks/01_discovery_and_pathway_studies/` — later identity, feature/frequency, and guidance discovery
- `notebooks/02_structural_spectral_and_guidance_search/` — exhaustive generation/search packs and resume chains
- `notebooks/03_exhaustive_core_metrics/` — SUBC/BGC/WRAP_E/MD evaluation
- `notebooks/04_exhaustive_fid_metrics/` — FID/FDD/KD evaluation shards
- `notebooks/05_final_router_selection/` — exact-affine audit and deployable-router preflight
- `notebooks/06_final_full5677_generation/` — fresh final four-shard generation
- `notebooks/07_final_full5677_metrics/` — final complete metric chain
- `notebooks/08_final_qualitative/` — final qualitative comparison code (image payloads pruned from the repository copy)
- `results/` — structured result JSON/CSV files and final tables
- `metadata/` — source pins, execution status, hashes, and the four-account recovery audit
- `docs/` — thesis progress reports, metrics appendix, and presentation
- `archive/noncanonical/` — superseded, exploratory, or duplicate historical artifacts
- `archive/utilities/` — utility notebooks that are not experiment results
- `EXPERIMENT_INDEX.md` — chronological map of the experimental program
- `REPRODUCIBILITY.md` — final run order and data/environment requirements

## Reproducibility pins

- FreeFine commit: `4c9fdb971572b32edbeac13464659274c28decbb`
- GeoBench-2D frozen manifest SHA256:
  `17d971102daca232921d33de91adac58ef0ddbea9c9f814e219148486c9de802`
- Population: 5,677 = 1,439 move + 1,603 rotate + 2,635 resize

## Important execution-history notes

Several long Kaggle jobs were intentionally resumable. Some notebooks therefore stop partially and are completed by later resume notebooks. The status and lineage are recorded in `metadata/notebook_status.csv` and `EXPERIMENT_INDEX.md`.

The four-account recovery also found a small number of 0-byte Kaggle `.xpynb` placeholders, including the historical W2 merge notebooks. These are documented in `metadata/account_recovery_audit.csv` but are **not reconstructed**.

The original incorrect v1 affine-severity audit is retained only under `archive/noncanonical/`; the corrected exact-affine v2 audit is the one used for the final method.

## Data and model weights

Large datasets, generated image populations, and model checkpoints are intentionally not committed to this repository. The notebooks document the required Kaggle inputs and reconstruct the workflow from pinned external sources.

## Upstream attribution

This work builds on FreeFine:

- Upstream repository: https://github.com/CIawevy/FreeFine
- Paper: *Training-Free Geometric Image Editing on Diffusion Models*, ICCV 2025
- Upstream license: Apache-2.0

See `references/README.md`.

## Thesis author

Giorgos Tzamouranis
