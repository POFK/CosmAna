#!/usr/bin/env python
# coding=utf-8
from CosmAna.core.utils import Utils
from mpi4py import MPI
import mpiunittest as unittest
import numpy as np


@unittest.skipIf(MPI.COMM_WORLD.Get_size() > 4, 'mpi-world-size>4')
class TestPS(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
