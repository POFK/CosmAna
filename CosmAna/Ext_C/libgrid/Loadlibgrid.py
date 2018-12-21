#!/usr/bin/env python
# coding=utf-8
from ctypes import *
import numpy as np
import numpy.ctypeslib as npct
import os


class Pos(Structure):
    _fields_ = [('x', c_float), ('y', c_float), ('z', c_float)]

# load the library, using numpy mechanisms
_libdir = os.path.dirname(__file__)
if _libdir == '':
    _libdir = './'
_libpath = os.path.join(_libdir, "libgrid.so")
libcd = CDLL(_libpath)

# setup the return typs and argument types
libcd.Griding_NGP.restype = POINTER(c_double)
libcd.Griding_NGP.argtypes = [
    c_int,
    c_int,
    c_int,
    POINTER(Pos),
]

libcd.Griding_CIC.restype = POINTER(c_double)
libcd.Griding_CIC.argtypes = [
    c_int,
    c_int,
    c_int,
    POINTER(Pos),
]

libcd.Griding_PCS.restype = POINTER(c_double)
libcd.Griding_PCS.argtypes = [
    c_int,
    c_int,
    c_int,
    POINTER(Pos),
]

def NGP(pos, NG=32, L=300):
    ''' shape of pos is [-1, 3], conrresponding to [x, y, z]'''
    if not pos.flags['C_CONTIGUOUS']:
        pos = np.ascontiguous(pos, dtype=pos.dtype)
    pos_ctypes_ptr = cast(pos.ctypes.data, POINTER(Pos))
    Gp = libcd.Griding_NGP(NG, L, len(pos), pos_ctypes_ptr)
    Grid = np.fromiter(Gp, dtype=np.float64, count=NG**3).astype(np.float32)
    return Grid


def CIC(pos, NG=32, L=300):
    ''' shape of pos is [-1, 3], conrresponding to [x, y, z]'''
    if not pos.flags['C_CONTIGUOUS']:
        pos = np.ascontiguous(pos, dtype=pos.dtype)
    pos_ctypes_ptr = cast(pos.ctypes.data, POINTER(Pos))
    Gp = libcd.Griding_CIC(NG, L, len(pos), pos_ctypes_ptr)
    Grid = np.fromiter(Gp, dtype=np.float64, count=NG**3).astype(np.float32)
    return Grid

def PCS(pos, NG=32, L=300):
    ''' shape of pos is [-1, 3], conrresponding to [x, y, z]'''
    if not pos.flags['C_CONTIGUOUS']:
        pos = np.ascontiguous(pos, dtype=pos.dtype)
    pos_ctypes_ptr = cast(pos.ctypes.data, POINTER(Pos))
    Gp = libcd.Griding_PCS(NG, L, len(pos), pos_ctypes_ptr)
    Grid = np.fromiter(Gp, dtype=np.float64, count=NG**3).astype(np.float32)
    return Grid



if __name__ == '__main__':
    #   x = np.arange(32**3*3, dtype=np.float32)
    x = np.linspace(1, 299, 256 * 3, dtype=np.float32).reshape([-1, 3])
    NG = 128
    grid_pcs = PCS(x, NG=NG, L=300).reshape(NG,NG,NG)
    grid_cic = CIC(x, NG=NG, L=300).reshape(NG,NG,NG)

    import matplotlib.pyplot as plt
    plt.subplot(121)
    plt.imshow(grid_pcs.mean(axis=0))
    plt.subplot(122)
    plt.imshow(grid_cic.mean(axis=0))
    plt.show()
