#!/usr/bin/env python
# coding=utf-8

import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import numpy

os.environ["CC"] = 'mpicc' # set CC compiler
os.environ["LDSHARED"] = 'mpicc -shared' # set linker_so
#============================ Extension C =======================================
FFTW_INCL  =  '/home/mtx/local/fftw-3.3.5/include'
FFTW_LIBS  =  '/home/mtx/local/fftw-3.3.5/lib'
MPI_INCL = '/home/mtx/local/mpich-3.2/include'
INCL = []
INCL.append(FFTW_INCL)
INCL.append(MPI_INCL)
INCL.append(numpy.get_include())



ext_modules = []

ext_modules.append(
    Extension("libfftw",
              sources=["libfftw.pyx", "pyfftwf.c"],
              include_dirs=INCL,
              library_dirs=[FFTW_LIBS],
              libraries=['fftw3f_mpi', 'fftw3f'],
             )
                  )

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
)


