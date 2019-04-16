from mpi4py.libmpi cimport *
# declare the interface to the C code (float)
cdef extern void FPyFFTW_FORWARD(MPI_Comm comm, int N, float *data_in_real, float *data_in_imag, float *data_out_real, float *data_out_imag);
cdef extern void FPyFFTW_BACKWARD(MPI_Comm comm, int N, float *data_in_real, float *data_in_imag, float *data_out_real, float *data_out_imag);

# declare the interface to the C code (double)
cdef extern void DPyFFTW_FORWARD(MPI_Comm comm, int N, double *data_in_real, double *data_in_imag, double *data_out_real, double *data_out_imag);
cdef extern void DPyFFTW_BACKWARD(MPI_Comm comm, int N, double *data_in_real, double *data_in_imag, double *data_out_real, double *data_out_imag);
