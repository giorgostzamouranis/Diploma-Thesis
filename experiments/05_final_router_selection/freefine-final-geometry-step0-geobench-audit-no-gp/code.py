# %% [cell 1]
import os, glob, json, hashlib, math
import numpy as np
import pandas as pd

print("Kaggle inputs:")
for p in sorted(glob.glob("/kaggle/input/*")):
    print(" -", p)

def find_one(patterns, desc):
    xs=[]
    for pat in patterns:
        xs += glob.glob(pat, recursive=True)
    xs=[x for x in xs if os.path.isfile(x)]
    if not xs:
        raise FileNotFoundError(f"Missing {desc}. Tried: {patterns}")
    return sorted(set(xs), key=lambda x:(len(x),x))[0]

META=find_one(
    ["/kaggle/input/**/sample_metadata.csv"],
    "sample_metadata.csv"
)
ANN=find_one(
    ["/kaggle/input/**/annotation_2d.json",
     "/kaggle/input/**/annotations_2d.json"],
    "annotation_2d.json / annotations_2d.json"
)

print("\nResolved:")
print("META =", META)
print("ANN  =", ANN)

df=pd.read_csv(META,dtype=str)
for c in ["edit_type","difficulty"]:
    if c in df.columns:
        df[c]=df[c].astype(str).str.strip().str.lower()

required={"da_n","ins_id","case_id","edit_type"}
miss=required-set(df.columns)
assert not miss, f"metadata missing columns: {miss}"

df2=df[df.edit_type.isin(["move","rotate","resize"])].copy()

expected={"move":1439,"rotate":1603,"resize":2635}
got=df2.edit_type.value_counts().to_dict()
print("\n2D counts:", got, "total=",len(df2))
assert len(df2)==5677
assert got==expected, (got,expected)

ann=json.load(open(ANN))

def case_obj(row):
    d=str(row["da_n"]); i=str(row["ins_id"]); c=str(row["case_id"])
    # JSON keys are strings in the official annotations.
    try:
        return ann[d]["instances"][i][c]
    except Exception as e:
        # print nearby keys once for an actionable error
        if d not in ann:
            raise KeyError(f"da_n {d} not in annotation; first keys={list(ann)[:10]}") from e
        inst=ann[d].get("instances",{})
        if i not in inst:
            raise KeyError(f"ins_id {i} not under da_n={d}; keys={list(inst)[:10]}") from e
        raise KeyError(f"case_id {c} not under da_n={d}, ins_id={i}; keys={list(inst[i])[:20]}") from e

rows=[]
for _,r in df2.iterrows():
    obj=case_obj(r)
    ep=obj.get("edit_param")
    if ep is None:
        raise KeyError(f"Missing edit_param for {(r.da_n,r.ins_id,r.case_id)}; keys={list(obj)}")
    if len(ep)!=9:
        raise ValueError(f"Expected 9 edit params, got {len(ep)} for {(r.da_n,r.ins_id,r.case_id)}: {ep}")
    dx,dy,dz,rx,ry,rz,sx,sy,sz=[float(x) for x in ep]
    rows.append({
        "da_n":str(r.da_n),"ins_id":str(r.ins_id),"case_id":str(r.case_id),
        "edit_type":r.edit_type,
        "diagnostic_difficulty": r.get("difficulty", ""),
        "dx":dx,"dy":dy,"dz":dz,"rx":rx,"ry":ry,"rz":rz,
        "sx":sx,"sy":sy,"sz":sz,
    })

aff=pd.DataFrame(rows)
print("\nExact edit_param extraction: OK", len(aff))

# Stable manifest hash based on exact affine parameters.
manifest_lines=[]
for q in aff.sort_values(["da_n","ins_id","case_id"]).itertuples():
    manifest_lines.append(
        f"{q.da_n}|{q.ins_id}|{q.case_id}|{q.edit_type}|"
        f"{q.dx:.12g}|{q.dy:.12g}|{q.dz:.12g}|{q.rx:.12g}|{q.ry:.12g}|{q.rz:.12g}|"
        f"{q.sx:.12g}|{q.sy:.12g}|{q.sz:.12g}"
    )
manifest_sha=hashlib.sha256("\n".join(manifest_lines).encode()).hexdigest()
print("Exact-affine manifest SHA256:",manifest_sha)

aff.to_csv("/kaggle/working/geobench_2d_exact_affine_manifest_5677.csv",index=False)

# %% [cell 2]
# Sanity-check what the official inference parameters actually contain.

def desc(sub, cols):
    return sub[cols].astype(float).describe().T[["count","min","max","mean","50%"]]

for t in ["move","rotate","resize"]:
    s=aff[aff.edit_type==t]
    print(f"\n=== {t.upper()} n={len(s)} ===")
    display(desc(s,["dx","dy","rz","sx","sy","sz"]))

resize=aff[aff.edit_type=="resize"].copy()

# FreeFine's 2D resize is expected to be isotropic in GeoBench: sx == sy.
resize["anisotropy_abs"]=np.abs(resize.sx-resize.sy)
print("\nResize |sx-sy|:")
print(resize.anisotropy_abs.describe())

# Use the exact requested scale. If tiny numeric differences exist, use geometric mean.
resize["scale_exact"]=np.sqrt(resize.sx*resize.sy)

# Check that "resize" cases actually resize and that move/rotate generally use unit scale.
print("\nResize exact scale:")
display(resize["scale_exact"].describe().to_frame().T)

near_unit=(np.abs(resize.scale_exact-1.0)<1e-8).sum()
print("resize cases with scale == 1:",int(near_unit))

