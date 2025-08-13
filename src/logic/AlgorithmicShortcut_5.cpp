#ifdef ASC_5
    #include "../../include/logic/AlgorithmicShortcut_5.h"

    acceptance_result AlgorithmicShortcut_5::try_solve(AF &framework, uint32_t query_argument)
    {
        // initialize SATSolver
        SatSolver *solver = NULL;
        solver = new SatSolver();
        // add encoding for nonempty complete labeling to the SATSolver
        Encoding::add_clauses_nonempty_complete(*solver, framework);
        // ask SAT solver if a nonempty complete labeling lab exists, so that lab(q) = IN
        bool exists_complete_labeling = (*solver).solve(Encoding::get_literal_accepted(query_argument, true));

        if(exists_complete_labeling){
            return acceptance_result::unknown;
        } else {
            return acceptance_result::rejected;
        }
    }
#endif