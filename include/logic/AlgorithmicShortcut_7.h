#ifndef ALGO_SHORT_7_H
#define ALGO_SHORT_7_H
    #ifdef ASC_7
    
        #include "AlgorithmicShortcut.h"
        #include "Encoding.h"
        #include "SatSolver.h"

        class AlgorithmicShortcut_7 : public AlgorithmicShortcut {

        public:
            ~AlgorithmicShortcut_7() { };
            acceptance_result try_solve(AF &framework, uint32_t query_argument);
        };
    #endif
#endif