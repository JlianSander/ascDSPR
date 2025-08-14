#ifndef ALGO_SHORT_9_H
#define ALGO_SHORT_9_H
    #ifdef ASC_9
    
        #include "AlgorithmicShortcut.h"
        #include "Encoding.h"
        #include "SatSolver.h"

        class AlgorithmicShortcut_9 : public AlgorithmicShortcut {

        public:
            ~AlgorithmicShortcut_9() { };
            acceptance_result try_solve(AF &framework, uint32_t query_argument);
        };
    #endif
#endif