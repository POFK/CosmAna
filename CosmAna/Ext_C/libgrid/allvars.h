/*************************************************************************
	> File Name: head.h
	> Author: mtx
	> Mail: maotianxiang@bao.ac.cn
	> Created Time: Mon 07 Nov 2016 05:33:51 PM CST
 ************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <memory.h>

#define PI   3.141592653
#define kf   (2.*PI/L)

extern int Index(int,int,int,int);
extern int *InverIndexK(int,int);

struct READ_POSITION
{
	float x;
	float y;
	float z;
};
