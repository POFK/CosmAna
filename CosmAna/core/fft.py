#!/usr/bin/env python
# coding=utf-8
from CosmAna.Ext_C import libfftw
'''!!! libfftw must be imported first !!!'''
import numpy as np
from Analysis import Ana


class fft(Ana):

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

        # ----------------------------------------
        self.format = kwargs.get('format', 'f4')
        self.rank_print('data format: %s'%self.format)
        self._format = {'f4': np.complex64, 'f8': np.complex128}
        if self.format == 'f4':
            self.rank_print("fft precision: float!")
            self.forward = self.libfftw.forwardF
            self.backward = self.libfftw.backwardF
        elif self.format == 'f8':
            self.rank_print("fft precision: double!")
            self.forward = self.libfftw.forwardD
            self.backward = self.libfftw.backwardD
        else:
            raise ValueError('fft data format error: %s, please input f4 or f8!'%(self.format))
        # ----------------------------------------
        dt = {'f4': np.float32, 'f8': np.float64}
        self.Kf = 2 * np.pi / self.L
        self.H = float(self.L) / self.Ng
        self.fn = np.fft.fftfreq(self.Ng, 1. / self.Ng).astype(dt[self.format])
        # fn: 0,1,2,...,511,-512,-511,-510,...,-2,-1
        self.mpi_fn = np.array_split(self.fn, self.size)
        self.shape = self.Ng * self.Ng * self.Ng / self.size
        self.k_ind = (self.mpi_fn[self.rank][:, None, None]**2.
                  + self.fn[None, :, None]**2.
                  + self.fn[None, None, :]**2)**(0.5)

    def fft(self, data):
        '''
        forward fftw
        data: 3-D numpy array, wigh shape [N/size,N,N]
        '''
        if data.dtype != self._format[self.format]:
            self.rank_print("!Warning: the input should be 3-D '%s' numpy array for fft, but get %s\n"%(self.format, data.dtype))
            data = data.astype(self._format[self.format])

        return self.forward(self.comm, data)

    def ifft(self, datak):
        '''
        backward fftw
        datak: 3-D numpy array, wigh shape [N/size,N,N]
        '''
        if datak.dtype != self._format[self.format]:
            self.rank_print("!Warning: the input should be 3-D '%s' numpy array for fft, but get %s\n"%(self.format, datak.dtype))
            datak = datak.astype(self._format[self.format])
        N = datak.shape[-1]
        return self.backward(self.comm, datak)/N**3.
