#!/bin/bash
# License: MIT. See license file in root directory
# Copyright(c) JetsonHacks (2017-2019)
# Modify by SouthernVEVO (2021)

cd ~

OPENCV_VERSION=4.4.0
#4.5.3
# Jetson Nano
ARCH_BIN=5.3
INSTALL_DIR=/usr/local
# Download the opencv_extras repository
# If you are installing the opencv testdata, ie
#  OPENCV_TEST_DATA_PATH=../opencv_extra/testdata
# Make sure that you set this to YES
# Value should be YES or NO
DOWNLOAD_OPENCV_EXTRAS=YES
# Source code directory
OPENCV_SOURCE_DIR=$HOME
WHEREAMI=$PWD
# NUM_JOBS is the number of jobs to run simultaneously when using make
# This will default to the number of CPU cores (on the Nano, that's 4)
# If you are using a SD card, you may want to change this
# to 1. Also, you may want to increase the size of your swap file
NUM_JOBS=$(nproc)

CLEANUP=true

PACKAGE_OPENCV="-D CPACK_BINARY_DEB=ON"

function usage
{
    echo "usage: ./buildOpenCV.sh [[-s sourcedir ] | [-h]]"
    echo "-s | --sourcedir   Directory in which to place the opencv sources (default $HOME)"
    echo "-i | --installdir  Directory in which to install opencv libraries (default /usr/local)"
    echo "--no_package       Do not package OpenCV as .deb file (default is true)"
    echo "-h | --help  This message"
}

# Iterate through command line inputs
while [ "$1" != "" ]; do
    case $1 in
        -s | --sourcedir )      shift
				OPENCV_SOURCE_DIR=$1
                                ;;
        -i | --installdir )     shift
                                INSTALL_DIR=$1
                                ;;
        --no_package )          PACKAGE_OPENCV=""
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

CMAKE_INSTALL_PREFIX=$INSTALL_DIR

# Print out the current configuration
echo "Build configuration: "
echo " NVIDIA Jetson Nano"
echo " OpenCV binaries will be installed in: $CMAKE_INSTALL_PREFIX"
echo " OpenCV Source will be installed in: $OPENCV_SOURCE_DIR"
if [ "$PACKAGE_OPENCV" = "" ] ; then
   echo " NOT Packaging OpenCV"
else
   echo " Packaging OpenCV"
fi

if [ $DOWNLOAD_OPENCV_EXTRAS == "YES" ] ; then
 echo "Also downloading opencv_extras"
fi


# remove old versions or previous builds
sudo apt-get purge *libopencv* -y
sudo rm -rf opencv*

# Repository setup
sudo sh -c "echo '/usr/local/cuda/lib64' >> /etc/ld.so.conf.d/nvidia-tegra.conf"
sudo ldconfig

sudo apt-add-repository universe
sudo apt-get update

# Download dependencies for the desired configuration
cd $WHEREAMI
sudo apt-get install -y \
    build-essential \
    cmake \
    git \
    gfortran \
    libatlas-base-dev \
    libavresample-dev \
    libcanberra-gtk3-module \
    libdc1394-22-dev \
    libgstreamer-plugins-good1.0-dev \
    libjpeg8-dev \
    libjpeg-turbo8-dev \
    libvorbis-dev \
    liblapack-dev \
    liblapacke-dev \
    libtheora-dev \
    libmp3lame-dev \
    libfaac-dev \
    libopenblas-dev \
    libopencore-amrnb-dev \
    libopencore-amrwb-dev \
    libtbb2 \
    libtesseract-dev \
    libtiff-dev \
  	libblas-dev \
    libxine2-dev \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
  	libcanberra-gtk* \
    libeigen3-dev \
    libglew-dev \
    libgtk2.0-dev \
    libgtk-3-dev \
    libjpeg-dev \
    libpng-dev \
    libpostproc-dev \
    libswscale-dev \
    libtbb-dev \
    libtiff5-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    qt5-default \
    zlib1g-dev \
    python-dev \
    python-numpy \
    python3-dev \
    python3-numpy \
    python3-matplotlib \
	gstreamer1.0-tools \
    qv4l2 \
    v4l-utils \
    v4l2ucp \
    libgoogle-glog-dev \
    libprotobuf-dev \
    libgflags-dev \
    libhdf5-dev \
    protobuf-compiler \
    unzip \
    pkg-config

