#!/bin/bash

cd ~

VERSION=3.19

sudo apt-get install libssl-dev -y

sudo rm -rf cmake-$VERSION.0/
wget https://cmake.org/files/v$VERSION/cmake-$VERSION.0.tar.gz
sudo tar -xpvf cmake-$VERSION.0.tar.gz cmake-$VERSION.0/
sudo chmod -R 777 cmake-$VERSION.0/
cd cmake-$VERSION.0/
sudo ./bootstrap
sudo make -j$(nproc)
sudo make install
sudo ldconfig
