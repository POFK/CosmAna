.PHONY : default
default: clean build 

EXEC 	= libgrid.so
OBJS   	= libgrid.o libPCS.o allvars.o
INCL 	= allvars.h
CC 		= gcc
PYTHON 	= python

PYTHON_CONFIG = ${PYTHON} ../python-config
MPI4PY_INCLUDE = ${shell ${PYTHON} -c 'import mpi4py; print( mpi4py.get_include() )'}
CFLAGS = -fPIC ${shell ${PYTHON_CONFIG} --includes}
LDFLAGS = -shared ${shell ${PYTHON_CONFIG} --libs}

.PHONY: build
build: ${EXEC}
${EXEC}: $(OBJS)
	${CC} ${CFLAGS} -I${MPI4PY_INCLUDE} -o $@ $^ ${LDFLAGS}

${OBJS}: ${INCL}

.PHONY: clean
clean:
	${RM} -r ${OBJS} ${EXEC} *.pyc 

