#!/usr/bin/env python
# coding=utf-8
from CosmAna import Utils
import numpy as np
'''!!! fft must be imported first !!!'''


class PS(Utils):
    def __init__(self, L=300., Ng=128, **kwargs):
        '''window: choosed from cic and pcs'''
        super(PS, self).__init__(L=L, Ng=Ng, **kwargs)

    def AutoPS(self, delta, dewo=0):
        '''
        dewo: the order of window function that will be deconvolved,
        set 2 if cic, 4 if pcs and 0 if no deconvolution.
        return: None
        '''
        deltak = self.fft(delta)
        if dewo != 0:
            window_name = {1: 'NGP', 2: 'CIC', 4: 'PCS'}
            window = self._DeWindow()
            self.rank_print('deconvolve %s window' % window_name[dewo])
            deltak /= window ** dewo
        self.pk = np.abs(deltak)**2.

    def CrossPS(self, delta1, delta2, dewo1=0, dewo2=0):
        deltak1 = self.fft(delta1)
        if dewo1 != 0:
            window_name = {1: 'NGP', 2: 'CIC', 4: 'PCS'}
            window = self._DeWindow()
            self.rank_print('deconvolve %s window' % window_name[dewo1])
            deltak1 /= window ** dewo1
        deltak2 = self.fft(delta2)
        if dewo2 != 0:
            window_name = {1: 'NGP', 2: 'CIC', 4: 'PCS'}
            window = self._DeWindow()
            self.rank_print('deconvolve %s window' % window_name[dewo2])
            deltak2 /= window ** dewo2
        self.pk = deltak1.real * deltak2.real + deltak1.imag * deltak2.imag

    def set_binsnum(self, num):
        self.bins = num

    def set_binstyle(self, style=''):
        if style == 'log':
            self.binspace = self.logspace_wrapper(np.logspace)
        elif style == 'linear':
            self.binspace = np.linspace
        else:
            raise ValueError('binstyle should be "log" or "linear".')

    def logspace_wrapper(self, func):
        def wrapper(*args, **kwargs):
            a = args[0]
            b = args[1]
            args = args[2:]
            return func(np.log10(a), np.log10(b), *args, **kwargs)
        return wrapper

    def Run_Getbin1d(self):
        MPI_n, MPI_Pk, MPI_k = self.get_bin1d()
        if self.rank == 0:
            MPI_n[MPI_n == 0] = 1
            MPI_k *= self.Kf / MPI_n
            MPI_Pk *= self.L**3 / self.Ng**6 / MPI_n
            return np.c_[MPI_k, MPI_Pk, MPI_n]

    def get_bin1d(self):
        try: 
            bin = self.binspace(1, self.Ng/2, self.bins+1, endpoint=True)
        except AttributeError:
            self.rank_print('can not find parameter binstyle, \
                            use default logspace...')
            bin = np.logspace(np.log10(1), np.log10(self.Ng/2), 
                              self.bins+1, endpoint=True)
        n_bin = []
        Pk_bin = []
        k_bin = []
        for i in range(self.bins):
            bool = (bin[i] <= self.k_ind) * (self.k_ind < bin[i+1])
            n_bin.append(bool.sum())
            k_bin.append(self.k_ind[bool].astype(np.float64).sum())
            Pk_bin.append(self.pk[bool].astype(np.float64).sum())
        n_bin = np.array(n_bin)
        Pk_bin = np.array(Pk_bin)
        k_bin = np.array(k_bin)
        MPI_n = self.comm.reduce(n_bin, root=0)
        MPI_Pk = self.comm.reduce(Pk_bin, root=0)
        MPI_k = self.comm.reduce(k_bin, root=0)
        '''
        if utils.rank == 0:
            MPI_n[MPI_n == 0] = 1
            MPI_k *= utils.Kf / MPI_n
            MPI_Pk *= utils.L**3 / utils.N**6 / MPI_n
        '''
        return MPI_n, MPI_Pk, MPI_k


