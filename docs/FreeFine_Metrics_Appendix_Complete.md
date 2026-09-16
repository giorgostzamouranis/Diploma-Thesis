FreeFine — Complete Metrics Appendix

All measured metrics from every experiment · Phases 0–B4 · Diploma Thesis · Giorgos Tzamouranis · 20 June 2026

Definitive data sheet. Every value is a measured result. Arrows: SUBC, BGC ↑; FID, DINOv2/FDD, KD, WE/WRAP_E, MD ↓. BC = BGC; WE = WRAP_E; DINOv2 = FDD. Baseline row shaded; best MD per hard group in green. Phases 0–2b are full-set / balanced-200 as noted; B1–B4 are balanced-200 with seeded MD (rotate_hard n=22, resize_hard n=23, move_all n=67, all_200 n=200).

Phase 0 — Full-set reproduction (5,677 edits)

Repo defaults, fp32, seed 42. MD stochastic (two runs 8.50/8.55).

Phase 1 — Per-group diagnostic (full set, 5,677 edits)

By difficulty

By edit type

FID/DINOv2/KD omitted per-group (subset-inflated). Approx hard-subgroup MD: hard rotate ≈15.7, hard resize ≈16.5.

Phase 2 / 2b — Balanced-200 controllability sweep (seeded MD)

rotate_hard (n=22)

resize_hard (n=23)

move_all (n=67)

all_200 (n=200)

Variants: ss=start_step, l=start_layer (model.py fix, live), p=prompt-enabled CFG. g5/g10 empty-prompt CFG verified ≡ baseline (omitted).

B1 — AA-Warp + Adaptive-ES (balanced-200)

rotate_hard (n=22)

resize_hard (n=23)

move_all (n=67)

all_200 (n=200)

aaw=AA-Warp; es25/es50=end_scale floor 0.25/0.5; esA=difficulty-adaptive (easy0/med0.25/hard0.5); aaw_esA=combo. AA WRAP_E scored vs AA coarse. esA hard groups ≡ es50 by construction.

B2 — IP-Adapter identity conditioning (balanced-200)

rotate_hard (n=22)

resize_hard (n=23)

move_all (n=67)

all_200 (n=200)

ipNN = IP-Adapter scale NN/100. Monotone SUBC degradation on rotate_hard with scale.

B3 — Geometry-Aligned TCA (balanced-200)

rotate_hard (n=22)

resize_hard (n=23)

move_all (n=67)

all_200 (n=200)

g2=correspondence bias (λ); g1_warp=warped K/V; g1warp_gate=+G3 validity gate; r2=R²-TCA warped reference. All lower SUBC vs baseline.

B4 — Refinement preservation (balanced-200)

rotate_hard (n=22)

resize_hard (n=23)

move_all (n=67)

all_200 (n=200)

pres_wNN = preservation blend strength 0.NN. SUBC flat across w (dose-saturated) → near the perfect-warp ceiling.

Measurement & provenance notes

Phase 0/1: full GeoBench-2D (5,677), repo-default unmodified scoring, fp32 seed 42; MD unseeded/stochastic (noise floor ≈0.05 global, ≈0.15 hardest).

Phase 2–B4: balanced-200, seeded MD (seed 42) across baseline and every variant; hard groups small (n=22/23) — treat sub-0.005 SUBC and sub-0.15 MD moves as within range.

FID family: reliable only at full-set scale; the all_200 FID/DINOv2/KD are subset-inflated and carry run-to-run noise (baseline FID_KD varies 0.123–0.129 across runs) — use for trend, not fine claims.

Determinism: SUBC/BGC/WRAP_E are deterministic (reproduce exactly); only MD and the FID-family carry stochastic/subset variation.


### Table 1


| Metric | Paper | Reproduced | Diff |

| --- | --- | --- | --- |

| FID ↓ | 34.72 | 35.04 | +0.9% |

| DINOv2 / FDD ↓ | 478.18 | 487.82 | +2.0% |

| KD ↓ | 0.144 | 0.142 | −1.2% |

| SUBC ↑ | 0.907 | 0.911 | +0.4% |

| BC / BGC ↑ | 0.971 | 0.967 | −0.4% |

| WE ↓ | 0.055 | 0.047 | −14.5% |

| MD ↓ | 9.25 | 8.50 (exact 8.4993) | −8.1% |


### Table 2


| Group | SUBC ↑ | BGC ↑ | WE ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| easy | 0.942 | 0.971 | 0.046 | 4.85 |

