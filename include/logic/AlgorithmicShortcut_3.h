#ifndef ALGO_SHORT_3_H
#define ALGO_SHORT_3_H

    #include "AlgorithmicShortcut.h"
    #include "Solver_GR.h"

    class AlgorithmicShortcut_3 : public AlgorithmicShortcut {

    public:
        ~AlgorithmicShortcut_3() { };
        acceptance_result try_solve(AF &framework, uint32_t query_argument);
    };

#endif