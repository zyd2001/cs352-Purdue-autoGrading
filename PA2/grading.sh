#!/bin/bash

tar xzf *.tgz
ln -s ../../llvm/ llvm
ln -s ../../llvm/Debug+Asserts/lib/
ln -s ../../llvm/Debug+Asserts/bin/
cd uscc
make -f ../../Makefile clean
make -f ../../Makefile
tar xzf ../../uscc-PA2.tgz
cd tests
python2 testSemant.py