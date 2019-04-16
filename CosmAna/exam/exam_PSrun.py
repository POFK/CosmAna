#!/usr/bin/env python
# coding=utf-8
""" It is a old version!!"""
import sys
sys.path.append("..")
from CosmAna.core.PS import PS
import numpy as np
from CosmAna.read_snapshot import ReadSnapshot
from mpi4py import MPI
from CosmAna.Griding.grid import CIC
from CosmAna.MPI_IO.MPI_IO import MPI_IO
#import matplotlib.pyplot as plt

#-------------------------------------------------------------------------
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
#----------------------------------------
OutDir = './output/'
NP_flag = 128
Path = '/data/dell1/userdir/maotx/output/gadget/ics/test_%d/ics.' % NP_flag
#Path = '/data/dell1/userdir/maotx/output/gadget/output/test256/snapdir_000/snapshot_000.'
rs = ReadSnapshot(Path)
if rank == 0:
    print rs.Info
    print rs.Info.dtype
Ng = 512
Boxsize = 300
Np = rs.Info['npartall'][0][1]
redshift = rs.Info['redshift'][0]
if redshift < 0:
    redshift=0.
#OutName = 'IC_Np128_RS%.0f_' % redshift
OutName = 'test_Np%d_RS%.0f_Ng%d' % (NP_flag,redshift, Ng)
Filenum = np.arange(rs.Filenum)
Fnum_mpi = np.array_split(Filenum, size)
#----- load position --------------------
Pos = []
for i in Fnum_mpi[rank]:
    pos = rs.ReadPos(Filenum=i)
    Pos.append(pos['pos'])
Pos = np.vstack(Pos)
Pos[Pos>=300.0]-=300.
#--------------- CIC --------------------
grid_cic = CIC(Pos, NG=Ng, L=Boxsize).reshape(Ng, Ng, Ng)
grid_cic *= (Ng**3. / Np)
if rank == 0:
    grid_cic_all = np.zeros_like(grid_cic)
else:
    grid_cic_all = None
comm.Reduce(grid_cic, grid_cic_all, op=MPI.SUM, root=0)
if rank == 0:
    grid_cic_all.tofile('/tmp/maotx/grid.bin', format='f4')
#--------------- PS ---------------------
#================================================================================
utils = PS(bins=50, Ng=Ng, L=float(Boxsize), window1='cic', window2='')
Path1 = '/tmp/maotx/grid.bin'
mpi_io = MPI_IO(comm=utils.comm, MPI=utils.MPI)
mpi_io.datar = np.empty(
    shape=[utils.N * utils.N * utils.N / utils.size],
    dtype=np.float32)
#================================================================================
mpi_io.MPI_READ(path=Path1)
utils.delta_x1 = mpi_io.datar.copy()
utils.AutoPS()
PS_result = utils.Run_Getbin1d()
if utils.rank == 0:
    print PS_result
#   np.savetxt(OutDir+OutName+'PS_TEST.txt', PS_result)
    np.savetxt(OutDir+OutName+'PS.txt', PS_result)
    print utils.N
    print utils.L
    print utils.H
    print utils.shape

