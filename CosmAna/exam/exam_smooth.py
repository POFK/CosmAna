# coding: utf-8
from CosmAna import Utils # must import this line first
from mpi4py import MPI
import numpy as np
from CosmAna import MPI_IO 

Ng = 32 # grids number per side
L = 300. # boxsize
utils = Utils(L=L, Ng=Ng)
mpi_io = MPI_IO(comm=utils.comm, MPI=utils.MPI)

#==================== read data =============================
path = '/tmp/test.bin'
mpi_io.datar = np.empty(shape=[Ng * Ng * Ng / utils.size], dtype=np.float32)
mpi_io.MPI_READ(path=path)
data = mpi_io.datar.reshape([Ng/utils.size,Ng,Ng])
#==================== smoothing =============================
sigma = 15.
datas = utils.Smooth(data, sigma)
#==================== save data =============================
mpi_io.dataw = datas.copy(order='C')
mpi_io.MPI_WRITE('/tmp/test_s.bin')
#====================== check ===============================
if utils.rank == 0:
    import matplotlib.pyplot as plt
    s = np.fromfile('/tmp/test_s.bin', dtype=np.float32)
    s = s.reshape(Ng,Ng,Ng)
    plt.imshow(s.mean(axis=0))
    plt.show()
