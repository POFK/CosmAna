/*************************************************************************
	> File Name: grid.c
	> Author: mtx
	> Mail: maotianxiang@bao.ac.cn
	> Created Time: Wed 19 Oct 2016 10:10:28 PM CST
 ************************************************************************/
#include "allvars.h"


double* Griding_NGP(int N, int L, int SIZE, struct READ_POSITION* pos)
{
	int n;
	int i, j, k;
	int Index(int N, int x, int y, int z);
	float H = (float)L / (float)N;
	double *gridP = (double *)malloc(N * N * N * sizeof(double));
	memset(gridP, 0, sizeof(double) * N * N * N);  // initialization

	for(n = 0; n < SIZE; n++)
	{
		i = pos[n].x / H;
		j = pos[n].y / H;
		k = pos[n].z / H;
		gridP[Index(N, i, j, k)] += 1.;
	}
	return gridP;
}

double* Griding_CIC(int N, int L, int SIZE, struct READ_POSITION* pos)
{
	int n;
	int ibin, jbin, kbin, ibinm, ibinp, jbinm, jbinp, kbinm, kbinp;
	float hx, hy, hz, hx0, hy0, hz0, hxp, hxm, hyp, hym, hzp, hzm;
	float H = (float)L / (float)N;
//	double value = (N * N * N / (double)SIZE);
	double value = 1.;
	double *gridP = (double *)malloc(N * N * N * sizeof(double));
	memset(gridP, 0, sizeof(double) * N * N * N);  // initialization

	for(n = 0; n < SIZE; n++)
	{
		ibin = pos[n].x / H;
		jbin = pos[n].y / H;
		kbin = pos[n].z / H;
		if(ibin > (N - 1) || ibin < 0) printf("error: ibin exceeds boundary: %d,%d,%d,%d", n, ibin, jbin, kbin);

		if(jbin > (N - 1) || jbin < 0) printf("error: ibin exceeds boundary: %d,%d,%d,%d", n, ibin, jbin, kbin);

		if(kbin > (N - 1) || kbin < 0) printf("error: ibin exceeds boundary: %d,%d,%d,%d", n, ibin, jbin, kbin);

		hx = pos[n].x / H - ibin - 0.5;
		hy = pos[n].y / H - jbin - 0.5;
		hz = pos[n].z / H - kbin - 0.5;

		hx0 = 1. - fabs(hx);
		hy0 = 1. - fabs(hy);
		hz0 = 1. - fabs(hz);

		if(hx > 0)
		{
			hxp = hx;
			hxm = 0.;
		}
		else
		{
			hxp = 0.;
			hxm = -hx;
		}

		if(hy > 0)
		{
			hyp = hy;
			hym = 0.;
		}
		else
		{
			hyp = 0.;
			hym = -hy;
		}

		if(hz > 0)
		{
			hzp = hz;
			hzm = 0.;
		}
		else
		{
			hzp = 0.;
			hzm = -hz;
		}

		ibinm = (ibin - 1 + N) % N;
		ibinp = (ibin + 1 + N) % N;
		jbinm = (jbin - 1 + N) % N;
		jbinp = (jbin + 1 + N) % N;
		kbinm = (kbin - 1 + N) % N;
		kbinp = (kbin + 1 + N) % N;

		gridP[Index(N, ibinm, jbinm, kbinm)] += hxm * hym * hzm * value;
		gridP[Index(N, ibinm, jbinm, kbin)] += hxm * hym * hz0 * value;
		gridP[Index(N, ibinm, jbinm, kbinp)] += hxm * hym * hzp * value;
		gridP[Index(N, ibinm, jbin , kbinm)] += hxm * hy0 * hzm * value;
		gridP[Index(N, ibinm, jbin , kbin)] += hxm * hy0 * hz0 * value;
		gridP[Index(N, ibinm, jbin , kbinp)] += hxm * hy0 * hzp * value;
		gridP[Index(N, ibinm, jbinp, kbinm)] += hxm * hyp * hzm * value;
		gridP[Index(N, ibinm, jbinp, kbin)] += hxm * hyp * hz0 * value;
		gridP[Index(N, ibinm, jbinp, kbinp)] += hxm * hyp * hzp * value;

		gridP[Index(N, ibin , jbinm, kbinm)] += hx0 * hym * hzm * value;
		gridP[Index(N, ibin , jbinm, kbin)] += hx0 * hym * hz0 * value;
		gridP[Index(N, ibin , jbinm, kbinp)] += hx0 * hym * hzp * value;
		gridP[Index(N, ibin , jbin , kbinm)] += hx0 * hy0 * hzm * value;
		gridP[Index(N, ibin , jbin , kbin)] += hx0 * hy0 * hz0 * value;
		gridP[Index(N, ibin , jbin , kbinp)] += hx0 * hy0 * hzp * value;
		gridP[Index(N, ibin , jbinp, kbinm)] += hx0 * hyp * hzm * value;
		gridP[Index(N, ibin , jbinp, kbin)] += hx0 * hyp * hz0 * value;
		gridP[Index(N, ibin , jbinp, kbinp)] += hx0 * hyp * hzp * value;

		gridP[Index(N, ibinp, jbinm, kbinm)] += hxp * hym * hzm * value;
		gridP[Index(N, ibinp, jbinm, kbin)] += hxp * hym * hz0 * value;
		gridP[Index(N, ibinp, jbinm, kbinp)] += hxp * hym * hzp * value;
		gridP[Index(N, ibinp, jbin , kbinm)] += hxp * hy0 * hzm * value;
		gridP[Index(N, ibinp, jbin , kbin)] += hxp * hy0 * hz0 * value;
		gridP[Index(N, ibinp, jbin , kbinp)] += hxp * hy0 * hzp * value;
		gridP[Index(N, ibinp, jbinp, kbinm)] += hxp * hyp * hzm * value;
		gridP[Index(N, ibinp, jbinp, kbin)] += hxp * hyp * hz0 * value;
		gridP[Index(N, ibinp, jbinp, kbinp)] += hxp * hyp * hzp * value;
	}

	return gridP;
}


int Index(int N, int x, int y, int z)
{
	return x * N * N + y * N + z;
}

int *InverIndexK(int N, int n)
{
	/*used to make index of fftw*/
	int *InIndex = (int *)malloc(sizeof(int) * 3);
	memset(InIndex, 0, sizeof(int) * 3);
	int cn2 = N / 2 + 1;
	InIndex[0] = n / N / cn2;
	InIndex[1] = n % (N * cn2) / cn2;
	InIndex[2] = n % (N * cn2) % cn2;
	return InIndex;
}

