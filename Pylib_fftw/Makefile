CODE="python"
PYTHON 	= python
#================================================================================
FFTW_INCL  =  -I/home/mtx/local/fftw-3.3.5/include
FFTW_LIBS  =  -L/home/mtx/local/fftw-3.3.5/lib -lfftw3f_mpi -lfftw3f
#================================================================================
PYTHON_CONFIG = ${PYTHON} ../python-config
MPI4PY_INCL = ${shell ${PYTHON} -c 'import mpi4py; print( mpi4py.get_include() )'}
NUMPY_INCL = ${shell ${PYTHON} -c 'import numpy; print( numpy.get_include() )'}
PYTHON_INCL = ${shell ${PYTHON_CONFIG} --includes}

ifeq ($(CODE),"python")
EXEC   	=  	_Pylib.so
OBJS   	=  	Pylib.o Pylib_wrap.o
OPTIMIZE= 	-Wall -O -g -fPIC -shared
endif

CC     	= 	mpicc
INCL  	=  	$(FFTW_INCL) $(PYTHON_INCL) $(MPICHINCL) -I$(MPI4PY_INCL) -I$(NUMPY_INCL)
CFLAGS 	=   $(OPTIMIZE) $(OPT) $(INCL)
LIBS   	=   -lm $(FFTW_LIBS)
#****************************************
$(EXEC): $(OBJS) 
	$(CC) $(OBJS) $(LIBS) $(CFLAGS) -o $(EXEC)  

Pylib_wrap.c: Pylib.i
	swig -I$(MPI4PY_INCL) -python Pylib.i

clean:
	rm -f $(OBJS) $(EXEC) Pylib_wrap.c *.pyc Pylib.py
#================================================================================
