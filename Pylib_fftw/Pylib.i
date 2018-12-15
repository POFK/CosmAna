%module Pylib
%{
    #define SWIG_FILE_WITH_INIT
    #include <mpi.h>
    #include <stdio.h>
    #include "Pylib.h"
%}
/* mpi support */
%include mpi4py/mpi4py.i
%mpi4py_typemap(Comm, MPI_Comm);
/* numpy support */
%include "numpy.i"
%init %{
    import_array();
%}
%apply (float *IN_ARRAY1, int DIM1) {(float *data_in_real, int size_in1)}
%apply (float *IN_ARRAY1, int DIM1) {(float *data_in_imag, int size_in2)}
%apply (float *INPLACE_ARRAY1, int DIM1) {(float *data_out_real, int size_out1)}
%apply (float *INPLACE_ARRAY1, int DIM1) {(float *data_out_imag, int size_out2)}

%include "Pylib.h"
