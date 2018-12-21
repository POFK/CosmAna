#!/usr/bin/env python
# coding=utf-8
from fft import fft
'''!!! fft must be imported first !!!'''
import numpy as np
from Analysis import Ana


class Utils(Ana, fft):
    def __init__(self, L=300., Ng=128, **kwargs):
        super(Utils, self).__init__(L=L, Ng=Ng, **kwargs)

    def _GaussianWindow(self, sigma):
        window = np.exp(-0.5 * (self.k_ind * self.Kf) ** 2. * sigma**2.)
        return window

    def _DeWindow(self):
        window = (np.sinc(1. / self.Ng * self.mpi_fn[self.rank][:, None, None])
                  * np.sinc(1. / self.Ng * self.fn[None, :, None])
                  * np.sinc(1. / self.Ng * self.fn[None, None, :]))
        return window

    def convolve_fft(self, a, b, use_fft=True):
        '''
        b: window function in Fourier space, real type
        use_fft: whether the input a array should be Fourier transfered.
        '''
        if a.dtype != np.complex64:
            a = a.astype(np.complex64)
        if use_fft:
            a = self.fft(a)
        return self.ifft(a * b).real

    def Smooth(self, data, sigma):
        window = self._GaussianWindow(sigma)
        return self.convolve_fft(data, window)


if __name__ == '__main__':
    utils = Utils()
