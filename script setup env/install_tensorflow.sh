#!/bin/bash

cd ~

rm -rf tensorflow
mkdir tensorflow

# install prerequisites
sudo apt install libhdf5-serial-dev hdf5-tools libhdf5-dev zlib1g-dev zip libjpeg8-dev liblapack-dev libblas-dev gfortran -y

# install and upgrade pip3
sudo apt install python3-pip -y
sudo pip3 install -U pip testresources setuptools==49.6.0

# install the following python packages
sudo pip3 install -U numpy==1.19.4 future==0.18.2 mock==3.0.5 h5py==2.10.0 keras_preprocessing==1.1.1 keras_applications==1.0.8 gast==0.2.2 futures protobuf pybind11


# to install TensorFlow 1.15 for JetPack 4.6:
sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v45 'tensorflow<2'

# or install the latest version of TensorFlow (2.5) for JetPack 4.6:
sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v45 tensorflow

JP_VERSION=45
TF_VERSION=2.3.1
NV_VERSION=21.6

#2.5.0
sudo pip3 install --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v$JP_VERSION tensorflow==$TF_VERSION+nv$NV_VERSION

sudo ldconfig

