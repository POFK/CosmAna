import cython

# import both numpy and the Cython declarations for numpy
cimport numpy as np
import numpy as np
from mpi4py.libmpi cimport *
cimport mpi4py.MPI as MPI
cimport cpyfftw

cdef extern from "mpi_compat.h": pass

@cython.boundscheck(False)
@cython.wraparound(False)
def forward(MPI.Comm comm not None, i_arr):
    """
    i_arr: 3-D input array, complex64
    """
    cdef MPI_Comm c_comm = comm.ob_mpi
    cdef int size, rank, N
    MPI_Comm_size(c_comm, &size)
    MPI_Comm_rank(c_comm, &rank)
    assert i_arr.ndim == 3
    assert i_arr.shape[0] * size == i_arr.shape[1]
    assert i_arr.shape[1] == i_arr.shape[2]
    N = i_arr.shape[2]
    irarr = np.ascontiguousarray(i_arr.real.reshape(-1))
    iiarr = np.ascontiguousarray(i_arr.imag.reshape(-1))
    orarr = np.zeros_like(irarr)
    oiarr = np.zeros_like(iiarr)

    cdef float[::1] c_irarr = irarr
    cdef float[::1] c_iiarr = iiarr
    cdef float[::1] c_orarr = orarr
    cdef float[::1] c_oiarr = oiarr

    cpyfftw.PyFFTW_FORWARD(c_comm, 
                           N, 
                           &c_irarr[0], 
                           &c_iiarr[0], 
                           &c_orarr[0], 
                           &c_oiarr[0])
    return np.reshape(orarr + 1.j*oiarr, i_arr.shape)


@cython.boundscheck(False)
@cython.wraparound(False)
def backward(MPI.Comm comm not None, i_arr):
    """
    i_arr: 3-D input array, complex64
    """
    cdef MPI_Comm c_comm = comm.ob_mpi
    cdef int size, rank, N
    MPI_Comm_size(c_comm, &size)
    MPI_Comm_rank(c_comm, &rank)
    assert i_arr.ndim == 3
    assert i_arr.shape[0] * size == i_arr.shape[1]
    assert i_arr.shape[1] == i_arr.shape[2]
    N = i_arr.shape[2]
    irarr = np.ascontiguousarray(i_arr.real.reshape(-1))
    iiarr = np.ascontiguousarray(i_arr.imag.reshape(-1))
    orarr = np.zeros_like(irarr)
    oiarr = np.zeros_like(iiarr)

    cdef float[::1] c_irarr = irarr
    cdef float[::1] c_iiarr = iiarr
    cdef float[::1] c_orarr = orarr
    cdef float[::1] c_oiarr = oiarr

    cpyfftw.PyFFTW_BACKWARD(c_comm, 
                           N, 
                           &c_irarr[0], 
                           &c_iiarr[0], 
                           &c_orarr[0], 
                           &c_oiarr[0])
    return np.reshape(orarr + 1.j*oiarr, i_arr.shape)
