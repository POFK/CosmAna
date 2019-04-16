# coding: utf-8
from CosmAna import Main # must import this line first
import numpy as np

Ng = 32 # grids number per side
L = 300. # boxsize
sigma = 15.


"""
float:
"""
CA = Main(L=L, Ng=Ng, format='f4') # if float, format='f4'; else if double, format='f8'
#==================== read data =============================
path = '/tmp/test.bin'
data = CA.fromfile(path=path, shape=[Ng, Ng, Ng], dtype=np.float32)
data = data.reshape([Ng/CA.size,Ng,Ng])
#==================== smoothing =============================
datas = CA.Smooth(data.astype(np.complex64), sigma)
#==================== save data =============================
CA.tofile(datas, path='/tmp/test_fs.bin')
#====================== check ===============================
if CA.rank == 0:
    import matplotlib.pyplot as plt
    s = np.fromfile('/tmp/test_fs.bin', dtype=np.float32)
    s = s.reshape(Ng,Ng,Ng)
    plt.imshow(s.mean(axis=0))
    plt.show()


"""
double:
"""
CA = Main(L=L, Ng=Ng, format='f8') # if float, format='f4'; else if double, format='f8'
#==================== read data =============================
path = '/tmp/test_double.bin'
data = CA.fromfile(path=path, shape=[Ng, Ng, Ng], dtype=np.float64)
data = data.reshape([Ng/CA.size,Ng,Ng])
#==================== smoothing =============================
datas = CA.Smooth(data.astype(np.complex128), sigma)
#==================== save data =============================
CA.tofile(datas, path='/tmp/test_ds.bin')
#====================== check ===============================
if CA.rank == 0:
    import matplotlib.pyplot as plt
    s = np.fromfile('/tmp/test_ds.bin', dtype=np.float64)
    s = s.reshape(Ng,Ng,Ng)
    plt.imshow(s.mean(axis=0))
    plt.show()
