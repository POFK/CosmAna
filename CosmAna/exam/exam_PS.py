#!/usr/bin/env python
# coding=utf-8
from CosmAna import Main
import numpy as np
import os

CA = Main(Ng=512, L=1000., format='f4')
CA.set_binstyle('linear')
CA.set_binsnum(50)
CA.set_binskrange(kmin=2e-2, kmax=0.6)

fp = '/nfs/P100/gadget/Indra/PCS_field_128/ICS0/6_7_0_snap012_NG512_grid_S0.bin'
OutDir = '/tmp/result/PS/'
CA.checkdir(OutDir)
#------------------- load data ------------------------------
ic = CA.fromfile(path=fp, shape=[CA.Ng, CA.Ng, CA.Ng], dtype=np.float32)
ic = ic.reshape(CA.Ng/CA.size, CA.Ng, CA.Ng) - 1.
#------------------ auto-power spectrum ---------------------
ic = ic.astype(np.complex64)
CA.AutoPS(ic, dewo=0)
PS = CA.Run_Getbin1d()
if CA.rank == 0:
    np.savetxt(os.path.join(OutDir,'PS.txt'), PS)
#----------------- cross-power spectrum ---------------------
CA.CrossPS(ic, ic)
PS = CA.Run_Getbin1d()
if CA.rank == 0:
    np.savetxt(os.path.join(outdir,'cro_PS.txt'), PS)

