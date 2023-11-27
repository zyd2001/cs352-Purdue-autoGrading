#!/bin/bash

tar xzf *.tgz
ln -s ../../llvm/ llvm
ln -s ../../llvm/Debug+Asserts/lib/
ln -s ../../llvm/Debug+Asserts/bin/
cd uscc
make -f ../../Makefile clean
make -f ../../Makefile
tar xzf ../../uscc-PA4.tgz
cd tests
timeout 20 python2 testLiveness.py