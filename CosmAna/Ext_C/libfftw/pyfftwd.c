/*************************************************************************
	> File Name: Pylib.c
	> Author: mtx
	> Mail: maotianxiang@bao.ac.cn
	> Created Time: Tue 30 May 2017 03:45:30 PM CST
 ************************************************************************/
#include<stdio.h>
#include<string.h>
#include<memory.h>
#include"mpi.h"
#include"fftw3-mpi.h"
void DPyFFTW_FORWARD(MPI_Comm comm, int N, double *data_in_real, double *data_in_imag, double *data_out_real, double *data_out_imag)
{
	/*There is a normalization of N**3*/
	int my_rank, i, j, k;
	/* fftw mpi */
	const ptrdiff_t N0 = N, N1 = N, N2 = N;
	fftw_plan plan;
	fftw_complex *data_in, *data_out;
	ptrdiff_t alloc_local, local_n0, local_0_start ;
	MPI_Comm_rank(comm, &my_rank);
	//	fftwf_mpi_init();
	/* get local data size and allocate */
	alloc_local = fftw_mpi_local_size_3d(N0, N1, N2, comm,
	                                      &local_n0, &local_0_start);
	data_in = fftw_alloc_complex(alloc_local);
	memset(data_in, 0., sizeof(fftw_complex)*alloc_local);
	data_out = fftw_alloc_complex(alloc_local);
	memset(data_out, 0., sizeof(fftw_complex)*alloc_local);
	/* create plan for in-place forward DFT */
	plan = fftw_mpi_plan_dft_3d(N0, N1, N2, data_in, data_out, comm,
	                             FFTW_FORWARD, FFTW_ESTIMATE);
	/* initialize data to some function my_function(x,y) */
	for(i = 0; i < local_n0; i++) for(j = 0; j < N1; j++) for(k = 0; k < N2; k++)
			{
				data_in[i * N1 * N2 + j * N2 + k][0] = data_in_real[i * N1 * N2 + j * N2 + k];
				data_in[i * N1 * N2 + j * N2 + k][1] = data_in_imag[i * N1 * N2 + j * N2 + k];
			}
	/* compute transforms, in-place, as many times as desired */
	fftw_execute(plan);
	for(i = 0; i < local_n0; i++) for(j = 0; j < N1; j++) for(k = 0; k < N2; k++)
			{
				data_out_real[i * N1 * N2 + j * N2 + k] = data_out[i * N1 * N2 + j * N2 + k][0]  ;
				data_out_imag[i * N1 * N2 + j * N2 + k] = data_out[i * N1 * N2 + j * N2 + k][1]  ;
			}
	fftw_destroy_plan(plan);
	fftw_free(data_in);
	fftw_free(data_out);
}
void DPyFFTW_BACKWARD(MPI_Comm comm, int N, double *data_in_real, double *data_in_imag, double *data_out_real, double *data_out_imag)
{
	/*There is a normalization of N**3*/
	int my_rank, i, j, k;
	/* fftw mpi */
	const ptrdiff_t N0 = N, N1 = N, N2 = N;
	fftw_plan iplan;
	fftw_complex *data_in, *data_out;
	ptrdiff_t alloc_local, local_n0, local_0_start ;
	MPI_Comm_rank(comm, &my_rank);
	//	fftw_mpi_init();
	/* get local data size and allocate */
	alloc_local = fftw_mpi_local_size_3d(N0, N1, N2, comm,
	                                      &local_n0, &local_0_start);
	data_in = fftw_alloc_complex(alloc_local);
	memset(data_in, 0., sizeof(fftw_complex)*alloc_local);
	data_out = fftw_alloc_complex(alloc_local);
	memset(data_out, 0., sizeof(fftw_complex)*alloc_local);
	/* create plan for in-place forward DFT */
	iplan = fftw_mpi_plan_dft_3d(N0, N1, N2, data_in, data_out, comm,
	                              FFTW_BACKWARD, FFTW_ESTIMATE);
	/* initialize data to some function my_function(x,y) */
	for(i = 0; i < local_n0; i++) for(j = 0; j < N1; j++) for(k = 0; k < N2; k++)
			{
				data_in[i * N1 * N2 + j * N2 + k][0] = data_in_real[i * N1 * N2 + j * N2 + k];
				data_in[i * N1 * N2 + j * N2 + k][1] = data_in_imag[i * N1 * N2 + j * N2 + k];
			}
	/* compute transforms, in-place, as many times as desired */
	fftw_execute(iplan);
	for(i = 0; i < local_n0; i++) for(j = 0; j < N1; j++) for(k = 0; k < N2; k++)
			{
				data_out_real[i * N1 * N2 + j * N2 + k] = data_out[i * N1 * N2 + j * N2 + k][0]  ;
				data_out_imag[i * N1 * N2 + j * N2 + k] = data_out[i * N1 * N2 + j * N2 + k][1]  ;
			}
	fftw_destroy_plan(iplan);
	fftw_free(data_in);
	fftw_free(data_out);
}
