#!/usr/bin/env python
# coding=utf-8
import libfftw as fft
import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

#--------------------------------------------------------------------------------
N = 4
a = np.arange(N**3,dtype=np.complex64).reshape(N,N,N)
mpia = np.array_split(a,size)[rank]

fa = fft.forwardF(comm, mpia)

#assert np.allclose(np.fft.fftn(a.reshape(N,N,N)), fa)

npifft = np.fft.ifftn(np.fft.fftn(a.reshape(N,N,N)))
#assert np.allclose(fft.backwardF(comm,fa)/N**3,npifft) 
print(rank, fft.backwardF(comm, fa)/N**3)
#--------------------------------------------------------------------------------
N = 4
a = np.arange(N**3,dtype=np.complex128).reshape(N,N,N)
mpia = np.array_split(a,size)[rank]

fa = fft.forwardD(comm, mpia)

#assert np.allclose(np.fft.fftn(a.reshape(N,N,N)), fa)

npifft = np.fft.ifftn(np.fft.fftn(a.reshape(N,N,N)))
#assert np.allclose(fft.backwardD(comm,fa)/N**3,npifft) 
#--------------------------------------------------------------------------------
print(rank, fft.backwardD(comm, fa)/N**3)
