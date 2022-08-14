#!/bin/bash
#
cd ~

echo "** Install requirements"
sudo apt-get update
sudo apt-get install -y \
	curl \
	libopencv-core-dev \
	libopencv-highgui-dev \
	libopencv-calib3d-dev \
	libopencv-features2d-dev \
	libopencv-imgproc-dev \
	libopencv-video-dev \
	build-essential cmake git unzip pkg-config \
	libjpeg-dev libpng-dev libgtk2.0-dev \
	python3-dev python3-numpy python3-pip \
	libxvidcore-dev libx264-dev libssl-dev \
	libtbb2 libtbb-dev libdc1394-22-dev \
	gstreamer1.0-tools libv4l-dev v4l-utils \
	libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
	libvorbis-dev libxine2-dev \
	libfaac-dev libmp3lame-dev libtheora-dev \
	libopencore-amrnb-dev libopencore-amrwb-dev \
	libopenblas-dev libatlas-base-dev libblas-dev \
	liblapack-dev libeigen3-dev \
	libhdf5-dev protobuf-compiler \
	libprotobuf-dev libgoogle-glog-dev libgflags-dev \
	libavutil-dev libavcodec-dev \
	libavformat-dev libswscale-dev ffmpeg

# sudo apt-get install -y libavutil55=7:3.4.2-2

sudo rm -rf mediapipe
mkdir -p mediapipe
cd mediapipe

#curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1M7LdJjHZoz648KnZreKZawRmWK3UD3ib" > /dev/null
#CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
#curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1M7LdJjHZoz648KnZreKZawRmWK3UD3ib" -o opencv_contrib_python-4.5.2.52-cp36-none-linux_aarch64.whl

echo "** Download numpy-1.19.4 sources"
curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=15JN3sYMuKsV1AVmNHRFlN5pQ1LVh8MVa" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=15JN3sYMuKsV1AVmNHRFlN5pQ1LVh8MVa" -o numpy-1.19.4-cp36-none-manylinux2014_aarch64.whl

echo "** Download mediapipe-0.8.5 sources"
curl -sc /tmp/cookie "https://drive.google.com/uc?export=download&id=1_GRGQDwsl169TN9w_qWUs1cx9g_d4wMd" > /dev/null
CODE="$(awk '/_warning_/ {print $NF}' /tmp/cookie)"
curl -Lb /tmp/cookie "https://drive.google.com/uc?export=download&confirm=${CODE}&id=1_GRGQDwsl169TN9w_qWUs1cx9g_d4wMd" -o mediapipe-0.8.5_cuda102-cp36-none-linux_aarch64.whl


sudo pip3 install \
	numpy-1.19.4-cp36-none-manylinux2014_aarch64.whl \
	mediapipe-0.8.5_cuda102-cp36-none-linux_aarch64.whl
sudo ldconfig

echo "Success installed mediapipe-0.8.5, numpy-1.19.4"
