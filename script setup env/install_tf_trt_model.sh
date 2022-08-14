#!/bin/bash

cd ~
rm -rf tf_trt_models
git clone --recursive https://github.com/NVIDIA-Jetson/tf_trt_models.git
cd tf_trt_models
sudo ./install.sh