# We will be supporting OpenGL, we need a little magic to help
# https://devtalk.nvidia.com/default/topic/1007290/jetson-tx2/building-opencv-with-opengl-support-/post/5141945/#5141945
cd /usr/local/cuda/include
sudo patch -N cuda_gl_interop.h $WHEREAMI'/patches/OpenGLHeader.patch' 

# Python 2.7
sudo apt-get install -y python-dev python3-pip python-numpy python-py python-pytest
# Python 3.6
sudo apt-get install -y python3-dev python3-numpy python3-py python3-pytest
# GStreamer support
sudo apt-get install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
sudo pip3 install scikit-build

cd $OPENCV_SOURCE_DIR
git clone --branch "$OPENCV_VERSION" https://github.com/opencv/opencv.git
git clone --branch "$OPENCV_VERSION" https://github.com/opencv/opencv_contrib.git
sudo chmod -R 777 opencv opencv_contrib

if [ $DOWNLOAD_OPENCV_EXTRAS == "YES" ] ; then
 echo "Installing opencv_extras"
 # This is for the test data
 cd $OPENCV_SOURCE_DIR
 git clone https://github.com/opencv/opencv_extra.git
 cd opencv_extra
 git checkout -b v${OPENCV_VERSION} ${OPENCV_VERSION}
fi

# Patch the Eigen library issue ...
cd $OPENCV_SOURCE_DIR/opencv
sed -i 's/include <Eigen\/Core>/include <eigen3\/Eigen\/Core>/g' modules/core/include/opencv2/core/private.hpp

# Create the build directory and start cmake
cd $OPENCV_SOURCE_DIR/opencv
mkdir build
cd build

# Here are some options to install source examples and tests
#     -D INSTALL_TESTS=ON \
#     -D OPENCV_TEST_DATA_PATH=../opencv_extra/testdata \
#     -D INSTALL_C_EXAMPLES=ON \
#     -D INSTALL_PYTHON_EXAMPLES=ON \
#     -D CUDNN_VERSION='8.0' \
#     -D CUDA_ARCH_PTX="53"


# If you are compiling the opencv_contrib modules:
# curl -L https://github.com/opencv/opencv_contrib/archive/3.4.1.zip -o opencv_contrib-3.4.1.zip

# There are also switches which tell CMAKE to build the samples and tests
# Check OpenCV documentation for details
#       -D WITH_QT=ON \

