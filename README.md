[![BCH compliance](https://bettercodehub.com/edge/badge/POFK/CosmAna?branch=master)](https://bettercodehub.com/)
# CosmAna 

## Dependences
### install [Miniconda](https://conda.io/miniconda.html) \(python2.7)

```
conda config --add channels conda-forge
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

