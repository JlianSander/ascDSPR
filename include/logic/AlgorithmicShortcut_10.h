#ifndef ALGO_SHORT_10_H
#define ALGO_SHORT_10_H
    
    #include "AlgorithmicShortcut.h"
    #include "Encoding.h"
    #include "SatSolver.h"

    class AlgorithmicShortcut_10 : public AlgorithmicShortcut {

    public:
        ~AlgorithmicShortcut_10() { };
        acceptance_result try_solve(AF &framework, uint32_t query_argument);

    private:
        static void create_clauses_self_defense(AF &framework, SatSolver &solver);
        static vector<uint32_t> get_set_self_defending_arguments(AF &framework);
    };

#endif