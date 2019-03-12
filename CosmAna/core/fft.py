#!/usr/bin/env python
# coding=utf-8
from CosmAna.Ext_C import libfftw
'''!!! libfftw must be imported first !!!'''
import numpy as np
from Base import Base


class fft(Base):

    libfftw = libfftw

    def __init__(self, *args, **kwargs):
        super(fft, self).__init__(*args, **kwargs)
        try:
            self.comm
        except AttributeError:
            from mpi4py import MPI
            self.MPI = MPI
            self.comm = MPI.COMM_WORLD
            self.rank = self.comm.rank
            self.size = self.comm.size

    def fft(self, data):
        '''
        forward fftw
        data: 3-D complex64 numpy array, wigh shape [N/size,N,N]
        '''
        if data.dtype != np.complex64:
            self.rank_print("!Warning: the input should be 3-D complex64 numpy array for fft!\n")
            data = data.astype(np.complex64)

        return self.libfftw.forward(self.comm, data)

    def ifft(self, datak):
        '''
        backward fftw
        datak: 3-D complex64 numpy array, wigh shape [N/size,N,N]
        '''
        if datak.dtype != np.complex64:
            self.rank_print("!Warning: the input should be 3-D complex64 numpy array for ifft!\n")
            datak = datak.astype(np.complex64)
        N = datak.shape[-1]
        return self.libfftw.backward(self.comm, datak)/N**3.
