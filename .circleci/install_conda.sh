#!/bin/bash

if [[ ! -d /home/circleci/miniconda ]]; then
    wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O miniconda.sh &&
    bash miniconda.sh -b -f -p /home/circleci/miniconda;
else
    echo "Using cached miniconda";
fi
source ~/miniconda/bin/activate root
conda config --set always_yes yes
conda update -q conda
conda config --add channels conda-forge
