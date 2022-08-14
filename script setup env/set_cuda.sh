#!/bin/bash

set -e

if ! grep 'cuda/bin' ${HOME}/.bashrc > /dev/null ; then
  echo "[BASH]  Add CUDA path into ~/.bashrc"
  echo >> ${HOME}/.bashrc
  echo "export CUDA_HOME=/usr/local/cuda" >> ${HOME}/.bashrc
  echo "export LD_LIBRARY_PATH=/usr/local/cuda/lib64:\${LD_LIBRARY_PATH}" >> ${HOME}/.bashrc
  echo "export PATH=/usr/local/cuda/bin:\${PATH}" >> ${HOME}/.bashrc
  echo "export CPATH=$CPATH:/usr/local/cuda/targets/aarch64-linux/include" >> ${HOME}/.bashrc
  echo "export CUDA_VISIBLE_DEVICES=0" >> ${HOME}/.bashrc
  echo "export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/cuda/targets/aarch64-linux/lib" >> ${HOME}/.bashrc
  source ~/.bashrc
fi
