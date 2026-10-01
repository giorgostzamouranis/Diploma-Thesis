# Experiment Index

This index maps the full experimental history of the thesis from the first FreeFine reproduction through the final SGR-EPSREC evaluation. It separates canonical completed experiments, resumable execution chains, superseded historical artifacts, and account-recovery notes.

## 00 — Reproduction, diagnosis, and June falsification studies

These are the executed historical notebooks behind the June 2026 progress presentation and metrics appendix. They were recovered from Kaggle Accounts A/B and are now preserved as genuine execution artifacts.

- `benchmark-reproduction.ipynb` — Phase 0 full 5,677-edit FreeFine reproduction. Generates the complete GeoBench-2D population and records the main baseline measurements.
- `phase0-md-fid-dino-fid-kd.ipynb` — Phase 0 supplemental FID_DINO / FID_KD / sharded-MD evaluation.
- `phase1-per-group-fid-dino-kd-bgc-subc-we.ipynb` — Phase 1 diagnosis by edit type and difficulty.
- `phase1-full-md-per-sample-dump.ipynb` — full per-keypoint MD dump; one stochastic full run gives pooled MD 8.499344.
- `phase1-rerun-md.ipynb` — corrected per-path grouping and a second stochastic full MD run (8.545517), documenting the observed MD noise floor.
- `freefine-phase2run-corrected.ipynb` — Phase 2/2b controllability sweep: `ss25/30/40/45`, `l4/8/12`, `p7.5/p10`.
- `experiments-phase.ipynb` — B1 AA-Warp / Adaptive-ES: `aaw`, `es25`, `es50`, `esA`, `aaw_esA`.
- `experiments-phase-b2.ipynb` — B2 IP-Adapter sweep: `ip50`, `ip80`, `ip110`, `ip140`.
- `experiments-phase-b3.ipynb` — B3 geometry-aligned TCA/KV study: correspondence bias, warped K/V, validity gating, and R²-TCA.
- `experiments-phase-b4.ipynb` — B4 refinement-preservation sweep: `pres_w03/05/07/09`.

The uncorrected `freefine-phase2run.ipynb` is retained only under `archive/noncanonical/`.

## 01 — Discovery and pathway studies

- `approach-1-ip-controlnet.ipynb` — IP identity + masked Canny ControlNet branch.
- `ip-pathway-study.ipynb` — IP pathway variants, including warped crop and HOG-IP.
- `guidance-discovery.ipynb` — APG/EPSREC/FDG guidance discovery.
- `m-hff-feature-discovery.ipynb` — M-HFF feature/frequency discovery on Account A.
- `freefine-account-b2-v3-apg-parameterization-m.ipynb` — APG parameterization and momentum-matching study on Account B.
- `combined-model-geometric-edit.ipynb` — early combined router/compositing model.
- `combined-model-geometric-held-out-200.ipynb` — held-out-200 validation of the early combined model.

## 02 — Structural, spectral, preservation, and guidance search

- `freefine-final-exhaustive-run-account-a-structu.ipynb` — final Account-A structural/spectral exhaustive run.
- `freefine-final-exhaustive-run-account-b-guidan.ipynb` — final Account-B guidance/move/combinations run. This is the predecessor whose partial `PRES03_GLOBAL=179/200` output is resumed by Wave 0B.
- `01-w0a-complete-mid30-and-pure-structural-t4x2-v1.ipynb` + `01-w0a-resume-only-missing-dirhf-t4x2-v2.ipynb` — resumable Wave-0A chain.
- `02-w0b-complete-pres03-and-guidance-gaps-t4x2-v1.ipynb` — completes the Account-B predecessor and the remaining pure-guidance/combo ablations.

## 03 — Exhaustive core metrics

- `wave-1a-structural.ipynb` is a partial run completed by `wave-1a-core-resume-v2.ipynb`.
- `wave-1b-guidance-combo-post.ipynb` is a partial run completed by the three `w1b-core-resume-shard*` notebooks.

The Account-C export contains only a 0-byte placeholder named `wave-1b-three-shard-merge-v3.xpynb`; therefore no merge notebook is committed as if it were recoverable.

## 04 — Exhaustive FID/FDD/KD metrics

The `w2a`–`w2d` notebooks evaluate structural and guidance/post families, globally and by difficulty, using resumable T4×2 shards.

