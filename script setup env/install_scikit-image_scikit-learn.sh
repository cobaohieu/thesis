#!/bin/bash

cd ~
sudo apt-get install libpcap-dev libpq-dev libatlas-base-dev python3-sklearn python3-sklearn-lib python3-skimage  python3-dev libfreetype6-dev libfontconfig1-dev python3-dev libpython3-dev python3-pil python3-tk python3-pil.imagetk build-essential wget locales liblapack-dev -y
sudo apt-get install libfreetype6-dev python3-setuptools protobuf-compiler libprotobuf-dev openssl libssl-dev libcurl4-openssl-dev cython3 build-essential pkg-config libtbb2 libtbb-dev -y
#sudo apt-get install python3-sklearn-doc

sudo pip3 install scikit-image scikit-learn
sudo pip3 install git+https://github.com/scikit-learn/scikit-learn.git