echo $PWD
time cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} \
          -D BUILD_EXAMPLES=OFF \
          -D BUILD_opencv_python2=ON \
          -D BUILD_opencv_python3=ON \
          -D BUILD_PERF_TESTS=OFF \
          -D BUILD_JPEG=ON \
          -D BUILD_PNG=ON \
          -D BUILD_TBB=ON \
          -D BUILD_TESTS=OFF \
          -D BUILD_TIFF=ON \
          -D CUDA_ARCH_BIN=${ARCH_BIN} \
          -D CUDA_ARCH_PTX="" \
          -D CUDNN_VERSION='8.0' \
          -D CUDA_FAST_MATH=ON \
          -D CUDA_TOOLKIT_ROOT_DIR='/usr/local/cuda' \
          -D CUDNN_INCLUDE_DIR='/usr/include' \
          -D EIGEN_INCLUDE_PATH='/usr/include/eigen3' \
          -D ENABLE_FAST_MATH=ON \
          -D ENABLE_NEON=ON \
          -D INSTALL_C_EXAMPLES=OFF \
          -D INSTALL_TESTS=OFF \
          -D INSTALL_PYTHON_EXAMPLES=OFF \
          -D OPENCV_DNN_CUDA=ON \
          -D OPENCV_ENABLE_NONFREE=ON \
          -D OPENCV_EXTRA_MODULES_PATH='/home/jetson/opencv_contrib/modules' \
          -D OPENCV_GENERATE_PKGCONFIG=ON \
          -D OPENCV_MJPEG=ON \
          -D WITH_CUBLAS=ON \
          -D WITH_CUDA=ON \
          -D WITH_CUDNN=ON \
          -D WITH_EIGEN=ON \
          -D WITH_FFMPEG=ON \
          -D WITH_GSTREAMER=ON \
          -D WITH_GSTREAMER_0_10=OFF \
          -D WITH_GTK=ON \
          -D WITH_JPEG=ON \
          -D WITH_PNG=ON \
          -D WITH_LIBV4L=ON \
          -D WITH_MFX=ON \
          -D WITH_NVCUVID=ON \
          -D WITH_OPENCL=ON \
          -D WITH_OPENGL=ON \
          -D WITH_OPENMP=ON \
          -D WITH_QT=OFF \
          -D WITH_TBB=ON \
          -D WITH_V4L=ON \
          -D WITH_V4L2=ON \
          $"PACKAGE_OPENCV" \
      ../


if [ $? -eq 0 ] ; then
  echo "CMake configuration make successful"
else
  # Try to make again
  echo "CMake issues " >&2
  echo "Please check the configuration being used"
  exit 1
fi

# Consider the MAXN performance mode if using a barrel jack on the Nano
time make -j$NUM_JOBS
if [ $? -eq 0 ] ; then
  echo "OpenCV make successful"
else
  # Try to make again; Sometimes there are issues with the build
  # because of lack of resources or concurrency issues
  echo "Make did not build " >&2
  echo "Retrying ... "
  # Single thread this time
  make
  if [ $? -eq 0 ] ; then
    echo "OpenCV make successful"
  else
    # Try to make again
    echo "Make did not successfully build" >&2
    echo "Please fix issues and retry build"
    exit 1
  fi
fi

echo "Installing ... "
sudo rm -r /usr/include/opencv4/opencv2
sudo make install
cd build/python_loader
sudo python3 setup.py bdist_wheel
sudo ldconfig
if [ $? -eq 0 ] ; then
   echo "OpenCV installed in: $CMAKE_INSTALL_PREFIX"
else
   echo "There was an issue with the final installation"
   exit 1
fi

# If PACKAGE_OPENCV is on, pack 'er up and get ready to go!
# We should still be in the build directory ...
if [ "$PACKAGE_OPENCV" != "" ] ; then
   echo "Starting Packaging"
   sudo ldconfig  
   time sudo make package -j$NUM_JOBS
   if [ $? -eq 0 ] ; then
     echo "OpenCV make package successful"
   else
     # Try to make again; Sometimes there are issues with the build
     # because of lack of resources or concurrency issues
     echo "Make package did not build " >&2
     echo "Retrying ... "
     # Single thread this time
     sudo make package
     if [ $? -eq 0 ] ; then
       echo "OpenCV make package successful"
     else
       # Try to make again
       echo "Make package did not successfully build" >&2
       echo "Please fix issues and retry build"
       exit 1
     fi
   fi
fi


# check installation
IMPORT_CHECK="$(python -c "import cv2 ; print cv2.__version__")"
if [[ $IMPORT_CHECK != *$OPENCV_VERSION* ]]; then
  echo "There was an error loading OpenCV in the Python sanity test."
  echo "The loaded version does not match the version built here."
  echo "Please check the installation."
  echo "The first check should be the PYTHONPATH environment variable."
fi

# cleaning (frees 300 MB)
make clean
sudo apt-get update
sudo ldconfig

echo "Congratulations!"
echo "You've successfully installed OpenCV "$OPENCV_VERSION" on your Jetson Nano"