The four expected merge notebooks (`w2a/w2b/w2c/w2d-merge-no-gpu-v3`) were present in the four-account exports only as 0-byte `.xpynb` placeholders. Their executable code is therefore not reconstructed. Their produced result tables are preserved in:

- `results/A_fid_main_results.json`
- `results/A_fid_difficulty_results.json`
- `results/B_fid_main_results.json`
- `results/B_fid_difficulty_results.json`

## 05 — Final router selection

- `freefine-final-geometry-step0-geobench-audit-no-gp (1).ipynb` — corrected v2 exact-affine audit.
- `freefine-final-geometry-step1-deployable-router-pr(1).ipynb` — balanced-200 deployable-router preflight.

The superseded v1 audit is kept only under `archive/noncanonical/`.

## 06 — Final full 5,677 generation

Four generation shards produce:

- fresh FreeFine baseline,
- `SGR_EPSREC`,
- `SGR_MIDHF_EPSREC`.

All four shards are preserved and were recovered across Kaggle Accounts A–D.

## 07 — Final full 5,677 metrics

The first three metric notebooks produced the main/global and some subgroup measurements. The combined resume notebook completed the missing exact-affine subgroup metrics except the final rotate job, and the canonical final fork completed that last job.

**Canonical final metrics:** `results/final_full5677_metrics.{json,csv}`

## 08 — Final qualitative comparison

`freefine-final-geometry-qualitative-comparison-no-output-pruned.ipynb` is a repository-sized archival copy of the executed no-GPU qualitative comparison notebook. Code, execution metadata, and textual outputs are retained; embedded image display payloads were removed. The SHA256 of the original 34.8 MB executed Kaggle notebook is recorded inside the notebook and in the account-recovery audit.

## 09 — Post-hoc validation runs

Two studies were run after the final evaluation, while the thesis was being written. Their outputs are in `results/post_hoc/`.

- `geometry-attention-corrected-sharda.ipynb` + `geometry-attention-corrected-shardb.ipynb` — corrected re-run of the B3
  geometry-aware attention study on balanced-200. Shard A: per-branch head-layout control `c0`, correspondence bias G2
  (`c0_g2_l4`, `c0_g2_l8`). Shard B: warped K/V G1 (`c0_g1`), G1 + validity gating G3 (`c0_g1_g3`), pixel-warped reference R²
  (`c0_r2`). Results: `gafix_results_A.{json,csv}`, `gafix_results_B.{json,csv}`. Every corrected mechanism still lowers
  hard-group SUBC relative to `c0`. This corrected study is the one reported in the thesis (Experiment 11).
- `percase_metrics_full5677.ipynb` — re-scores the final full-5,677 images (nothing is regenerated) with the official metric code,
  patched only to record the per-image SUBC, BGC and WRAP_E of FreeFine and SGR-EPSREC, and of SGR-MIDHF-EPSREC on the 759 severe
  resizes. Built-in checks: per-image means equal the official group values; group means reproduce
  `results/final_full5677_metrics.csv` to four decimals; rotations are byte-identical. Outputs: `percase_metrics_full5677.csv`
  (one row per edit), `paired_stats.csv` (bootstrap 95% intervals, Wilcoxon signed-rank tests and win/tie/loss counts per group)
  and `percase_validation_report.json`. The repository copy is the executed notebook with its outputs; all four checks pass.

## Four-account recovery audit

Accounts A, B, C, and D were audited together. The raw ZIP exports contained 72 entries: 50 non-empty `.ipynb` files and 22 zero-byte `.xpynb` placeholders. Two non-empty entries were exact duplicates, leaving 48 unique notebooks in the four ZIPs. The separately recovered Phase-0 `benchmark-reproduction.ipynb` adds one additional unique historical artifact.

See:

- `metadata/ACCOUNT_RECOVERY_AUDIT.md`
- `metadata/account_recovery_audit.csv`
- `metadata/notebook_status.csv`

Zero-byte placeholders are documented but are not committed as fake notebooks.

## Final recommended method

`SGR_EPSREC`:

- Move → RING4
- Rotate → original FreeFine
- Resize, non-severe (`0.6 < s < 1.5`) → RING8
- Resize, severe (`s <= 0.6` or `s >= 1.5`) → object prompt + CFG10 + EPSREC

with `s = sqrt(sx * sy)` from the exact requested affine transform.
