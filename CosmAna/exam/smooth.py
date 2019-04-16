#!/usr/bin/env python
# coding=utf-8
"""It is an old version code!"""
from CosmAna import Pylib
from CosmAna import PS
import numpy as np
from CosmAna import ReadSnapshot
from CosmAna import PCS as Assigment
from CosmAna import MPI_IO
from smooth import Smooth
import os

def checkdir(dirpath):
    isExists = os.path.exists(dirpath)
    if not isExists:
        os.makedirs(dirpath)

#-------------------------------------------------------------------------
OutDir = '/data/dell1/userdir/maotx/ICRdata/ICRcheck/check/test0503/'
Path = '/data/dell1/userdir/maotx/ICRdata/ICRcheck/snapdir_012/snapshot_012.'
grid_name = 'grid_cic.bin'
Boxsize = 500
Ng = 512
wm = ''
rs = ReadSnapshot(Path)
utils = PS(bins=20, Ng=Ng, L=float(Boxsize), window1='', window2='')
sfunc = Smooth(bins=20, Ng=Ng, L=float(Boxsize))

if utils.rank == 0:
    print rs.Info
    print rs.Info.dtype
    checkdir(OutDir)

Np = rs.Info['npartall'][0][1]
redshift = rs.Info['redshift'][0]
if redshift < 0:
    redshift=0.
OutName = 'newPCS_RS%.0f_Ng%d' % (redshift, Ng)
Filenum = np.arange(rs.Filenum)
Fnum_mpi = np.array_split(Filenum, utils.size)
#----- load position --------------------
Pos = []
for i in Fnum_mpi[utils.rank]:
    pos = rs.ReadPos(Filenum=i)
    Pos.append(pos['pos'])
    utils.mybarrier()
Pos = np.vstack(Pos)
Pos[Pos>=Boxsize]-=float(Boxsize)
#--------------- CIC --------------------
grid = Assigment(Pos, NG=Ng, L=Boxsize).reshape(Ng, Ng, Ng)
grid *= (Ng**3. / Np)
if utils.rank == 0:
    grid_all = np.zeros_like(grid)
else:
    grid_all = None
utils.comm.Reduce(grid, grid_all, op=utils.MPI.SUM, root=0)
if utils.rank == 0:
    grid_all.tofile(OutDir+grid_name, format='f4')
    print 'saved grid data'
#================================================================================
Path1 = OutDir + grid_name 
mpi_io = MPI_IO(comm=utils.comm, MPI=utils.MPI)
mpi_io.datar = np.empty(
    shape=[utils.N * utils.N * utils.N / utils.size],
    dtype=np.float32)
#================================================================================
mpi_io.MPI_READ(path=Path1)
utils.delta_x1 = mpi_io.datar.copy()
#------------ deconcolve ----------------
sfunc.delta_x1 = utils.delta_x1.copy()
de_x = sfunc.DeConv(rank=4)
utils.delta_x1 = de_x
mpi_io.dataw = utils.delta_x1
mpi_io.MPI_WRITE(path=Path[:-4]+'_deconv.bin')
#----------------- PS -------------------
utils.AutoPS()
PS_result = utils.Run_Getbin1d()
if utils.rank == 0:
    print PS_result
    np.savetxt(OutDir+OutName+'PS.txt', PS_result)
    print utils.N
    print utils.L
    print utils.H
    print utils.shape


