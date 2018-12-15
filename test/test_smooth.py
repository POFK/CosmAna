#!/usr/bin/env python
# coding=utf-8
from CosmAna.core.utils import Utils
from mpi4py import MPI
import mpiunittest as unittest
import numpy as np


@unittest.skipIf(MPI.COMM_WORLD.Get_size() > 4, 'mpi-world-size>4')
class TestSmooth(unittest.TestCase):
    def tearDown(self):
        pass

    def setUp(self):
        Ng = 32
        L = 300.
        self.utils = Utils(L=L, Ng=Ng)
        data = np.zeros([Ng, Ng, Ng], dtype=np.float32)
        self.pos1 = [[Ng / 2, Ng / 2, Ng / 2]]
        self.pos2 = np.array([[Ng / 2, Ng / 2, Ng / 2],
                              [Ng / 2 + 4, Ng / 2 - 3, Ng / 2 + 1],
                              [2, 1, 1],
                              [-1, -1, Ng / 2]])
        self.data1 = data.copy()
        for i, j, k in self.pos1:
            self.data1[i, j, k] += 1
        self.data2 = data.copy()
        for i, j, k in self.pos2:
            self.data2[i, j, k] += 1

    @classmethod
    def tearDownClass(self):
        del self.comm

    @classmethod
    def setUpClass(self):
        self.comm = MPI.COMM_WORLD

    def GaussInRealSpace(self, x, pos, sigma):
        H = self.utils.H
        Ng = self.utils.Ng
        zeros = np.zeros([Ng, Ng, Ng], dtype=np.float32)
        x = np.arange(Ng, dtype=np.float32)[:, None, None] + zeros
        y = np.arange(Ng, dtype=np.float32)[None, :, None] + zeros
        z = np.arange(Ng, dtype=np.float32)[None, None, :] + zeros
        for i, j, k in pos:
            dx = x - i
            dy = y - j
            dz = z - k
            dx[dx > Ng / 2] -= Ng
            dx[dx < -Ng / 2] += Ng
            dy[dy > Ng / 2] -= Ng
            dy[dy < -Ng / 2] += Ng
            dz[dz > Ng / 2] -= Ng
            dz[dz < -Ng / 2] += Ng
            dis = dx**2. + dy**2. + dz**2.
            w = 1. / np.sqrt(2. * np.pi * sigma**2.) * \
                np.exp(-0.5 * dis * H**2. / (sigma**2.))
            w /= w.sum()
            zeros += w
        return zeros

    def test_smooth1(self):
        sigma = 20.
        data_mpi = np.array_split(self.data1, self.comm.size)[self.comm.rank]
        data_s = self.utils.Smooth(data_mpi, sigma)
        data_real = self.GaussInRealSpace(self.data1, self.pos1, sigma)
        data_real = np.array_split(data_real, self.comm.size)[self.comm.rank]
        if self.comm.size == 1:
            self.assertEqual(data_s.sum(), 1)
        else:
            data_sum = self.comm.reduce(data_s, root=0)
            if self.comm.rank == 0:
                self.assertEqual(data_sum.sum(), 1.)
        np.testing.assert_allclose(
            data_real, data_s, atol=1e-3 * data_real.max())

    def test_smooth2(self):
        sigma = 20.
        data_mpi = np.array_split(self.data2, self.comm.size)[self.comm.rank]
        data_s = self.utils.Smooth(data_mpi, sigma)
        data_real = self.GaussInRealSpace(self.data2, self.pos2, sigma)
        data_real = np.array_split(data_real, self.comm.size)[self.comm.rank]
        if self.comm.size == 1:
            self.assertEqual(data_s.sum(), 4)
        else:
            data_sum = self.comm.reduce(data_s, root=0)
            if self.comm.rank == 0:
                self.assertEqual(data_sum.sum(), 4.)
        np.testing.assert_allclose(
            data_real, data_s, atol=1e-3 * data_real.max())


if __name__ == '__main__':
    unittest.main()
