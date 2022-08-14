#!/bin/bashs
cd ~


sudo apt install libssl-dev -y

# install some requirement: cmake 3.18
VERSION=3.18
sudo rm -rf cmake-$VERSION.0/
wget https://cmake.org/files/v$VERSION/cmake-$VERSION.0.tar.gz
sudo tar -xpvf cmake-$VERSION.0.tar.gz cmake-$VERSION.0/
sudo chmod -R 777 cmake-$VERSION.0/
cd cmake-$VERSION.0/
sudo ./bootstrap
sudo make -j$(nproc)
sudo make install
sudo ldconfig

sudo apt install -y --no-install-recommends \
   build-essential software-properties-common protobuf-compiler libopenblas-dev libprotoc-dev \
   libpython3.6-dev python3-pip python3-dev python3-setuptools python3-wheel
sudo pip3 install Cython onnx --user
sudo pip3 install pandas onnxmltools

export CUDACXX="/usr/local/cuda/bin/nvcc"
export PATH="/usr/local/cuda/bin:${PATH}"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64
export ONNX_ML=1


# Uses auto
git clone --recursive https://github.com/microsoft/onnxruntime
cd onnxruntime

# git checkout b783805 (if needed)
# mody file tools/ci_build/build.py
# def generate_build_tree
# - "-Donnxruntime_DEV_MODE=" + ("OFF" if args.android else "ON"),
# + "-Donnxruntime_DEV_MODE=" + ("OFF" if args.android else "OFF"),
# Modify cmake/CMakeLists.txt
#    -  set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -gencode=arch=compute_50,code=sm_50") # M series
#    +  set(CMAKE_CUDA_FLAGS "${CMAKE_CUDA_FLAGS} -gencode=arch=compute_53,code=sm_53") # Jetson support
#
# with lasted release
# search: def generate_build_tree in tools/ci_build/build.py
# "-Donnxruntime_DEV_MODE=" + ("OFF" if args.android else "OFF"),
# use cuda build
rm -rf build/
./build.sh --config Release --update --build --parallel --build_wheel \
	--use_cuda --cuda_home /usr/local/cuda \
	--cudnn_home /usr/lib/aarch64-linux-gnu
sudo pip3 install build/Linux/Release/dist/*.whl

# use tensorrt build
rm -rf build/
./build.sh --config Release --update --build --parallel --build_wheel \
	--use_tensorrt --cuda_home /usr/local/cuda --cudnn_home /usr/lib/aarch64-linux-gnu \
	--tensorrt_home /usr/lib/aarch64-linux-gnu
sudo pip3 install build/Linux/Release/dist/*.whl


# Uses manual
git clone --recurse-submodules https://github.com/onnx/onnx-tensorrt.git
cd onnx-tensorrt
mkdir build
cd build
cmake ../ -DCUDA_INCLUDE_DIRS="/usr/local/cuda-10.2/include" -DCUDNN_INCLUDE_DIR="/usr/lib/aarch64-linux-gnu" -DTENSORRT_INCLUDE_DIR="/usr/include/aarch64-linux-gnu" -DTENSORRT_LIBRARY_INFER_PLUGIN="/usr/lib/aarch64-linux-gnu/libnvinfer_plugin.so" -DTENSORRT_ROOT="/usr/src/tensorrt/" -DGPU_ARCHS="53" -DTENSORRT_LIBRARY_INFER="/usr/lib/aarch64-linux-gnu/libnvinfer.so"
sudo make -j4
sudo make install

