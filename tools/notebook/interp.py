"""Junta as interpretações em markdown (INTERP) usadas por build_nb.py."""
from interp_a import INTERP as A
from interp_b import INTERP as B
from interp_c import INTERP as C
from interp_d import INTERP as D
from interp_e import INTERP as E
from interp_f import CALLOUTS

INTERP = {**A, **B, **C, **E, "[[INTERP-CALLOUT-9]]": ""}
for key, value in INTERP.items():
    for inner_key, inner_value in D.items():
        value = value.replace(inner_key, inner_value.strip("\n"))
    if key in CALLOUTS:
        value = value.rstrip("\n") + "\n\n" + CALLOUTS[key] + "\n"
    INTERP[key] = value
