from mpi4py.libmpi cimport *
# declare the interface to the C code
cdef extern void PyFFTW_FORWARD(MPI_Comm comm, int N, float *data_in_real, float *data_in_imag, float *data_out_real, float *data_out_imag);
cdef extern void PyFFTW_BACKWARD(MPI_Comm comm, int N, float *data_in_real, float *data_in_imag, float *data_out_real, float *data_out_imag);
