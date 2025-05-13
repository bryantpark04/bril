# Bril-MLIR

Code to support an MLIR dialect for Bril.


Helpful commands
```bash
export LLVM_DIR=`brew --prefix llvm`/lib/cmake/llvm

cd bril-mlir
git clone git@github.com:bryantpark04/llvm-project.git
cd llvm-project
# follow the directions on https://mlir.llvm.org/getting_started/ to build MLIR - this will take a while
cd ..
bril2json < {filename} | python ssa-old/to_ssa.py | ./llvm-project/build/bin/brilc -emit=mlir > {filename}.mlir
./llvm-project/build/bin/brilc -emit=convert < {filename}.mlir
```
