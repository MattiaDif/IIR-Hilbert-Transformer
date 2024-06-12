#!/mnt/d/GitHub/IIR-Hilbert-Transformer/dsp/linux_venv/bin/python3.8

from hilbert.IIRHilb import AllPass as ap

warp   = False
filter = ap(20000, 200, 80, warping=warp)