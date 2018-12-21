/*************************************************************************
	> File Name: pcs.c
	> Author: mtx
	> Mail: maotianxiang@bao.ac.cn
	> Created Time: 2018年04月26日 星期四 15时53分21秒
 ************************************************************************/
#include "allvars.h"

float weight(float s)
{
	float w;

	if(fabs(s) < 1 && fabs(s) >= 0)
		w = 1. / 6.*(4 - 6 * s * s + 3 * pow(fabs(s), 3));
	else if(fabs(s) >= 1 && fabs(s) < 2)
		w = 1. / 6.* pow(2 - fabs(s), 3);
	else
		w = 0;

	return w;
}

float GetWeight(float H, int ibin, int jbin, int kbin, struct READ_POSITION pos)
{
	float wi, wj, wk, si, sj, sk, w;
	si = ibin + 0.5 - pos.x / H;
	sj = jbin + 0.5 - pos.y / H;
	sk = kbin + 0.5 - pos.z / H;
	wi = weight(si);
	wj = weight(sj);
	wk = weight(sk);
	w = wi * wj * wk;
	return w;
}

double* Griding_PCS(int N, int L, int SIZE, struct READ_POSITION* pos)
{
	int ibin, jbin, kbin, i, j, k, ii, jj, kk;
	double value = 1.;
	float H = (float)L / (float)N;
	float w;
	double *gridP = (double *)malloc(N * N * N * sizeof(double));
	memset(gridP, 0, sizeof(double) * N * N * N); // initialization
	long n;
	double posx, posy, posz;

	for(n = 0; n < SIZE; n++)
	{
		posx = pos[n].x;
		posy = pos[n].y;
		posz = pos[n].z;

		ibin = posx / H;
		jbin = posy / H;
		kbin = posz / H;

		for(i = ibin - 2; i <= ibin + 2; i++)
			for(j = jbin - 2; j <= jbin + 2; j++)
				for(k = kbin - 2; k <= kbin + 2; k++)
				{
					w = GetWeight(H, i, j, k, pos[n]);

					if(i < 0)
						ii = i + N;
					else if(i >= N)
						ii = i - N;
					else
						ii = i;

					if(j < 0)
						jj = j + N;
					else if(j >= N)
						jj = j - N;
					else
						jj = j;

					if(k < 0)
						kk = k + N;
					else if(k >= N)
						kk = k - N;
					else
						kk = k;

					gridP[Index(N, ii, jj, kk)] += w * value;
				}
	}
    return gridP;
	//free(gridP);
}
