# Python implementation of An Infinite Impulse Response (IIR) Hilbert Transformer


Hilbert transformers play a pivotal role in various signal processing applications, ranging from single-sideband communication systems to audio effects. The utilization of Infinite Impulse Response (IIR) implementations is particularly appealing due to their computational efficiency. This approach begins with the design of a half-band filter, illustrating how the pole locations evolve during the transformation process from a half-band filter to summed all-pass filters and ultimately to a Hilbert transformer filter. 

This repo is exclusively based on the work of Harris and colleagues: ([paper](http://www.aes.org/e-lib/browse.cfm?elib=15680)).


## Required Software

1. Python 3.8
   - numpy==1.22.2
   - matplotlib==3.7.3
   - scipy==1.10.1


## Installation

To clone this repo open your terminal and run:

`git clone https://github.com/MattiaDif/IIR-Hilbert-Transformer.git`


## Repo description

Inside IIR-HIlbert-Transformer

1. 'dsp' folder: it contains the IIRHilb.py file (inside hilbert folder) with the class implementation of the Hilbert transformer. The run.py script runs a filter design example.
2. requirements.txt: txt file with the python packages required.


## REFERENCE
If you use this repo, please cite:

"Di Florio, M., Iyer, V., Rajhans, A., Buccelli, S., & Chiappalone, M. (2022, July). Model-based online implementation of spike detection algorithms for neuroengineering applications. In 2022 44th Annual International Conference of the IEEE Engineering in Medicine & Biology Society (EMBC) (pp. 736-739). IEEE."
