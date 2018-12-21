#!/usr/bin/env python
# coding=utf-8
import os
import glob
import codecs
from setuptools import setup, Extension
from distutils.util import convert_path
from distutils import sysconfig
#from Cython.Distutils import build_ext
from Cython.Build import cythonize


os.environ["CC"] = 'mpicc'  # set CC compiler
os.environ["LDSHARED"] = 'mpicc -shared'  # set linker_so
FFTW_INCL = '/home/mtx/local/fftw-3.3.5/include'
FFTW_LIBS = '/home/mtx/local/fftw-3.3.5/lib'
MPI_INCL = '/home/mtx/local/mpich-3.2/include'
INCL = []
# ================================================================================


def read(fname):
    '''
    read description from README.rst
    '''
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


def find_packages(base_path):
    base_path = convert_path(base_path)
    found = []
    for root, dirs, files in os.walk(base_path, followlinks=True):
        dirs[:] = [
            d for d in dirs if d[0] != '.' and d not in (
                'ez_setup', '__pycache__')]
        relpath = os.path.relpath(root, base_path)
        parent = relpath.replace(os.sep, '.').lstrip('.')
        if relpath != '.' and parent not in found:
            # foo.bar package but no foo package, skip
            continue
        for dir in dirs:
            if os.path.isfile(os.path.join(root, dir, '__init__.py')):
                package = '.'.join((parent, dir)) if parent else dir
                found.append(package)
    return found


def find_extc(base_path):
    file = {}
    for i in glob.iglob(base_path + '*/*.c'):
        dir, name = i.split(base_path)[1].split('/')
        if dir not in file.keys():
            file[dir] = []
        if name == 'libfftw.c':
            continue
        file[dir].append(base_path + dir + '/' + name)

    for i in glob.iglob(base_path + '*/*.pyx'):
        dir, name = i.split(base_path)[1].split('/')
        if dir not in file.keys():
            file[dir] = []
        file[dir].append(base_path + dir + '/' + name)

    for dir in file.keys():
        if len(glob.glob(base_path + dir + '/*.i')) > 0:
            file[dir].append(base_path + dir + '/' + dir + '.i')

    return file


# the base dependencies
with open('requirements.txt', 'r') as fh:
    dependencies = [l.strip() for l in fh]
# ================================================================================
NAME = 'CosmAna'

PACKAGES = find_packages('.')  # ,['pack1', 'pack2', 'Ext_C']

SCRIPTS = ['']

DESCRIPTION = 'A Python package for cosmological data analysis.'

LONG_DESCRIPTION = read('README.md')

KEYWORDS = 'python; cosmology; data analysis'

AUTHOR = 'Tian-Xiang Mao'

AUTHOR_EMAIL = 'maotianxiang@bao.ac.cn'

URL = 'https://github.com/POFK/CosmAna'

VERSION = '0.2'

LICENSE = 'MIT'

DATA_FILES = ''

# ============================ Extension C ===============================
Ext_path = find_extc('CosmAna/Ext_C/')
Ext_Dir = ['libgrid', 'libfftw']
ext_modules = []
cython_ext_modules = []

try:
    import mpi4py
except ImportError:
    print "mpi4py is needed!"

try:
    import numpy
    INCL.append(numpy.get_include())
except ImportError:
    pass

cython_ext_modules += cythonize(
    Extension(NAME + '.Ext_C.libfftw.libfftw',
              sources=Ext_path['libfftw'],
              include_dirs=INCL + [FFTW_INCL] + [MPI_INCL],
              library_dirs=[FFTW_LIBS],
              libraries=['fftw3f_mpi', 'fftw3f']))

ext_modules.append(Extension(NAME + '.Ext_C.libgrid.libgrid',
                             sources=Ext_path['libgrid'],
                             include_dirs=INCL,
                             # define_macros=[('A', '1')], # example for macros
                             )
                   )
ext_modules = ext_modules + cython_ext_modules

# ================================================================================

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language ::Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    ext_modules=ext_modules,
    packages=PACKAGES,
    scripts=SCRIPTS,
    data_files=DATA_FILES,
    install_requires=dependencies,
    setup_requires=['cython>0.25', 'setuptools>=18.0'],
    test_suite='tests',
)

'''
>>> python setup.py sdist
>>> python setup.py build_ext
>>> python setup.py build
>>> python setup.py develop
>>> python setup.py develop -u
'''
