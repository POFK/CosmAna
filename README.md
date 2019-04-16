[![BCH compliance](https://bettercodehub.com/edge/badge/POFK/CosmAna?branch=master)](https://bettercodehub.com/)
# CosmAna 

## Dependences
### install [Miniconda](https://conda.io/miniconda.html) \(python2.7)

```
conda create -n CosmAna python=2.7
source activate CosmAna
conda install --file requirements.txt
```
If the download speed is too slow, you can add the following lines to `~/.condarc`.
```
channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - defaults
show_channel_urls: true
```

### install [mpich](http://www.mpich.org/static/downloads/3.2.1/mpich-3.2.1.tar.gz)

```
tar -xvf mpich-3.2.1.tar.gz
cd mpich-3.2.1
./configure --prefix=$HOME/local/mpich-3.2.1
make
make install
```
### install [mpi4py](https://github.com/mpi4py/mpi4py/archive/3.0.0.zip)
```
tar -xvf mpi4py-3.0.0.tar.gz
cd mpi4py-3.0.0
```
open file "mpi.cfg", set
```
mpi_dir = path/to/mpich-3.2.1
```
and remove comments of `mpicc` and `mpicxx`. 
then run
```
python setup.py build
python setup.py install
```

### install fftw

```
tar -xvf fftw-3.3.5.tar.gz
cd fftw-3.3.5

./configure --prefix=$HOME/local/fftw-3.3.5 --enable-threads --enable-mpi --enable-openmp --enable-shared --disable-fortran --enable-long-double
make -j4; make install; make clean

./configure --prefix=$HOME/local/fftw-3.3.5 --enable-threads --enable-mpi --enable-openmp --enable-shared --disable-fortran --enable-float
make -j4; make install; make clean

./configure --prefix=$HOME/local/fftw-3.3.5 --enable-threads --enable-mpi --enable-openmp --enable-shared --disable-fortran
make -j4; make install
```
add LD_LIBRARY_PATH: 
```
export LD_LIBRARY_PATH=$HOME/local/fftw-3.3.5/lib:$LD_LIBRARY_PATH
```

### install CosmAna
```
python setup.py build_ext
python setup.py develop
```

### Option
- matplotlib:
`conda install matplotlib`
- jupyter notebook
- jupyter ipython cluster


## Authors

* **Tian-Xiang Mao** [email](mailto:maotianxiang@bao.ac.cn) - *Initial work* - [POFK](https://github.com/POFK)

See also the list of [contributors](https://github.com/POFK/CosmAna/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE) file for details

<!---
## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
-->

