#ifdef ASC_6
    #include "../../include/logic/AlgorithmicShortcut_6.h"

    acceptance_result AlgorithmicShortcut_6::try_solve(AF &framework, uint32_t query_argument)
    {
        // initialize SATSolver
        SatSolver *solver = NULL;
        solver = new SatSolver();
        // add encoding for nonempty complete labeling to the SATSolver
        Encoding::add_clauses_nonempty_complete(*solver, framework);
        // ask SAT solver if a nonempty complete labeling lab exists, so that lab(q) = OUT
        bool exists_complete_labeling = (*solver).solve(Encoding::get_literal_rejected(framework, query_argument, true));

        if(exists_complete_labeling){
            return acceptance_result::rejected;
        } else {
            return acceptance_result::unknown;
        }
    }
#endif