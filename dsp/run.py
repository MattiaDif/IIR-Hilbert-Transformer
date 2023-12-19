from hilbert.IIRHilb import AllPass as ap

warp   = True
filter = ap(20000, 200, 80, f2=8000, warping=warp)