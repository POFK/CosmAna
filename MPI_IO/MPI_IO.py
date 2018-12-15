#!/usr/bin/env python
# coding=utf-8
import numpy as np


class MPI_IO():

    def __init__(self, comm, MPI):
        self.comm = comm
        self.MPI = MPI
        self.size = comm.Get_size()

    def MPI_READ(self, path=''):
        rmode = self.MPI.MODE_RDONLY
        fp = self.MPI.File.Open(self.comm, path, rmode)
#       self.data = np.empty([N * N * N / self.size], dtype=dtype)
        offset = self.comm.Get_rank() * self.datar.nbytes
        fp.Read_at_all(offset, self.datar)
        fp.Close()

    def MPI_WRITE(self, path=''):
        amode = self.MPI.MODE_WRONLY | self.MPI.MODE_CREATE
        fp = self.MPI.File.Open(self.comm, path, amode)
        offset = self.comm.Get_rank() * self.dataw.nbytes
        fp.Write_at_all(offset, self.dataw)
        fp.Close()


if __name__ == '__main__':
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
#   from test import MPI_IO
    mpi_io = MPI_IO(comm=comm, MPI=MPI)
    mpi_io.dataw = np.arange(10, dtype=np.int32)
    mpi_io.MPI_WRITE(path='./test.bin')
    mpi_io.datar = np.empty([2, 5], dtype=np.int32)
    mpi_io.MPI_READ(path='./test.bin')
    if rank == 0:
        print [size, mpi_io.datar]
