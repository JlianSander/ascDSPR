#ifndef ALGO_SHORT_8_H
#define ALGO_SHORT_8_H
    
    #include "AlgorithmicShortcut.h"
    #include "Encoding.h"
    #include "SatSolver.h"

    class AlgorithmicShortcut_8 : public AlgorithmicShortcut {

    public:
        ~AlgorithmicShortcut_8() { };
        acceptance_result try_solve(AF &framework, uint32_t query_argument);

            

    private:
        static void create_clauses(AF &framework, uint32_t query_argument, SatSolver &solver);
        static bool check_each_attacker_has_defender(AF &framework, uint32_t query_argument);
        static bool check_only_self_attack(AF &framework, uint32_t query_argument);
    };

#endif