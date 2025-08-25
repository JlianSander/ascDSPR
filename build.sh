#!/bin/sh

#==========================================================================================
# installs the SAT-Solver Kissat (https://github.com/arminbiere/kissat), which is 
# the default SAT-Solver of this Argumentation Solver
#==========================================================================================

cd sat
wget https://github.com/arminbiere/kissat/archive/refs/tags/rel-4.0.3.tar.gz
tar -xvzf kissat-rel-4.0.3.tar.gz
rm kissat-rel-4.0.3.tar.gz
mv kissat-rel-4.0.3 kissat
cd kissat
./configure && make
cd ../..
make