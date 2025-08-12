#!/bin/sh

#==========================================================================================
# installs the SAT-Solver CaDiCaL (https://github.com/arminbiere/cadical), which is 
# the default SAT-Solver of this Argumentation Solver
#==========================================================================================

cd sat
wget https://github.com/arminbiere/cadical/archive/refs/tags/rel-2.1.3.tar.gz
tar -xvzf rel-2.1.3.tar.gz
rm rel-2.1.3.tar.gz
mv cadical-rel-2.1.3 cadical
cd cadical
./configure && make
cd ../..
make