#!/usr/bin/env python
# coding=utf-8
import numpy as np
from grid import NGP, CIC
from read_snapshot import ReadSnapshot

Path = '/data/dell1/userdir/maotx/output/gadget/output/L300N128_0/snapdir_003/snapshot_003.'
rs = ReadSnapshot(Path)

Pos = []
for i in np.arange(rs.filenum):
    pos = rs.ReadPos(Filenum=i)
    Pos.append(pos['pos'])
Pos = np.vstack(Pos)


grid_cic = CIC(Pos, NG=64, L=300).reshape(64,64,64)
grid_ngp = NGP(Pos, NG=64, L=300).reshape(64,64,64)

grid_ngp *= (64**3./128**3.)
grid_cic *= (64**3./128**3.)
