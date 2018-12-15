/*************************************************************************
	> File Name: Pylib.h
	> Author: mtx
	> Mail: maotianxiang@bao.ac.cn
	> Created Time: Mon 29 May 2017 03:01:22 PM CST
 ************************************************************************/

void PyFFTW_FORWARD(MPI_Comm comm, int N, float *data_in_real, int size_in1, float *data_in_imag, int size_in2, float *data_out_real, int size_out1, float *data_out_imag, int size_out2);
void PyFFTW_BACKWARD(MPI_Comm comm, int N, float *data_in_real, int size_in1, float *data_in_imag, int size_in2, float *data_out_real, int size_out1, float *data_out_imag, int size_out2);
