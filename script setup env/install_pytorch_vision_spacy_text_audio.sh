#!/bin/bash

# This script will install pytorch, torchvision, torchtext and spacy on nano. 
# If you have any of these installed already on your machine, you can skip those.

cd ~

echo "** Install requirements"
sudo apt-get -y update
# sudo apt-get -y upgrade
#Dependencies
sudo apt-get install python3-setuptools -y
sudo apt-get install python3-pip libopenblas-base -y
sudo apt-get install libjpeg-dev zlib1g-dev -y
sudo apt-get install cmake build-essential pkg-config libgoogle-perftools-dev -y

#Installing PyTorch
#For latest PyTorch refer original Nvidia Jetson Nano thread - https://devtalk.nvidia.com/default/topic/1049071/jetson-nano/pytorch-for-jetson-nano/.
TORCH_VERSION=1.7.0
# echo "** Download torch-1.8.0 sources"
# wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O torch-1.8.0-cp36-cp36m-linux_aarch64.whl
echo "** Download torch-"$TORCH_VERSION "sources"
wget https://nvidia.box.com/shared/static/cs3xn3td6sfgtene6jdvsxlr366m2dhq.whl -O torch-$TORCH_VERSION-cp36-cp36m-linux_aarch64.whl
sudo chmod -R 777 torch-$TORCH_VERSION-cp36-cp36m-linux_aarch64.whl
echo "** Install numpy, torch-"$TORCH_VERSION
sudo pip3 install Cython
sudo pip3 install \
	numpy \
	torch-$TORCH_VERSION-cp36-cp36m-linux_aarch64.whl

#Installing torchvision
#For latest torchvision refer original Nvidia Jetson Nano thread - https://devtalk.nvidia.com/default/topic/1049071/jetson-nano/pytorch-for-jetson-nano/.
VISION_VERSION=0.8.1	
echo "** Download torchvision-v"$VISION_VERSION" sources"
git clone --branch v$VISION_VERSION https://github.com/pytorch/vision torchvision   
# see below for version of torchvision to download
sudo chmod -R 777 torchvision
cd torchvision
echo "** Install torchvision-v"$VISION_VERSION
sudo python3 setup.py install
cd ../  # attempting to load torchvision from build dir will result in import error

#Installing dependency sentencepiece
echo "** Download sentencepiece sources"
git clone https://github.com/google/sentencepiece.git
sudo chmod -R 777 sentencepiece
cd sentencepiece
mkdir build
cd build
echo "** Build sentencepiece sources"
cmake ..
make -j$(nproc)
sudo make install
sudo ldconfig -v
cd ../python
echo "** Install sentencepiece"
sudo python3 setup.py build
sudo python3 setup.py install
cd ../../

#Installing spaCy
echo "** Download spaCy sources"
git clone --recursive https://github.com/explosion/spaCy
git submodule update --init --recursive
sudo chmod -R 777 spaCy
cd spaCy/
export PYTHONPATH=`pwd`
export BLIS_ARCH=generic
echo "** Install spaCy"
sudo apt purge python3-yaml -y
sudo pip3 install -r requirements.txt
sudo python3 setup.py build_ext --inplace
sudo python3 setup.py install
sudo python3 -m spacy download en_core_web_sm
cd ../

#Installing torchtext
echo "** Download torchtext sources"
git clone --recursive https://github.com/pytorch/text.git
sudo chmod -R 777 text
cd text
git submodule update --init --recursive

echo "** Install torchtext"
sudo pip3 install -r requirements.txt
sudo python3 setup.py install
cd ../

#Installing audio
echo "** Download torchaudio sources"
git clone --recurse https://github.com/pytorch/audio.git
sudo chmod -R 777 audio
cd audio
git submodule update --init --recursive

echo "** Install torchaudio"
sudo pip3 install -r requirements.txt
sudo python3 setup.py install
cd ../

echo "\ndone installing PyTorch, torchvision, spaCy, torchtext, torchaudio"
