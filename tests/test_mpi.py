#!/usr/bin/env python
# coding=utf-8
import mpiunittest as unittest
from mpi4py import MPI
import numpy as np

class TestMpi(unittest.TestCase):

    def tearDown(self):
        pass

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    @classmethod
    def setUpClass(self):
        self.comm = MPI.COMM_WORLD

    def testmpi(self):
        rank = self.comm.rank
        size = self.comm.size
        data = np.array(rank, dtype=np.int32)
        if rank == 0:
            data_mpitem = np.zeros([1], dtype=np.int32)
        else:
            data_mpitem = None
        self.comm.Reduce([data, MPI.INT], data_mpitem, op=MPI.SUM, root=0)
        if rank == 0 and size > 1 :
            self.assertEqual(data_mpitem[0], (size-1)*size/2)


if __name__ == '__main__':
    unittest.main()
