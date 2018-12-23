#!/usr/bin/env python
# coding=utf-8
from CosmAna import PS
from mpi4py import MPI
import mpiunittest as unittest
import numpy as np

IsShow = True
try:
    import matplotlib.pyplot as plt
except ImportError:
    IsShow = False

data_base = None
data_base = '/data/dell5/userdir/maotx/ICR/fiducial_ICR/output/snapdir_012/ana/'


@unittest.skipUnless(data_base is not None, 'no data base name')
class TestPS(unittest.TestCase):
    def tearDown(self):
        del self.utils

    def setUp(self):
        Ng = 256
        L = 500.
        self.utils = PS(L=L, Ng=Ng)

    @classmethod
    def tearDownClass(self):
        del self.comm

    @classmethod
    def setUpClass(self):
        self.comm = MPI.COMM_WORLD

    def test_autoPS1(self):
        data = np.fromfile(data_base + 'PCS_NG256_grid.bin', dtype=np.float32)
        data = data.reshape(self.utils.Ng, self.utils.Ng, self.utils.Ng)
        data = np.array_split(data, self.comm.size)[self.comm.rank]
        self.utils.AutoPS(data, dewo=4)
        self.utils.set_binsnum(50)
        self.utils.set_binstyle('log')
        ps = self.utils.Run_Getbin1d()
        if self.comm.rank == 0:
            ps_true = np.loadtxt(data_base + 'PS_auto.txt')
            np.testing.assert_allclose(ps, ps_true, rtol=1e-4)

    def test_autoPS2(self):
        data = np.fromfile(data_base + 'PCS_NG256_grid.bin', dtype=np.float32)
        data = data.reshape(self.utils.Ng, self.utils.Ng, self.utils.Ng)
        data = np.array_split(data, self.comm.size)[self.comm.rank]
        self.utils.AutoPS(data, dewo=4)
        self.utils.set_binsnum(50)
        self.utils.set_binstyle('linear')
        ps = self.utils.Run_Getbin1d()
        if self.comm.rank == 0 and IsShow:
            ps_true = np.loadtxt(data_base + 'PS_auto.txt')
            plt.plot(ps[:, 0], ps[:, 1], 'k-')
            plt.plot(ps_true[:, 0], ps_true[:, 1], 'r-')
            plt.xscale('log')
            plt.yscale('log')

    def test_CrossPS(self):
        data = np.fromfile(data_base + 'PCS_NG256_grid.bin', dtype=np.float32)
        data = data.reshape(self.utils.Ng, self.utils.Ng, self.utils.Ng)
        data = np.array_split(data, self.comm.size)[self.comm.rank]
        self.utils.CrossPS(data, data, dewo1=4, dewo2=4)
        self.utils.set_binsnum(50)
        self.utils.set_binstyle('log')
        ps = self.utils.Run_Getbin1d()
        if self.comm.rank == 0:
            ps_true = np.loadtxt(data_base + 'PS_auto.txt')
            np.testing.assert_allclose(ps, ps_true, rtol=1e-4)

    @unittest.skip('skip, test it later')
    def test_PCS(self):
        from CosmAna import PCS as Assign
        from CosmAna import ReadSnapshot
        comm = self.comm
        rank = self.comm.rank
        size = self.comm.size
        # ----------------------------------------
        Path = data_base[:-4] + 'snapshot_012.'
        rs = ReadSnapshot(Path)
        if rank == 0:
            print rs.Info
            print rs.Info.dtype
        Ng = self.utils.Ng
        Boxsize = self.utils.L
        Np = rs.Info['npartall'][0][1]
        redshift = rs.Info['redshift'][0]
        if redshift < 0:
            redshift = 0.
        self.utils.checkdir('./test/CosmAna')
        OutName = '/test/CosmAna/PCS_test.bin'
        Filenum = np.arange(rs.Filenum)
        Fnum_mpi = np.array_split(Filenum, size)
        # ----- load position --------------------
        Pos = []
        for i in Fnum_mpi[rank]:
            pos = rs.ReadPos(Filenum=i)
            Pos.append(pos['pos'])
        Pos = np.vstack(Pos)
        Pos[Pos >= Boxsize] -= Boxsize
        # --------------- CIC --------------------
        grid_cic = Assign(Pos, NG=Ng, L=int(Boxsize)).reshape(Ng, Ng, Ng)
        grid_cic *= (Ng**3. / Np)
        if rank == 0:
            grid_cic_all = np.zeros_like(grid_cic)
        else:
            grid_cic_all = None
        comm.Reduce(grid_cic, grid_cic_all, op=MPI.SUM, root=0)
        if rank == 0:
            grid_cic_all.tofile(OutName, format='f4')


if __name__ == '__main__':
    unittest.main()
    if IsShow:
        plt.show()