nonresize=aff[aff.edit_type!="resize"].copy()
unit_err=np.maximum(np.abs(nonresize.sx-1),np.abs(nonresize.sy-1))
print("non-resize max scale deviation from 1:",float(unit_err.max()))

# We require near-isotropic scaling for the simple scalar severity rule.
if resize.anisotropy_abs.max() > 1e-6:
    raise RuntimeError(
        "GeoBench contains materially anisotropic resize cases. "
        "Do not use a single scalar threshold without reviewing sx/sy separately."
    )

# %% [cell 3]
# Freeze a deployable severe-resize rule from the actual requested affine.
#
# We use the boundary between the medium and hard resize ranges reported by FreeFine:
# enlarge: hard starts at 1.5
# shrink:  hard extends through 0.6
#
# IMPORTANT: this is NOT inferred from generated-image metrics and does NOT read the
# thesis diagnostic_difficulty field.

ENLARGE_SEVERE=1.5
SHRINK_SEVERE=0.6

resize["router_severe"]=(resize.scale_exact>=ENLARGE_SEVERE) | (resize.scale_exact<=SHRINK_SEVERE)
resize["direction"]=np.where(resize.scale_exact>1,"enlarge","shrink")

print("Router split on all 2,635 resize cases:")
print(resize.router_severe.value_counts().rename(index={False:"nonsevere",True:"severe"}))
print("\nDirection x severity:")
display(pd.crosstab(resize.direction,resize.router_severe,margins=True))

print("\nExact scale ranges selected by router:")
display(resize.groupby(["direction","router_severe"])["scale_exact"].agg(["count","min","max","mean","median"]))

# Boundary audit: exact-equality samples deserve explicit reporting because the paper's
# printed ranges touch at 0.6 and 1.5.
eq15=resize[np.isclose(resize.scale_exact,1.5,rtol=0,atol=1e-10)]
eq06=resize[np.isclose(resize.scale_exact,0.6,rtol=0,atol=1e-10)]
print("\nExact boundary samples:")
print("scale == 1.5:",len(eq15))
print("scale == 0.6:",len(eq06))
if len(eq15):
    display(eq15[["da_n","ins_id","case_id","scale_exact"]].head(50))
if len(eq06):
    display(eq06[["da_n","ins_id","case_id","scale_exact"]].head(50))

# For transparency only: show how our old *diagnostic tertile* labels distribute under the
# new affine rule. We deliberately DO NOT require agreement.
if "diagnostic_difficulty" in resize.columns:
    print("\nDiagnostic tertile label x affine router (report only; NOT a validity test):")
    display(pd.crosstab(resize.diagnostic_difficulty,resize.router_severe,margins=True))

audit_status="PASS_EXACT_AFFINE"
print("\nAUDIT STATUS:",audit_status)

# %% [cell 4]
router_cfg={
    "version":"SGR_router_pre_full_v2",
    "selection_source":"annotation edit_param (exact FreeFine inference input)",
    "resize_scale_definition":"sqrt(sx*sy); audited isotropic sx==sy",
    "resize_severe_rule":{
        "enlarge":"scale >= 1.5",
        "shrink":"scale <= 0.6",
        "enlarge_threshold":1.5,
        "shrink_threshold":0.6,
    },
    "branches_common":{
        "move":"RING4_MOVE_POST",
        "rotate":"FREEFINE_BASELINE",
        "resize_nonsevere":"RING8_GLOBAL_POST",
    },
    "pipeline_A_resize_severe":"EPSREC_PROMPT_ALL",
    "pipeline_B_resize_severe":"MIDHF_EPSREC_PROMPT_ALL",
    "geobench_2d_n":int(len(aff)),
    "counts":{k:int(v) for k,v in got.items()},
    "resize_n":int(len(resize)),
    "resize_severe_n":int(resize.router_severe.sum()),
    "resize_nonsevere_n":int((~resize.router_severe).sum()),
    "exact_affine_manifest_sha256":manifest_sha,
    "audit_status":audit_status,
    "methodological_note":(
        "The thesis sample_metadata difficulty field is diagnostic stratification only and "
        "is never used for final branch selection. Final routing uses exact edit_param scale."
    )
}

json.dump(router_cfg,open("/kaggle/working/final_geometry_router_config_v2.json","w"),indent=2)
resize.to_csv("/kaggle/working/resize_exact_affine_router_2635.csv",index=False)

summary={
    "audit_status":audit_status,
    "manifest_sha256":manifest_sha,
    "counts":router_cfg["counts"],
    "resize_n":router_cfg["resize_n"],
    "severe_n":router_cfg["resize_severe_n"],
    "nonsevere_n":router_cfg["resize_nonsevere_n"],
    "min_scale":float(resize.scale_exact.min()),
    "max_scale":float(resize.scale_exact.max()),
    "max_abs_sx_sy_difference":float(resize.anisotropy_abs.max()),
    "exact_scale_1p5_n":int(len(eq15)),
    "exact_scale_0p6_n":int(len(eq06)),
}
json.dump(summary,open("/kaggle/working/geobench_exact_affine_audit_summary_v2.json","w"),indent=2)

print(json.dumps(router_cfg,indent=2))
print("\nSaved:")
for p in [
    "/kaggle/working/final_geometry_router_config_v2.json",
    "/kaggle/working/geobench_exact_affine_audit_summary_v2.json",
    "/kaggle/working/geobench_2d_exact_affine_manifest_5677.csv",
    "/kaggle/working/resize_exact_affine_router_2635.csv",
]:
    print(" ",p)
print("\n✓ STEP 0 v2 COMPLETE — exact affine router frozen")
