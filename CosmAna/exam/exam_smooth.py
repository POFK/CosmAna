# coding: utf-8
from CosmAna import Main # must import this line first
import numpy as np

Ng = 32 # grids number per side
L = 300. # boxsize
CA = Main(L=L, Ng=Ng)

#==================== read data =============================
path = '/tmp/test.bin'
data = CA.fromfile(path=path, shape=[Ng, Ng, Ng], dtype=np.float32)
data = data.reshape([Ng/CA.size,Ng,Ng])
#==================== smoothing =============================
sigma = 15.
datas = CA.Smooth(data, sigma)
#==================== save data =============================
CA.tofile(datas, path='/tmp/test_s.bin')
#====================== check ===============================
if CA.rank == 0:
    import matplotlib.pyplot as plt
    s = np.fromfile('/tmp/test_s.bin', dtype=np.float32)
    s = s.reshape(Ng,Ng,Ng)
    plt.imshow(s.mean(axis=0))
    plt.show()
