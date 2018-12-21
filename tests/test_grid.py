#!/usr/bin/env python
# coding=utf-8
from mpi4py import MPI
import mpiunittest as unittest
import numpy as np


@unittest.skipIf(MPI.COMM_WORLD.Get_size() > 4, 'mpi-world-size>4')
class TestGrid(unittest.TestCase):

    def tearDown(self):
        pass

    def setUp(self):
        self.Ng = 4
        self.Boxsize = 4
        pos = [
            [1., 2., 3.], [0.3, 0., 0.], [3.9, 0.2, 2.6], [0., 0., 0.],
            [0., 1., 0.], [4.0, 4., 4.], [2.6, 3.9, 2.2], [1.3, 2.5, 0.7],
        ]
        pos = np.array(pos, dtype=np.float32)
        self.pos = np.array_split(pos, self.comm.size)[self.comm.rank]

    @classmethod
    def tearDownClass(self):
        pass

    @classmethod
    def setUpClass(self):
        self.comm = MPI.COMM_WORLD

    def weight_PCS(self, s):
        w = np.zeros_like(s)
        bool_1 = np.abs(s) < 1.
        bool_2 = (np.abs(s) >= 1) * (np.abs(s) < 2)
        s1 = s[bool_1]
        s2 = s[bool_2]
        w[bool_1] += 1. / 6. * (4 - 6 * s1 * s1 + 3 * np.abs(s1)**3.)
        w[bool_2] += 1. / 6. * (2 - np.abs(s2))**3.
        return w

    def weight_CIC(self, s):
        w = np.zeros_like(s)
        bool = np.abs(s) < 1.0
        w[bool] += 1 - np.abs(s[bool])
        return w

    def GetWeight(self, gx, gy, gz, pos, window_func):
        wx = window_func(gx - pos[0])
        wy = window_func(gy - pos[1])
        wz = window_func(gz - pos[2])
        w = wx * wy * wz
        return w

    def CIC(self):
        zeros = np.zeros(
            [self.Ng + 2, self.Ng + 2, self.Ng + 2], dtype=np.float32)
        gpos = np.arange(-1, self.Ng + 1) + 0.5
        gx = gpos[:, None, None] + zeros
        gy = gpos[None, :, None] + zeros
        gz = gpos[None, None, :] + zeros
        for i in xrange(self.pos.shape[0]):
            weight = self.GetWeight(gx, gy, gz, self.pos[i], self.weight_CIC)
            zeros += weight
        zeros[1, :, :] += zeros[-1, :, :]
        zeros[-2, :, :] += zeros[0, :, :]
        zeros[:, 1, :] += zeros[:, -1, :]
        zeros[:, -2, :] += zeros[:, 0, :]
        zeros[:, :, 1] += zeros[:, :, -1]
        zeros[:, :, -2] += zeros[:, :, 0]
        grid = zeros[1:-1, 1:-1, 1:-1]
        assert grid.sum() == self.pos.shape[0]
        assert grid.shape == (self.Ng, self.Ng, self.Ng)
        return grid

    def PCS(self):
        zeros = np.zeros(
            [self.Ng + 4, self.Ng + 4, self.Ng + 4], dtype=np.float32)
        gpos = np.arange(-2, self.Ng + 2) + 0.5
        gx = gpos[:, None, None] + zeros
        gy = gpos[None, :, None] + zeros
        gz = gpos[None, None, :] + zeros
        for i in xrange(self.pos.shape[0]):
            weight = self.GetWeight(gx, gy, gz, self.pos[i], self.weight_PCS)
            zeros += weight
        zeros[2:4, :, :] += zeros[-2:, :, :]
        zeros[-4:-2, :, :] += zeros[0:2, :, :]
        zeros[:, 2:4, :] += zeros[:, -2:, :]
        zeros[:, -4:-2, :] += zeros[:, 0:2, :]
        zeros[:, :, 2:4] += zeros[:, :, -2:]
        zeros[:, :, -4:-2] += zeros[:, :, 0:2]
        grid = zeros[2:-2, 2:-2, 2:-2]
        assert grid.sum() == self.pos.shape[0]
        assert grid.shape == (self.Ng, self.Ng, self.Ng)
        return grid

    def test1(self):
        self.CIC()
        self.PCS()

    def testGrid_CIC(self):
        from CosmAna import CIC as Assign
        self.pos[self.pos == self.Boxsize] -= self.Boxsize
        grid = Assign(self.pos,
                      NG=self.Ng,
                      L=self.Boxsize)
        grid = grid.reshape(self.Ng, self.Ng, self.Ng)
        self.assertEqual(grid.sum(), self.pos.shape[0])
        grid_true = self.CIC()
        self.assertTrue(np.allclose(grid, grid_true))

    def testGrid_PCS(self):
        from CosmAna import PCS as Assign
        self.pos[self.pos == self.Boxsize] -= self.Boxsize
        grid = Assign(self.pos,
                      NG=self.Ng,
                      L=self.Boxsize)
        grid = grid.reshape(self.Ng, self.Ng, self.Ng)
        self.assertTrue(np.allclose(grid.sum(), self.pos.shape[0], rtol=1e-06))
        grid_true = self.PCS()
        self.assertTrue(np.allclose(grid, grid_true, rtol=1e-06))


if __name__ == '__main__':
    unittest.main()
