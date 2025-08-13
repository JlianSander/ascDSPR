#ifndef ALGO_SHORT_1_H
#define ALGO_SHORT_1_H
    #ifdef ASC_1
    
        #include "AlgorithmicShortcut.h"

        class AlgorithmicShortcut_1 : public AlgorithmicShortcut {

        public:
            ~AlgorithmicShortcut_1() { };
            acceptance_result try_solve(AF &framework, uint32_t query_argument);
        };
    #endif
#endif