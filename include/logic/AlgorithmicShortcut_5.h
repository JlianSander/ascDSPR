#ifndef ALGO_SHORT_5_H
#define ALGO_SHORT_5_H
    #ifdef ASC_5
    
        #include "AlgorithmicShortcut.h"
        #include "Encoding.h"
        #include "SatSolver.h"

        class AlgorithmicShortcut_5 : public AlgorithmicShortcut {

        public:
            ~AlgorithmicShortcut_5() { };
            acceptance_result try_solve(AF &framework, uint32_t query_argument);
        };
    #endif
#endif