| medium | 0.927 | 0.966 | 0.046 | 6.98 |

| hard | 0.865 | 0.964 | 0.050 | 13.37 |


### Table 3


| Group | SUBC ↑ | BGC ↑ | WE ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| move | 0.959 | 0.967 | 0.049 | 3.75 |

| rotate | 0.901 | 0.967 | 0.043 | 10.43 |

| resize | 0.892 | 0.967 | 0.049 | 9.96 |


### Table 4


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8523 | 0.9664 | 0.0416 | 14.0096 |

| ss25 | 0.8497 | 0.9681 | 0.0459 | 15.2464 |

| ss30 | 0.8519 | 0.9675 | 0.0437 | 15.9111 |

| ss40 | 0.8528 | 0.9676 | 0.0398 | 15.0132 |

| ss45 | 0.8529 | 0.9666 | 0.0384 | 15.0901 |

| l4 | 0.8524 | 0.9672 | 0.0425 | 15.3029 |

| l8 | 0.8522 | 0.967 | 0.0424 | 14.329 |

| l12 | 0.8517 | 0.9669 | 0.0412 | 14.6813 |

| p7.5 | 0.8528 | 0.9675 | 0.0416 | 14.5514 |

| p10 | 0.8529 | 0.968 | 0.0416 | 14.6852 |


### Table 5


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8391 | 0.9631 | 0.0585 | 19.4713 |

| ss25 | 0.8319 | 0.9618 | 0.0658 | 21.1346 |

| ss30 | 0.8376 | 0.9636 | 0.0619 | 20.7004 |

| ss40 | 0.8413 | 0.9637 | 0.0555 | 20.1565 |

| ss45 | 0.8414 | 0.9624 | 0.0535 | 18.0894 |

| l4 | 0.8378 | 0.9622 | 0.0587 | 21.6877 |

| l8 | 0.8382 | 0.9629 | 0.0586 | 21.6105 |

| l12 | 0.8383 | 0.9616 | 0.0579 | 22.453 |

| p7.5 | 0.839 | 0.9626 | 0.0586 | 18.3849 |

| p10 | 0.8391 | 0.9625 | 0.0587 | 17.7459 |


### Table 6


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ |

| --- | --- | --- | --- |

| baseline | 0.959 | 0.9639 | 0.0495 |

| ss25 | 0.9542 | 0.9647 | 0.0534 |

| ss30 | 0.9571 | 0.9642 | 0.0512 |

| ss40 | 0.9605 | 0.9627 | 0.048 |

| ss45 | 0.9612 | 0.9629 | 0.0468 |

| l4 | 0.9587 | 0.9639 | 0.0497 |

| l8 | 0.9587 | 0.9639 | 0.0496 |

| l12 | 0.959 | 0.9628 | 0.0494 |

| p7.5 | 0.9588 | 0.9638 | 0.0496 |

| p10 | 0.9587 | 0.9639 | 0.0497 |


### Table 7


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | FID ↓ | FID_DINO ↓ | FID_KD ↓ |

| --- | --- | --- | --- | --- | --- | --- |

| baseline | 0.9154 | 0.9657 | 0.0488 | 132.279 | 1636.8248 | 0.1285 |

| ss25 | 0.9113 | 0.9667 | 0.054 | 132.5674 | 1636.0803 | 0.127 |

| ss30 | 0.9139 | 0.9663 | 0.0513 | 132.7277 | 1636.6126 | 0.1264 |

| ss40 | 0.9166 | 0.965 | 0.0468 | 133.0883 | 1640.2611 | 0.1347 |

| ss45 | 0.9174 | 0.9641 | 0.0452 | 133.5788 | 1643.6987 | 0.1397 |

| l4 | 0.9152 | 0.9658 | 0.0492 | 132.4057 | 1636.8961 | 0.1264 |

| l8 | 0.9152 | 0.9658 | 0.0491 | 132.5017 | 1637.1739 | 0.1303 |

| l12 | 0.9152 | 0.965 | 0.0486 | 132.8193 | 1637.5069 | 0.1276 |

| p7.5 | 0.9154 | 0.9656 | 0.0489 | 132.3545 | 1637.8364 | 0.1273 |

| p10 | 0.9154 | 0.9657 | 0.049 | 132.5098 | 1637.8859 | 0.1326 |


### Table 8


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8523 | 0.9664 | 0.0416 | 14.0096 |

| aaw | 0.8537 | 0.9663 | 0.0447 | 14.5439 |

