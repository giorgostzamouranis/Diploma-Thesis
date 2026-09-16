FreeFine — Master Progress Report

Reproduction, Metric-Driven Diagnosis, and a Systematic Architectural Study on GeoBench-2D

Diploma Thesis · Giorgos Tzamouranis · 20 June 2026

Abstract. We faithfully reproduce FreeFine (training-free geometric image editing, ICCV 2025) on GeoBench-2D, then localize its weakness through a metric-driven diagnosis: subject-structural fidelity (SUBC) collapses on hard rotate/resize, while background and pixel-refinement remain strong. We then test five distinct classes of intervention — scalar/configuration tuning, input-quality and injection-strength, semantic-identity conditioning, geometry-aware attention (three mechanisms), and refinement-preservation. None breaks the structural ceiling; the geometry-aware attention changes actively hurt. A preservation experiment finally lifts SUBC marginally but, crucially, its flat dose-response shows FreeFine already reaches ~99.9% of the perfect-warp ceiling. We conclude the residual hard-case gap is intrinsic to the in-plane transform and the view-sensitivity of the metric, not an addressable algorithmic deficiency — a result that reframes the open problem toward out-of-plane and effect-aware editing.

1.  Objective and Constraints

FreeFine performs geometric image editing — repositioning, reorienting, and reshaping an object while preserving scene coherence — without any training, using a diffusion model steered by Temporal Contextual Attention (TCA), Local Perturbation, and Content-specified Generation. The thesis goal is twofold: (i) reproduce FreeFine exactly, and (ii) propose a training-free architectural extension that improves on it.

Reproduction constraint: the published GitHub code is run unchanged (single precision, no algorithmic edits — only environment, path, and verified-neutral bug fixes).

Method constraint: any change in the method phase is a documented part of the contribution, validated to leave the reproduced baseline byte-identical when disabled.

2.  Compute and Data Infrastructure

Compute: Kaggle, 2×NVIDIA T4 (~15 GB each), hard 12-hour per-commit limit; every run is deadline-guarded.

Benchmark: GeoBench-2D — 609 source images, 5,677 single-type edits (move 1,439 / rotate 1,603 / resize 2,635), scored on the paper’s seven metrics.

Development subset: a stratified, seed-42, reproducible balanced-200 subset used for all low-cost sweeps, with per-group cells (rotate_hard n=22, resize_hard n=23, move_all n=67, all_200 n=200).

Two environments: a generation environment (torch 2.1.1 / diffusers 0.18) and a metric environment (torch 2.6); for all method comparisons the stochastic MD metric is identically seeded across baseline and every variant.

Metrics (arrows): SUBC, BGC ↑ (subject- and background-consistency, higher better); FID, DINOv2/FDD, KD, WE/WRAP_E (warping error), MD (mean keypoint distance) ↓ (lower better).

3.  Phase 0 — Faithful Reproduction

FreeFine was reproduced at repository defaults (fp32, seed 42) and all 5,677 edits were generated and scored. The only source changes were environment/bug fixes (a confirmed use-before-assignment bug in the public 2D script; an identical SD-2.1 mirror for the MD metric), each verified numerically neutral; bit-identical generation was confirmed.

All seven metrics reproduce within ~2% of the paper; edit-precision (WE, MD) is marginally better. MD is the sole stochastic metric (two full runs: 8.50 / 8.55).

4.  Phase 1 — Metric-Driven Diagnosis

To locate the weakness objectively, the 5,677 cases were grouped by difficulty (normalized tertiles over translation, rotation, scale, mask area) and by edit type, and every metric was recomputed per group.

Results by difficulty (full set)

Results by edit type (full set)

Move is solved: MD ~3.8, SUBC 0.96 — translation is effectively handled.

Rotate/resize collapse on hard edits: MD rises ~4× (easy 4.85 → hard 13.37) and SUBC falls to ~0.87.

Background and pixel-refinement stay flat: BGC ≈ 0.967, WE ≈ 0.043–0.050 across all groups.

Interpretation: FreeFine preserves background and pixel-refines the edited region well; what it loses under large shape-changing edits is the object’s structure/identity — a failure captured by SUBC and MD but not by the pixel-level WE. The improvement target is therefore subject-structural fidelity on hard rotate/resize.

