#!/usr/bin/env sh

mkdir -p ~/src
if [ ! -d ~/src/DisCODe ]; then
  git clone https://github.com/maciek-slon/DisCODe.git ~/src/DisCODe
  cd ~/src/DisCODe && mkdir build && cd build
  cmake .. -DCMAKE_INSTALL_PREFIX=`pwd`/inst
  make -j4
  make install
fi
