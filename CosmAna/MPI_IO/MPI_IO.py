#!/usr/bin/env python
# coding=utf-8
import numpy as np


class MPI_IO(object):

    def __init__(self, comm, MPI):
        self.comm = comm
        self.MPI = MPI
        self.size = comm.Get_size()

    def MPI_READ(self, path=''):
        rmode = self.MPI.MODE_RDONLY
        fp = self.MPI.File.Open(self.comm, path, rmode)
#       self.datar = np.empty([N * N * N / self.size], dtype=dtype)
        offset = self.comm.Get_rank() * self.datar.nbytes
        fp.Read_at_all(offset, self.datar)
        fp.Close()

    def MPI_WRITE(self, path=''):
        amode = self.MPI.MODE_WRONLY | self.MPI.MODE_CREATE
        fp = self.MPI.File.Open(self.comm, path, amode)
        offset = self.comm.Get_rank() * self.dataw.nbytes
        fp.Write_at_all(offset, self.dataw)
        fp.Close()

def fromfile(path, comm, MPI, shape=[], dtype=np.float32):
    """MPI read routine for binary file.

    :path: TODO
    :comm: TODO
    :MPI: TODO
    :shape: [x,y,z]
    :dtype: TODO
    :returns: TODO

    """
    mpi_io = MPI_IO(comm=comm, MPI=MPI)
    l = np.array(shape).prod()
    assert shape[0]%mpi_io.size==0, \
            "processes number: %d, shape: %s"%(mpi_io.size, shape)
    mpi_io.datar = np.empty([l/mpi_io.size], dtype=dtype)
    mpi_io.MPI_READ(path=path)
    return mpi_io.datar.copy()

def tofile(data, path, comm, MPI):
    """MPI write routine for binary file.

    :data: TODO
    :path: TODO
    :comm: TODO
    :MPI: TODO
    :shape: [x,y,z]
    :dtype: TODO
    :returns: TODO

    """
    mpi_io = MPI_IO(comm=comm, MPI=MPI)
    mpi_io.dataw = data.copy(order='C')
    return mpi_io.MPI_WRITE(path=path)



if __name__ == '__main__':
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    data = np.arange(12, dtype=np.float32)
    data = np.array_split(data, size)[rank]
    tofile(data, '/tmp/test.bin', comm, MPI)
    if rank == 0:
        s = np.fromfile('/tmp/test.bin', dtype=np.float32, count=12)
        print s
    datar = fromfile('/tmp/test.bin', comm, MPI, shape=[12], dtype=np.float32)
    print rank, datar
