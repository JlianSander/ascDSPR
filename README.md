
# reducto - A Vacuous Reduct-based Argumentation Solver 

**reducto** is a SAT-based solver for reasoning problems in abstract argumentation. The solver is mainly built on standard SAT-encodings with some improvements. In particular, for skeptical reasoning wrt. preferred semantics it contributes a non-standard approach. reducto refrains from iterative maximisation and instead utilises a reduct-based characterisation of preferred semantics to efficiently find counterexamples for the skeptical acceptance of an argument.

## Build process

### For default compilation:
```
./build.sh
```
As default reducto uses <a href="https://github.com/arminbiere/cadical">CaDiCaL</a> as a SAT-Solver. Executing the `build.sh` script will download and compile CaDiCaL.

### Using a specific IPASIR-SAT-Solver:
reducto supports the use of SAT-Solvers implementing the interface <a href="https://github.com/biotomas/ipasir">ipasir</a>.
In case you want reducto to use a specific IPASIR-SAT-Solver (e.g. MYSATSOLVER) follow this build process:
#### Default location
- Copy your compiled IPASIR-SAT-Solver to `/sat/MYSATSOLVER/build`
- execute the makefile as follows
```
make all IPASIRSOLVER=MYSATSOLVER
```

#### Specific location
If your SAT-Solver(.a or .so file) is located in a specific directory (e.g. PATHTOMYSATSOLVERLIB) use the following command:
```
make all IPASIRSOLVER=MYSATSOLVER IPASIRLIBDIR=PATHTOMYSATSOLVERLIB
```

## Features
Supported problems: [DC-ST,DC-CO,DS-ST,DS-PR,SE-ST,SE-PR]

Supported file-formats : [.i23, .tgf]	

use `--help` for further information

<p>
created by
<br>
<a href="https://www.fernuni-hagen.de/aig/team/lars.bengel.shtml">Lars Bengel</a>,
<a href="https://www.fernuni-hagen.de/aig/team/julian.sander.shtml">Julian Sander</a> and
<a href="https://www.fernuni-hagen.de/aig/team/matthias.thimm.shtml">Matthias Thimm</a>


