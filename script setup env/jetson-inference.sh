#!/bin/bash

cd ~

echo "** Install requirements"
sudo apt-get update
sudo apt-get install git cmake libpython3-dev python3-numpy

echo "** Download jetson-inference sources"
git clone --recursive https://github.com/dusty-nv/jetson-inference
cd jetson-inference
mkdir build
cd build
sudo cmake ../
sudo make -j$(nproc)
sudo make install
sudo ldconfig
