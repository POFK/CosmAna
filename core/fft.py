#!/usr/bin/env python
# coding=utf-8
from CosmAna.Pylib_fftw import Pylib
'''!!! Pylib_fftw must be imported first !!!'''
import numpy as np
from Base import Base


class fft(Base):
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
        shape = data.shape
        N = shape[-1]
        mpi_shape = N * N * N / self.size
        assert np.prod(shape) == mpi_shape, \
            'shape error! the input data should have shape [N/mpi_size,N,N]'
        FFTW_inr = np.empty(shape=[mpi_shape], dtype=np.float32)
        FFTW_ini = np.empty(shape=[mpi_shape], dtype=np.float32)
        FFTW_outr = np.empty(shape=[mpi_shape], dtype=np.float32)
        FFTW_outi = np.empty(shape=[mpi_shape], dtype=np.float32)
        FFTW_inr[:] = data.real.reshape(-1)
        FFTW_ini[:] = data.imag.reshape(-1)
        Pylib.PyFFTW_FORWARD(
            self.comm,
            N,
            FFTW_inr,
            FFTW_ini,
            FFTW_outr,
            FFTW_outi)
        datak = (FFTW_outr + 1j * FFTW_outi).reshape([N / self.size, N, N])
        return datak

    def ifft(self, datak):
        '''
        backward fftw
        datak: 3-D complex64 numpy array, wigh shape [N/size,N,N]
        '''
        shape = datak.shape
        N = shape[-1]
        mpi_shape = N * N * N / self.size
        assert np.prod(shape) == mpi_shape, \
            'shape error! the input data should have shape [N/mpi_size,N,N]'
        FFTW_inr = np.empty(shape=[mpi_shape], dtype=np.float32)
        FFTW_ini = np.empty(shape=[mpi_shape], dtype=np.float32)
        FFTW_outr = np.empty(shape=[mpi_shape], dtype=np.float32)
        FFTW_outi = np.empty(shape=[mpi_shape], dtype=np.float32)
        FFTW_inr[:] = datak.real.reshape(-1)
        FFTW_ini[:] = datak.imag.reshape(-1)
        Pylib.PyFFTW_BACKWARD(
            self.comm,
            N,
            FFTW_inr,
            FFTW_ini,
            FFTW_outr,
            FFTW_outi)
        data = (FFTW_outr + 1j * FFTW_outi).reshape([N / self.size, N, N])
        return data / N**3.
