#ifndef ALGO_SHORT_6_H
#define ALGO_SHORT_6_H

    #include "AlgorithmicShortcut.h"
    #include "Encoding.h"
    #include "SatSolver.h"

    class AlgorithmicShortcut_6 : public AlgorithmicShortcut {

    public:
        ~AlgorithmicShortcut_6() { };
        acceptance_result try_solve(AF &framework, uint32_t query_argument);
    };

#endif