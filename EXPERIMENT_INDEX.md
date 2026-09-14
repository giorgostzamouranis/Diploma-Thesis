# Experiment Index

This index separates **completed canonical experiments**, **resume chains**, and **non-canonical historical artifacts**.

## Phase 0–B4: reproduction, diagnosis, and falsification studies

The June progress reports in `docs/` record the complete Phase 0–B4 measurements:
- faithful full-set reproduction,
- metric-driven diagnosis,
- controllability sweep (`start_step`, `start_layer`, prompt CFG),
- AA-Warp / Adaptive-ES,
- IP-Adapter identity conditioning,
- geometry-aligned TCA/KV interventions,
- refinement preservation.

The executable notebooks currently available from the thesis workspace that belong to the later/expanded pathway studies are in `notebooks/01_discovery_and_pathway_studies/`.

## 01 — Discovery and pathway studies

- `approach-1-ip-controlnet.ipynb`: IP identity + masked Canny ControlNet branch.
- `ip-pathway-study.ipynb`: IP pathway variants, including warped crop and HOG-IP.
- `guidance-discovery.ipynb`: APG/EPSREC/FDG guidance discovery.
- `combined-model-geometric-edit.ipynb`: early combined router/compositing model.
- `combined-model-geometric-held-out-200.ipynb`: held-out-200 validation of the early combined model.

## 02 — Structural, spectral, preservation, and guidance search

- `freefine-final-exhaustive-run-account-a-structu.ipynb`: structural/spectral search.
- `01-w0a-complete-mid30-and-pure-structural-t4x2-v1.ipynb` + `01-w0a-resume-only-missing-dirhf-t4x2-v2.ipynb`: one resumable execution chain.
- `02-w0b-complete-pres03-and-guidance-gaps-t4x2-v1.ipynb`: preservation/guidance gap completion.

## 03 — Exhaustive core metrics

- `wave-1a-structural.ipynb` is a partial run completed by `wave-1a-core-resume-v2.ipynb`.
- `wave-1b-guidance-combo-post.ipynb` is a partial run completed by the three `w1b-core-resume-shard*` notebooks.

## 04 — Exhaustive FID/FDD/KD metrics

The `w2a`–`w2d` notebooks evaluate structural and guidance/post families, globally and by difficulty, using resumable T4×2 shards.

## 05 — Final router selection

- `freefine-final-geometry-step0-geobench-audit-no-gp (1).ipynb` is the **corrected v2 exact-affine audit**.
- `freefine-final-geometry-step1-deployable-router-pr(1).ipynb` is the balanced-200 deployable-router preflight.

The superseded v1 audit is kept only under `archive/noncanonical/` and must not be used.

## 06 — Final full 5,677 generation

Four generation shards produce:
- fresh FreeFine baseline,
- `SGR_EPSREC`,
- `SGR_MIDHF_EPSREC`.

## 07 — Final full 5,677 metrics

The first three metric notebooks produced the main/global and some subgroup measurements. The combined resume notebook completed the missing exact-affine subgroup metrics except the final rotate job, and the canonical final fork completed that last job.

**Canonical final metrics:** `results/final_full5677_metrics.{json,csv}`

## Final recommended method

`SGR_EPSREC`:
- Move → RING4
- Rotate → original FreeFine
- Resize, non-severe (`0.6 < s < 1.5`) → RING8
- Resize, severe (`s <= 0.6` or `s >= 1.5`) → object prompt + CFG10 + EPSREC

with `s = sqrt(sx * sy)` from the exact requested affine transform.
