#!/usr/bin/env sh

mkdir -p ~/src
if [ ! -d ~/src/DisCODe ]; then
  git clone https://github.com/qiubix/DisCODe.git ~/src/DisCODe
  cd ~/src/DisCODe && mkdir build && cd build
  cmake .. -DCMAKE_INSTALL_PREFIX=`pwd`/inst
  make -j4
  make install
fi

mkdir -p ~/src/DCL
if [ ! -d ~/src/DCL/CvCoreTypes ]; then
  git clone https://github.com/maciek-slon/CvCoreTypes.git ~/src/DCL/CvCoreTypes
  cd ~/src/DCL/CvCoreTypes && mkdir build && cd build
  cmake .. && make -j3 && make install
fi

if [ ! -d ~/src/DCL/CvBasic ]; then
  git clone https://github.com/maciek-slon/DCL_CvBasic ~/src/DCL/CvBasic
  cd ~/src/DCL/CvBasic && mkdir build && cd build
  cmake .. -DCMAKE_SKIP_INSTALL_ALL_DEPENDENCY=true && make Sequence CvSIFT -j3 && make install/fast
fi