5.  Phase 2 — Controllability Sweep (falsification #1)

Before any architectural change, we asked whether FreeFine’s own controls can recover the failure. Three control families were swept on the balanced-200 subset with seeded MD: the TCA injection start-step, the modulated UNet attention layers, and classifier-free guidance via the object label. Two corrections were required first (a hardcoded attention-layer range that silenced the layer control; an empty text prompt that left CFG inactive); both were verified live afterwards.

SUBC is pinned: across the full sweep, hard-group SUBC stays within 0.8517–0.8529 (rotate) and 0.832–0.841 (resize) — controls can damage it but none lift it.

start_layer: verified live but a negative result (neutral on rotate, harmful on resize).

Prompt-CFG: one narrow real signal — resize_hard MD 19.47 → 17.75 — but no SUBC gain and slightly worse on rotate.

Conclusion: scalar/configuration tuning is exhausted; the bottleneck is mechanistic, not a hyperparameter.

6.  Phase B1 — Input Quality and Injection Strength (falsification #2)

Two cheap architectural levers: AA-Warp (supersampled-Lanczos coarse warp, removing aliasing) and Adaptive-ES (difficulty-scaled end_scale, the unswept floor of the structure-injection schedule).

end_scale is a clean negative: raising the injection floor hurts monotonically (resize MD 19.47 → 24.45). Baseline (decay to 0) is already optimal.

AA-Warp is hygiene, not a fix: tiny SUBC nudge and better WE, but no movement on the bottleneck — a third confirmation that input quality and injection strength are not the issue.

7.  Phase B2 — Semantic-Identity Conditioning (falsification #3)

We integrated IP-Adapter (SD-1.5) into the refinement: the source-object crop is fed as an image prompt, scoped to the target mask, injecting CLIP-image identity through a rotation/scale-tolerant channel. Scales 0.5–1.4 were swept.

Monotone degradation: on rotate_hard SUBC falls cleanly 0.8523 → 0.8502 as IP strength rises — more identity conditioning means worse rotation identity. SUBC is deterministic, so this 4-point trend is real.

Interpretation: the 4-token base adapter injects coarse semantic identity (“what the object is”), not the fine geometric structure SUBC scores. The diagnosed failure is structural, not semantic-forgetting, so identity conditioning treats the wrong problem — ruling out a third hypothesis class.

8.  Phase B3 — Geometry-Aligned TCA (the core architectural study)

Code-level diagnosis (verified in source): FreeFine’s TCA lets the target-pose query attend to the original source-pose key/value through a column mask only — there is no geometric correspondence; matching is left to feature similarity, which fails under rotation/scale. The per-edit affine transform, though known, is never used inside attention. We built a geometry-aware TCA realized at three architectural levels, all training-free and flag-gated:

G2 — correspondence bias (selection level): add a Gaussian prior to the attention logits so a target query attends to its geometrically-corresponding source token.

G1 — warped key/value (representation level): resample the reference feature field by the affine transform so source features are physically relocated to the target geometry.

R²-TCA — warped reference (input level): give the reference branch the source already warped to target pose, so correspondence becomes near-identity.

G3 — validity gating: disoccluded target tokens (no source correspondence) fall back to self-attention.

All mechanisms were unit-tested on CPU (translation maps 64/64 tokens; 30° rotation within 0.66 cells) before any GPU run.

Every variant lowers SUBC: none breaks the ceiling; the attention-level interventions (bias, warp) hurt most, the input-level R²-TCA is roughly neutral.

The smoking gun — move: pure translation is geometrically trivial and baseline solved it (0.959), yet every variant damages it. So the mechanisms degrade through their own artifacts (over-sharpened attention, bilinear feature blur, warp interpolation), not through a geometry-difficulty effect.

Theory correction (the key insight of B3): GeoBench-2D edits are in-plane, so the correct target appearance is fully available (it is the warped source). R²-TCA handed the reference branch a clean, geometrically-ideal target-pose source — and still did not beat baseline. The reference’s pose-mismatch is therefore not the bottleneck. The structural collapse lives downstream, in the diffusion refinement itself, not in the attention correspondence.

9.  Phase B4 — Refinement Preservation (the decisive test)

Targeting the corrected diagnosis, B4 anchors the edit-branch latent to the coarse (the correct in-plane warp) inside the object region during denoising, with strength w: w=0 is baseline, w→1 pins the object to the coarse. This both is a lever and tests whether refinement was degrading the object.

First positive: for the first time SUBC beats baseline everywhere (all_200 +0.0021, deterministic) and WE improves ~7% — at a small FID cost. A modest Pareto trade.

The decisive finding — flat dose response: SUBC is identical across w=0.3–0.9. At w=0.9 the object is ~pinned to the coarse (the perfect in-plane warp), giving rotate_hard SUBC ≈ 0.8535 — only +0.0012 above the refined baseline 0.8523.

Conclusion: FreeFine’s refinement already reaches ~99.9% of the perfect-warp subject-consistency ceiling. The hard-case “collapse” is present in the coarse perfect-warp itself — it is intrinsic to the in-plane transform and the view-sensitivity of DINOv2, not an addressable algorithmic deficiency. No reference/correspondence/preservation change can meaningfully raise hard-group SUBC, because the ceiling is the warp.

10.  Synthesis — What Has Been Established

Across five distinct intervention classes the subject-structural ceiling is robust, and B4 explains why: the ceiling is the perfect-warp itself. FreeFine is near-optimal for GeoBench-2D subject-consistency.

Headline: the apparent weakness on hard rotate/resize is largely intrinsic (transform + metric view-sensitivity), not an algorithmic gap; FreeFine reaches ~99.9% of the achievable subject-consistency ceiling on these edits.

Methodological contribution: a rigorous, metric-driven diagnosis plus a systematic five-class falsification that localizes the bottleneck and demonstrates near-optimality — with a small, honest preservation improvement (SUBC +0.2%, WE −7%).

11.  Methodological Rigor

Provenance discipline: every number is labelled measured / derived / reconstructed; small-n cells (rotate_hard n=22, resize_hard n=23) are always flagged.

Seeded ablations: MD’s DIFT noise is identically seeded across baseline and every variant, so reported differences reflect the method, not chance; the reproduction-vs-paper figure keeps the unseeded metric.

FID-family caveat: FID / DINOv2 / KD are reliable only at full-set scale; on subsets they are inflated and are excluded from per-group quality claims.

Code-grounded claims: each method was verified in source and unit-tested on CPU before any GPU run; the no-op control (method disabled) reproduces the baseline byte-identically.

Fault tolerance: sweeps are per-variant isolated and deadline-guarded, so one failure never costs a whole commit.

12.  Next Directions

The near-ceiling result reframes the open problem: 2D in-plane subject-consistency is effectively solved, so a remarkable contribution must address where the source genuinely lacks information, or where every method (including FreeFine) is still visibly wrong. Five structural directions, each drawing on a different area of AI:

A. Generative 3D-prior TCA: for out-of-plane rotation, replace FreeFine’s depth-warp — which cannot hallucinate unseen surfaces — with a generative novel-view synthesis (Zero123++ / SV3D-style), then refine with TCA. Targets GeoBench-3D, where real headroom remains.

B. Effects-aware editing: synthesize the object’s shadows / reflections / contact at the target and remove them at the source — a glaring, largely unaddressed realism gap. Draws on intrinsic decomposition / relighting; reuses the 2D infrastructure.

C. Equivariance / cycle-consistency: an inference-time objective enforcing edit ∘ inverse-edit ≈ identity. Principled, general; draws on self-supervised learning and test-time guidance.

D. Non-rigid / articulated editing: extend beyond affine using foundation-model emergent correspondence to drive deformation fields — a capability expansion (edits FreeFine cannot currently do).

E. Amodal / layered editing: decompose, amodally complete the occluded object, edit in its canonical frame, recompose — principled disocclusion handling.

13.  Key References

FreeFine — Training-free Geometric Image Editing on Diffusion Models, ICCV 2025 (arXiv:2507.23300).

GeoDiffuser — Geometry-Based Image Editing with Diffusion Models, WACV 2025 (arXiv:2404.14403).

DragonDiffusion (arXiv:2307.02421) / DiffEditor (arXiv:2402.02583) — energy-guided editing.

IP-Adapter — Image Prompt Adapter for Text-to-Image Diffusion Models (arXiv:2308.06721).

Zero-1-to-3 (arXiv:2303.11328), Zero123++, SV3D — single-image novel-view / 3D priors.

Effects-Sensitive In-Context Inpainting for Geometric Editing (arXiv:2602.08388, 2026).


### Table 1


| Metric | Paper | Reproduced | Diff | Assessment |

| --- | --- | --- | --- | --- |

| FID ↓ | 34.72 | 35.04 | +0.9% | match |

| DINOv2 / FDD ↓ | 478.18 | 487.82 | +2.0% | match |

| KD ↓ | 0.144 | 0.142 | −1.2% | match |

| SUBC ↑ | 0.907 | 0.911 | +0.4% | match |

| BC / BGC ↑ | 0.971 | 0.967 | −0.4% | match |

| WE ↓ | 0.055 | 0.047 | −14.5% | better |

| MD ↓ | 9.25 | 8.50 | −8.1% | better |


### Table 2


| Difficulty | SUBC ↑ | BGC ↑ | WE ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| easy | 0.942 | 0.971 | 0.046 | 4.85 |

| medium | 0.927 | 0.966 | 0.046 | 6.98 |

| hard | 0.865 | 0.964 | 0.050 | 13.37 |


### Table 3


| Edit type | SUBC ↑ | BGC ↑ | WE ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| move | 0.959 | 0.967 | 0.049 | 3.75 |

| rotate | 0.901 | 0.967 | 0.043 | 10.43 |

| resize | 0.892 | 0.967 | 0.049 | 9.96 |


### Table 4


| Variant | rotate_hard SUBC | resize_hard SUBC | resize_hard MD |

| --- | --- | --- | --- |

| baseline (ss35) | 0.8523 | 0.8391 | 19.47 |

| start_step 45 | 0.8529 | 0.8414 | 18.09 |

| start_layer 8 | 0.8522 | 0.8382 | 21.61 |

| prompt-CFG 10 | 0.8529 | 0.8391 | 17.75 |


### Table 5


| Variant | rot_h SUBC | res_h SUBC | res_h MD | all200 WE |

| --- | --- | --- | --- | --- |

| baseline | 0.8523 | 0.8391 | 19.47 | 0.0488 |

| AA-Warp | 0.8537 | 0.8403 | 19.67 | 0.0486 |

| end_scale 0.25 | 0.8524 | 0.8388 | 22.06 | 0.0492 |

| end_scale 0.50 | 0.8522 | 0.8380 | 24.45 | 0.0498 |


### Table 6


| IP scale | rotate_hard SUBC | resize_hard SUBC | all_200 SUBC |

| --- | --- | --- | --- |

| baseline | 0.8523 | 0.8391 | 0.9154 |

| 0.5 | 0.8523 | 0.8396 | 0.9154 |

| 0.8 | 0.8518 | 0.8394 | 0.9153 |

| 1.1 | 0.8512 | 0.8393 | 0.9150 |

| 1.4 | 0.8502 | 0.8390 | 0.9147 |


### Table 7


| Variant | rot_h SUBC | res_h SUBC | move SUBC | all200 SUBC |

| --- | --- | --- | --- | --- |

| baseline | 0.8523 | 0.8391 | 0.959 | 0.9154 |

| G2 bias λ4 | 0.8318 | 0.8284 | 0.9415 | 0.9013 |

| G2 bias λ8 | 0.8269 | 0.8257 | 0.9373 | 0.8979 |

| G1 warp | 0.8438 | 0.8329 | 0.9542 | 0.9095 |

| G1 warp + gate | 0.8445 | 0.8336 | 0.9562 | 0.9106 |

| R²-TCA | 0.8495 | 0.8334 | 0.956 | 0.9128 |


### Table 8


| Variant | rot_h SUBC | res_h SUBC | all200 SUBC | all200 WE | FID |

| --- | --- | --- | --- | --- | --- |

| baseline | 0.8523 | 0.8391 | 0.9154 | 0.0488 | 132.3 |

| w = 0.3 | 0.8536 | 0.8409 | 0.9175 | 0.0454 | 133.1 |

| w = 0.5 | 0.8535 | 0.8404 | 0.9174 | 0.0453 | 133.4 |

| w = 0.7 | 0.8535 | 0.8400 | 0.9174 | 0.0453 | 133.5 |

| w = 0.9 | 0.8535 | 0.8399 | 0.9174 | 0.0453 | 133.5 |


### Table 9


| Phase | Class | Mechanism | Outcome on hard-group SUBC |

| --- | --- | --- | --- |

| Phase 2 | Tuning | start-step / layer / guidance | Pinned — no lift |

| B1 | Input / strength | AA-warp, end_scale floor | Marginal / negative |

| B2 | Identity | IP-Adapter conditioning | Monotone degradation |

| B3 | Geometry | warp / bias / pixel-warp | Degraded (artifacts) |

| B4 | Preservation | latent blend to coarse | +0.001–0.002 (at the ceiling) |