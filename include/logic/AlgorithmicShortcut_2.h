#ifndef ALGO_SHORT_2_H
#define ALGO_SHORT_2_H
    #ifdef ASC_2
    
        #include "AlgorithmicShortcut.h"

        class AlgorithmicShortcut_2 : public AlgorithmicShortcut {

        public:
            ~AlgorithmicShortcut_2() { };
            acceptance_result try_solve(AF &framework, uint32_t query_argument);
        };
    #endif
#endif