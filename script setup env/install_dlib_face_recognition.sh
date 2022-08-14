#!/bin/bash

cd ~

sudo apt-get update
sudo apt install -y build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libopenblas-dev \
    libswscale-dev \
    pkg-config \
    python3-pip \
    python3-dev \
    python3-numpy \
    python3-setuptools \
    sed \
    zip

# build from source
content=$(wget http://dlib.net/release_notes.html -q -O -)
# LAST_VERSION=`echo ${content} | awk -F '<h1 style="margin:0px;">Release ' '{print $2}' | awk -F "</h1>" '{print $1}'`

LAST_VERSION=19.19

DLIB_FILE="dlib-${LAST_VERSION}.tar.bz2"

wget http://dlib.net/files/${DLIB_FILE}
tar xvf ${DLIB_FILE}

cd dlib-${LAST_VERSION}/

sed -i 's,forward_algo = forward_best_algo;,//forward_algo = forward_best_algo;,g' dlib/cuda/cudnn_dlibapi.cpp
mkdir build
cd build
cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1
cmake --build . --config Release
cd ..
sudo python3 setup.py install
# sudo python3 setup.py install --yes USE_AVX_INSTRUCTIONS --yes DLIB_USE_CUDA
sudo ldconfig

# install face_recognition
# sudo pip3 install -U pip
sudo pip3 install -U face_recognition
sudo ldconfig

echo -e "Success installed dlib-"${LAST_VERSION}", face-recognition"