| es25 | 0.8524 | 0.9671 | 0.0423 | 14.7356 |

| es50 | 0.8522 | 0.9672 | 0.0434 | 14.9638 |

| esA | 0.8522 | 0.9672 | 0.0434 | 14.9638 |

| aaw_esA | 0.8536 | 0.9662 | 0.0463 | 15.0177 |


### Table 9


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8391 | 0.9631 | 0.0585 | 19.4713 |

| aaw | 0.8403 | 0.9628 | 0.0573 | 19.6664 |

| es25 | 0.8388 | 0.963 | 0.0591 | 22.0592 |

| es50 | 0.838 | 0.9632 | 0.06 | 24.4517 |

| esA | 0.838 | 0.9632 | 0.06 | 24.4517 |

| aaw_esA | 0.8388 | 0.9631 | 0.059 | 20.2972 |


### Table 10


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ |

| --- | --- | --- | --- |

| baseline | 0.959 | 0.9639 | 0.0495 |

| aaw | 0.9592 | 0.9635 | 0.0454 |

| es25 | 0.9588 | 0.9644 | 0.0496 |

| es50 | 0.9582 | 0.9652 | 0.05 |

| esA | 0.9583 | 0.9646 | 0.0499 |

| aaw_esA | 0.9586 | 0.9647 | 0.0459 |


### Table 11


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | FID ↓ | FID_DINO ↓ | FID_KD ↓ |

| --- | --- | --- | --- | --- | --- | --- |

| baseline | 0.9154 | 0.9657 | 0.0488 | 132.279 | 1636.8248 | 0.127 |

| aaw | 0.9156 | 0.9654 | 0.0486 | 132.3575 | 1637.268 | 0.1297 |

| es25 | 0.9155 | 0.966 | 0.0492 | 132.3072 | 1637.9401 | 0.125 |

| es50 | 0.9152 | 0.9666 | 0.0498 | 132.5224 | 1638.5029 | 0.1307 |

| esA | 0.9151 | 0.9661 | 0.0494 | 132.5459 | 1638.0476 | 0.1247 |

| aaw_esA | 0.9153 | 0.9659 | 0.0492 | 132.6294 | 1638.4158 | 0.1255 |


### Table 12


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8523 | 0.9664 | 0.0416 | 14.0096 |

| ip50 | 0.8523 | 0.9669 | 0.0416 | 14.6752 |

| ip80 | 0.8518 | 0.9668 | 0.0416 | 14.8623 |

| ip110 | 0.8512 | 0.9668 | 0.0417 | 15.4672 |

| ip140 | 0.8502 | 0.9667 | 0.0417 | 15.228 |


### Table 13


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8391 | 0.9631 | 0.0585 | 19.4713 |

| ip50 | 0.8396 | 0.9629 | 0.0584 | 21.4861 |

| ip80 | 0.8394 | 0.9627 | 0.0584 | 18.7526 |

| ip110 | 0.8393 | 0.9627 | 0.0585 | 19.4285 |

| ip140 | 0.839 | 0.9624 | 0.0586 | 21.5396 |


### Table 14


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ |

| --- | --- | --- | --- |

| baseline | 0.959 | 0.9639 | 0.0495 |

| ip50 | 0.959 | 0.9638 | 0.0495 |

| ip80 | 0.9589 | 0.9638 | 0.0496 |

| ip110 | 0.9587 | 0.9638 | 0.0497 |

| ip140 | 0.9585 | 0.9637 | 0.0498 |


### Table 15


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | FID ↓ | FID_DINO ↓ | FID_KD ↓ |

| --- | --- | --- | --- | --- | --- | --- |

| baseline | 0.9154 | 0.9657 | 0.0488 | 132.279 | 1636.8248 | 0.127 |

| ip50 | 0.9154 | 0.9656 | 0.0488 | 132.0828 | 1637.4637 | 0.1321 |

| ip80 | 0.9153 | 0.9656 | 0.0489 | 132.1062 | 1637.4597 | 0.1303 |

| ip110 | 0.915 | 0.9656 | 0.049 | 132.1496 | 1637.5607 | 0.1279 |

| ip140 | 0.9147 | 0.9655 | 0.049 | 132.2715 | 1637.7355 | 0.1286 |


### Table 16


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8523 | 0.9664 | 0.0416 | 14.0096 |

| g2_l4 | 0.8318 | 0.9596 | 0.0484 | 14.2244 |

| g2_l8 | 0.8269 | 0.9575 | 0.0496 | 14.6003 |

