#ifndef ALGO_SHORT_4_H
#define ALGO_SHORT_4_H

    #include "AlgorithmicShortcut.h"
    #include "Solver_GR.h"

    class AlgorithmicShortcut_4 : public AlgorithmicShortcut {

    public:
        ~AlgorithmicShortcut_4() { };
        acceptance_result try_solve(AF &framework, uint32_t query_argument);
    };

#endif