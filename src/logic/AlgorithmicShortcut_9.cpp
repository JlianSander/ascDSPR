#ifdef ASC_9
    #include "../../include/logic/AlgorithmicShortcut_9.h"

    acceptance_result AlgorithmicShortcut_9::try_solve(AF &framework, uint32_t query_argument)
    {
        // initialize SATSolver
        SatSolver *solver = NULL;
        solver = new SatSolver();
        // add encoding for nonempty complete labeling to the SATSolver
        Encoding::add_clauses_nonempty_complete(*solver, framework);

        // check if there is at least one nonempty complete labeling
        bool exists_complete_labeling = (*solver).solve();
        if(!exists_complete_labeling)
        {
            return acceptance_result::unknown;
        }

        // ask SAT solver if a nonempty complete labeling lab exists, so that lab(q) = NOT IN
        bool exists_complete_labeling_not_in = (*solver).solve(Encoding::get_literal_accepted(query_argument, false));

        if(exists_complete_labeling_not_in){
            return acceptance_result::unknown;
        } else {
            return acceptance_result::accepted;
        }
    }

#endif