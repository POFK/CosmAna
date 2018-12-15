/*************************************************************************
	> File Name: Pylib.c
	> Author: mtx
	> Mail: maotianxiang@bao.ac.cn
	> Created Time: Tue 30 May 2017 03:45:30 PM CST
 ************************************************************************/
#include<stdio.h>
#include<string.h>
#include<memory.h>
#include"fftw3-mpi.h"
#include"mpi.h"
void PyFFTW_FORWARD(MPI_Comm comm, int N, float *data_in_real, int size_in1, float *data_in_imag, int size_in2, float *data_out_real, int size_out1, float *data_out_imag, int size_out2)
{
	/*There is a normalization of N**3*/
	int my_rank, i, j, k;
	/* fftw mpi */
	const ptrdiff_t N0 = N, N1 = N, N2 = N;
	fftwf_plan plan;
	fftwf_complex *data_in, *data_out;
	ptrdiff_t alloc_local, local_n0, local_0_start ;
	MPI_Comm_rank(comm, &my_rank);
	//	fftwf_mpi_init();
	/* get local data size and allocate */
	alloc_local = fftwf_mpi_local_size_3d(N0, N1, N2, comm,
	                                      &local_n0, &local_0_start);
	data_in = fftwf_alloc_complex(alloc_local);
	memset(data_in, 0., sizeof(fftwf_complex)*alloc_local);
	data_out = fftwf_alloc_complex(alloc_local);
	memset(data_out, 0., sizeof(fftwf_complex)*alloc_local);
	/* create plan for in-place forward DFT */
	plan = fftwf_mpi_plan_dft_3d(N0, N1, N2, data_in, data_out, comm,
	                             FFTW_FORWARD, FFTW_ESTIMATE);
	/* initialize data to some function my_function(x,y) */
	for(i = 0; i < local_n0; i++) for(j = 0; j < N1; j++) for(k = 0; k < N2; k++)
			{
				data_in[i * N1 * N2 + j * N2 + k][0] = data_in_real[i * N1 * N2 + j * N2 + k];
				data_in[i * N1 * N2 + j * N2 + k][1] = data_in_imag[i * N1 * N2 + j * N2 + k];
			}
	/* compute transforms, in-place, as many times as desired */
	fftwf_execute(plan);
	for(i = 0; i < local_n0; i++) for(j = 0; j < N1; j++) for(k = 0; k < N2; k++)
			{
				data_out_real[i * N1 * N2 + j * N2 + k] = data_out[i * N1 * N2 + j * N2 + k][0]  ;
				data_out_imag[i * N1 * N2 + j * N2 + k] = data_out[i * N1 * N2 + j * N2 + k][1]  ;
			}
	fftwf_destroy_plan(plan);
	fftwf_free(data_in);
	fftwf_free(data_out);
}
void PyFFTW_BACKWARD(MPI_Comm comm, int N, float *data_in_real, int size_in1, float *data_in_imag, int size_in2, float *data_out_real, int size_out1, float *data_out_imag, int size_out2)
{
	/*There is a normalization of N**3*/
	int my_rank, i, j, k;
	/* fftw mpi */
	const ptrdiff_t N0 = N, N1 = N, N2 = N;
	fftwf_plan iplan;
	fftwf_complex *data_in, *data_out;
	ptrdiff_t alloc_local, local_n0, local_0_start ;
	MPI_Comm_rank(comm, &my_rank);
	//	fftwf_mpi_init();
	/* get local data size and allocate */
	alloc_local = fftwf_mpi_local_size_3d(N0, N1, N2, comm,
	                                      &local_n0, &local_0_start);
	data_in = fftwf_alloc_complex(alloc_local);
	memset(data_in, 0., sizeof(fftwf_complex)*alloc_local);
	data_out = fftwf_alloc_complex(alloc_local);
	memset(data_out, 0., sizeof(fftwf_complex)*alloc_local);
	/* create plan for in-place forward DFT */
	iplan = fftwf_mpi_plan_dft_3d(N0, N1, N2, data_in, data_out, comm,
	                              FFTW_BACKWARD, FFTW_ESTIMATE);
	/* initialize data to some function my_function(x,y) */
	for(i = 0; i < local_n0; i++) for(j = 0; j < N1; j++) for(k = 0; k < N2; k++)
			{
				data_in[i * N1 * N2 + j * N2 + k][0] = data_in_real[i * N1 * N2 + j * N2 + k];
				data_in[i * N1 * N2 + j * N2 + k][1] = data_in_imag[i * N1 * N2 + j * N2 + k];
			}
	/* compute transforms, in-place, as many times as desired */
	fftwf_execute(iplan);
	for(i = 0; i < local_n0; i++) for(j = 0; j < N1; j++) for(k = 0; k < N2; k++)
			{
				data_out_real[i * N1 * N2 + j * N2 + k] = data_out[i * N1 * N2 + j * N2 + k][0]  ;
				data_out_imag[i * N1 * N2 + j * N2 + k] = data_out[i * N1 * N2 + j * N2 + k][1]  ;
			}
	fftwf_destroy_plan(iplan);
	fftwf_free(data_in);
	fftwf_free(data_out);
}
