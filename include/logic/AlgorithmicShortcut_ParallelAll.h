#ifndef ALGO_SHORT_PARALLEL_ALL_H
#define ALGO_SHORT_PARALLEL_ALL_H
    //#ifdef ASC_PARALLEL_ALL
    
        #include <omp.h>

        #include "AlgorithmicShortcut.h"
        #include "Encoding.h"
        #include "SatSolver.h"

        #include "AlgorithmicShortcut_1.h"
        #include "AlgorithmicShortcut_2.h"
        #include "AlgorithmicShortcut_3.h"
        #include "AlgorithmicShortcut_4.h"
        #include "AlgorithmicShortcut_5.h"
        #include "AlgorithmicShortcut_6.h"
        #include "AlgorithmicShortcut_7.h"
        #include "AlgorithmicShortcut_8.h"
        #include "AlgorithmicShortcut_9.h"
        #include "AlgorithmicShortcut_10.h"


        class AlgorithmicShortcut_ParallelAll : public AlgorithmicShortcut {

        public:
            ~AlgorithmicShortcut_ParallelAll() { };
            acceptance_result try_solve(AF &framework, uint32_t query_argument);

        private:
            
        };
    //#endif
#endif