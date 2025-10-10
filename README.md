
# ascDSPR- algorithmic shortcuts for skeptical reasoning under preferred semantics

## Build process

### Default SAT-Solver:

To setup the default SAT-solver use 
```
./setup_sat.sh
```
The scripts downloads and compiles <a href="https://github.com/arminbiere/kissat">Kissat</a> 4.0.3.

To use the SAT-Solver of your choise follow these instructions:

### Using a specific IPASIR-SAT-Solver:
**ascDSPR** supports the use of SAT-Solvers implementing the interface <a href="https://github.com/biotomas/ipasir">ipasir</a>.
In case you want **ascDSPR** to use a specific IPASIR-SAT-Solver (e.g. MYSATSOLVER) follow this build process:
#### Default location
- Copy your compiled IPASIR-SAT-Solver to `/sat/MYSATSOLVER/build`
- execute the makefile as follows
```
make IPASIRSOLVER=MYSATSOLVER
```

#### Specific location
If your SAT-Solver(.a or .so file) is located in a specific directory (e.g. PATHTOMYSATSOLVERLIB) use the following command:
```
make IPASIRSOLVER=MYSATSOLVER IPASIRLIBDIR=PATHTOMYSATSOLVERLIB
```

### Compiling different Shortcuts:

Without any additional flag **ascDSPR** will always compile shortcut S1 (ASC_01). If you want to compile any of the other shortcuts (S2 - S10), then add the compiler flag ASC=X with X in \{2, 3, .., 10\}.
In case you use the default SAT-Solver the build command looks like this:
```
make ASC=4
```

## Features
Supported problems: [DS-PR]

Supported file-formats : [.i23, .tgf]	

use `--help` for further information

<p>
created by
<br>
<a href="https://www.fernuni-hagen.de/aig/team/lars.bengel.shtml">Lars Bengel</a>,
<a href="https://www.fernuni-hagen.de/aig/team/julian.sander.shtml">Julian Sander</a> and
<a href="https://www.fernuni-hagen.de/aig/team/matthias.thimm.shtml">Matthias Thimm</a>


