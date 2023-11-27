#!/bin/bash

tar xzf *.tgz
ln -s ../../llvm/ llvm
ln -s ../../llvm/Debug+Asserts/lib/
ln -s ../../llvm/Debug+Asserts/bin/
cd uscc
make -f ../../Makefile clean
make -f ../../Makefile
tar xzf ../../uscc-PA6.tgz
cd tests
timeout 20 python2 testOpt.py
