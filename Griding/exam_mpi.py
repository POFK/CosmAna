#!/usr/bin/env python
# coding=utf-8
import numpy as np
from grid import NGP, CIC
from read_snapshot import ReadSnapshot
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

Path = '/data/dell1/userdir/maotx/output/gadget/output/L300N128_0/snapdir_003/snapshot_003.'
#Path = '/data/dell1/userdir/maotx/output/gadget/output/testenv/snapdir_003/snapshot_003.'
rs = ReadSnapshot(Path)
if rank == 0:
    print rs.Info
    print rs.Info.dtype
#--------------------------------------------------------------------------------
Ng = 512
Boxsize = 300
Np = rs.Info['npartall'][0][1]
redshift = rs.Info['redshift'][0]
if redshift < 0:
    redshift=0.
Filenum = np.arange(rs.Filenum)
Fnum_mpi = np.array_split(Filenum, size)
#--------------------------------------------------------------------------------
Pos = []
for i in Fnum_mpi[rank]:
    pos = rs.ReadPos(Filenum=i)
    Pos.append(pos['pos'])
Pos = np.vstack(Pos)

grid_cic = CIC(Pos, NG=Ng, L=Boxsize).reshape(Ng,Ng,Ng)
grid_ngp = NGP(Pos, NG=Ng, L=Boxsize).reshape(Ng,Ng,Ng)
grid_cic *= (Ng**3. / Np)
grid_ngp *= (Ng**3. / Np)

if rank == 0:
    grid_cic_all = np.zeros_like(grid_cic)
    grid_ngp_all = np.zeros_like(grid_ngp)
else:
    grid_cic_all = None
    grid_ngp_all = None
comm.Reduce(grid_cic, grid_cic_all, op=MPI.SUM, root=0)
comm.Reduce(grid_ngp, grid_ngp_all, op=MPI.SUM, root=0)

if __name__ == '__main__':
    if rank == 0:
        cic_test = np.fromfile('../PK/output/cic/grid_64_L300N128_z00.bin', dtype=np.float32).reshape(64,64,64)
        ngp_test = np.fromfile('../PK/output/ngp/grid_64_L300N128_z00.bin', dtype=np.float32).reshape(64,64,64)
        print np.allclose(cic_test, grid_cic_all)
        print np.allclose(ngp_test, grid_ngp_all)
