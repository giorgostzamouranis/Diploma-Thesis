# Kaggle Account Recovery Audit

This file records the September 2026 recovery pass over the four Kaggle accounts used during the thesis.

## Inventory

| Account | ZIP entries | Non-empty `.ipynb` | Zero-byte `.xpynb` |
|---|---:|---:|---:|
| A | 36 | 20 | 16 |
| B | 21 | 18 | 3 |
| C | 8 | 6 | 2 |
| D | 7 | 6 | 1 |

Across A–D there are **72 exported entries**, of which **50 are non-empty `.ipynb` files** and **22 are 0-byte `.xpynb` placeholders**. Two non-empty occurrences are byte-identical duplicates (`freefine-phase2run.ipynb` across A/B and the duplicated W2D shard-4 export inside A), leaving **48 unique notebooks in the account ZIPs**.

A separately recovered executed `benchmark-reproduction.ipynb` is also included in the repository because the Account-A ZIP itself contains only a 0-byte placeholder with that name.

## Recovered gaps

The four-account audit recovered genuine executed artifacts for the historical June phases that were previously represented only by reports:

- Phase 0 reproduction and supplemental metrics,
- Phase 1 per-group diagnosis and MD runs,
- Phase 2/2b controllability sweep,
- B1 AA-Warp / Adaptive-ES,
- B2 IP-Adapter,
- B3 geometry-aligned TCA/KV,
- B4 refinement preservation.

It also recovered later missing lineage artifacts:

- `m-hff-feature-discovery.ipynb`,
- `freefine-account-b2-v3-apg-parameterization-m.ipynb`,
- `freefine-final-exhaustive-run-account-b-guidan.ipynb`.

The last of these is the genuine predecessor to `02-w0b-complete-pres03-and-guidance-gaps-t4x2-v1.ipynb`: its execution ends with `PRES03_GLOBAL=179/200`, which Wave 0B imports and completes.

## Unrecoverable placeholders

The account ZIPs contain only zero-byte placeholders for several notebooks. These are intentionally **not reconstructed**:

- `w2a-merge-no-gpu-v3.xpynb`
- `w2b-merge-no-gpu-v3.xpynb`
- `w2c-merge-no-gpu-v3.xpynb`
- `w2d-merge-no-gpu-v3.xpynb`
- `wave-1b-three-shard-merge-v3.xpynb`

The W2 merge outputs themselves are preserved in `results/*.json`, so the numerical results are not lost; only those merge-code artifacts were absent from the exports.

Other zero-byte placeholders are listed verbatim in `account_recovery_audit.csv`.

## Qualitative notebook

The executed final qualitative notebook from Account A is 34.8 MB because it embeds image display payloads. The repository stores an **output-pruned archival copy** that retains code, execution metadata, and textual outputs. The original executed notebook SHA256 is:

`f8d3864da15528275bd834bce3ce8fe8ac055900a2309f33f1947fc8b0d8bf15`

No claim is made that the pruned copy is byte-identical to the original; its provenance is explicit.

## Policy used for repository restructuring

1. Genuine executed artifacts are preferred over later reconstructions.
2. Exact duplicates are stored only once.
3. Superseded but scientifically relevant predecessors are retained under `archive/noncanonical/`.
4. Utility notebooks are kept separately from experiment notebooks.
5. Zero-byte placeholders are documented, not promoted to fake executable artifacts.
6. The final SGR-EPSREC run remains the canonical final result even when historical development notebooks are preserved.
