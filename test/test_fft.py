#!/usr/bin/env python
# coding=utf-8
from CosmAna import fft 
from mpi4py import MPI
import mpiunittest as unittest
import numpy as np
import sys

@unittest.skipIf(MPI.COMM_WORLD.Get_size() > 4, 'mpi-world-size>4')
class TestSmooth(unittest.TestCase):

    def tearDown(self):
        pass

    def setUp(self):
        self.fft = fft()
        N = 8
#       datar = np.random.rand(N,N,N).astype(np.float32) + 2
#       datai = np.random.rand(N,N,N).astype(np.float32) + 2
        datar = np.arange(N**3).reshape(N,N,N).astype(np.float32)
        datai = datar + 3

        self.data = datar + 1j*datai

    @classmethod
    def tearDownClass(self):
        pass

    @classmethod
    def setUpClass(self):
        self.comm = MPI.COMM_WORLD

    def test_fft(self):
        data = np.array_split(self.data, self.comm.size)
        datak = self.fft.fft(data[self.comm.rank])

        datak_np = np.fft.fftn(self.data)
        datak_np = np.array_split(datak_np, self.comm.size)
    #   if self.comm.rank == 0:
    #       print datak_np[self.comm.rank][0,0], '\n', datak[0,0]
        np.testing.assert_allclose(datak,datak_np[self.comm.rank],rtol=1e-5)

    def test_ifft(self):
        data = np.array_split(self.data, self.comm.size)
        datak = self.fft.ifft(data[self.comm.rank])

        datak_np = np.fft.ifftn(self.data)
        datak_np = np.array_split(datak_np, self.comm.size)
        np.testing.assert_allclose(datak,datak_np[self.comm.rank],rtol=1e-5)

if __name__ == '__main__':
    unittest.main()

