#!/usr/bin/env python
# coding=utf-8
from mpi4py import MPI
import numpy as np
import os
from Base import Base
from CosmAna.MPI_IO.MPI_IO import fromfile as _fromfile
from CosmAna.MPI_IO.MPI_IO import tofile as _tofile

class Ana(Base):

    def __init__(self, L=300., Ng=128, **kwargs):
        '''
        Ng: number of grids, int
        L: Boxsize, float
        '''
        super(Ana, self).__init__(L=L, Ng=Ng, **kwargs)
        self.MPI = MPI
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.rank
        self.size = self.comm.size
        # ----------------------------------------
        self.Ng = Ng
        self.L = L
        self.rank_print('=' * 80)
        self.rank_print('parameters:')
        self.rank_print('N: %d, L: %f' % (self.Ng, self.L))
        self.rank_print('=' * 80)
        # ----------------------------------------
        self.Kf = 2 * np.pi / self.L
        self.H = float(self.L) / self.Ng
        self.fn = np.fft.fftfreq(self.Ng, 1. / self.Ng).astype(np.float32)
        # fn: 0,1,2,...,511,-512,-511,-510,...,-2,-1
        self.mpi_fn = np.array_split(self.fn, self.size)
        self.shape = self.Ng * self.Ng * self.Ng / self.size
        self.k_ind = (self.mpi_fn[self.rank][:, None, None]**2.
                  + self.fn[None, :, None]**2.
                  + self.fn[None, None, :]**2)**(0.5)

    def mybarrier(self):
        return self.comm.barrier()

    def rank_print(self, str=''):
        if self.rank == 0:
            print str

    def checkdir(self, dirpath):
        if self.rank == 0:
            isExists = os.path.exists(dirpath)
            if not isExists:
                os.makedirs(dirpath)
        self.mybarrier()
        
    def fromfile(self, path, shape=[], dtype=np.float32):
        """
        :shape:3D shape before splited by MPI size.
        """
        return _fromfile(path, self.comm, self.MPI, shape=shape, dtype=dtype)
    
    def tofile(self, data, path):
        return _tofile(data, path, self.comm, self.MPI)

if __name__ == '__main__':
    s = Ana()
    pass
