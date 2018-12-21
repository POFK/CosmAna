#!/usr/bin/env python
# coding=utf-8
import libfftw as fft
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


N = 4
a = np.arange(N**3,dtype=np.complex64).reshape(N,N,N)
mpia = np.array_split(a,size)[rank]

fa = fft.forward(comm, mpia)

print fft.backward(comm,fa)/N**3