| g1_warp | 0.8438 | 0.9611 | 0.0422 | 15.4191 |

| g1warp_gate | 0.8445 | 0.9657 | 0.0419 | 15.2974 |

| r2 | 0.8495 | 0.9629 | 0.0399 | 14.8559 |


### Table 17


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8391 | 0.9631 | 0.0585 | 19.4713 |

| g2_l4 | 0.8284 | 0.9561 | 0.0624 | 17.9071 |

| g2_l8 | 0.8257 | 0.9541 | 0.0632 | 19.9736 |

| g1_warp | 0.8329 | 0.9573 | 0.0602 | 22.2831 |

| g1warp_gate | 0.8336 | 0.9571 | 0.0583 | 26.5216 |

| r2 | 0.8334 | 0.9557 | 0.06 | 21.0155 |


### Table 18


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ |

| --- | --- | --- | --- |

| baseline | 0.959 | 0.9639 | 0.0495 |

| g2_l4 | 0.9415 | 0.9593 | 0.0572 |

| g2_l8 | 0.9373 | 0.9574 | 0.0589 |

| g1_warp | 0.9542 | 0.9591 | 0.0507 |

| g1warp_gate | 0.9562 | 0.9593 | 0.05 |

| r2 | 0.956 | 0.9623 | 0.0506 |


### Table 19


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | FID ↓ | FID_DINO ↓ | FID_KD ↓ |

| --- | --- | --- | --- | --- | --- | --- |

| baseline | 0.9154 | 0.9657 | 0.0488 | 132.279 | 1636.8248 | 0.1273 |

| g2_l4 | 0.9013 | 0.9607 | 0.0546 | 135.1509 | 1642.1749 | 0.1463 |

| g2_l8 | 0.8979 | 0.9585 | 0.0557 | 135.8088 | 1644.6477 | 0.1488 |

| g1_warp | 0.9095 | 0.9598 | 0.0498 | 133.4685 | 1640.5089 | 0.13 |

| g1warp_gate | 0.9106 | 0.9614 | 0.0492 | 133.5782 | 1642.8418 | 0.1336 |

| r2 | 0.9128 | 0.9633 | 0.0487 | 132.5187 | 1635.2379 | 0.1261 |


### Table 20


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8523 | 0.9664 | 0.0416 | 14.0096 |

| pres_w03 | 0.8536 | 0.9663 | 0.0397 | 14.6308 |

| pres_w05 | 0.8535 | 0.9663 | 0.0396 | 14.6929 |

| pres_w07 | 0.8535 | 0.9661 | 0.0395 | 14.7735 |

| pres_w09 | 0.8535 | 0.9661 | 0.0395 | 14.8722 |


### Table 21


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | MD ↓ |

| --- | --- | --- | --- | --- |

| baseline | 0.8391 | 0.9631 | 0.0585 | 19.4713 |

| pres_w03 | 0.8409 | 0.9605 | 0.0538 | 21.7356 |

| pres_w05 | 0.8404 | 0.9593 | 0.0537 | 20.1519 |

| pres_w07 | 0.84 | 0.9599 | 0.0537 | 22.0379 |

| pres_w09 | 0.8399 | 0.9607 | 0.0537 | 24.1885 |


### Table 22


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ |

| --- | --- | --- | --- |

| baseline | 0.959 | 0.9639 | 0.0495 |

| pres_w03 | 0.961 | 0.9624 | 0.0468 |

| pres_w05 | 0.9612 | 0.9622 | 0.0467 |

| pres_w07 | 0.9614 | 0.9621 | 0.0467 |

| pres_w09 | 0.9614 | 0.9622 | 0.0467 |


### Table 23


| Variant | SUBC ↑ | BGC ↑ | WRAP_E ↓ | FID ↓ | FID_DINO ↓ | FID_KD ↓ |

| --- | --- | --- | --- | --- | --- | --- |

| baseline | 0.9154 | 0.9657 | 0.0488 | 132.279 | 1636.8248 | 0.1228 |

| pres_w03 | 0.9175 | 0.9631 | 0.0454 | 133.1397 | 1641.7848 | 0.1391 |

| pres_w05 | 0.9174 | 0.9627 | 0.0453 | 133.3756 | 1643.6384 | 0.1462 |

| pres_w07 | 0.9174 | 0.9625 | 0.0453 | 133.4504 | 1644.1713 | 0.1449 |

| pres_w09 | 0.9174 | 0.9626 | 0.0453 | 133.5082 | 1644.4654 | 0.142 |