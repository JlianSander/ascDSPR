#ifdef ASC_7
    #include "../../include/logic/AlgorithmicShortcut_7.h"

    acceptance_result AlgorithmicShortcut_7::try_solve(AF &framework, uint32_t query_argument)
    {
        // check if q attacks any other argument
        if(framework.victims[query_argument].size() == 0){
            return acceptance_result::unknown;
        }

        // initialize SATSolver
        SatSolver *solver = NULL;
        solver = new SatSolver();
        // add encoding for nonempty complete labeling to the SATSolver
        Encoding::add_clauses_nonempty_complete(*solver, framework);

        // create clause of the victims of q
        vector<int64_t> clause_victims;
        vector<uint32_t> victims = framework.victims[query_argument];
		for (std::vector<unsigned int>::size_type i = 0; i < victims.size(); i++)
		{
            uint32_t victim = victims[i];
            clause_victims.push_back(Encoding::get_literal_accepted(victim, true));
        }
        (*solver).add_clause(clause_victims);

        // ask SAT solver if a nonempty complete labeling lab exists, so that lab(q) = OUT
        bool exists_complete_labeling = (*solver).solve();

        if(exists_complete_labeling){
            return acceptance_result::rejected;
        } else {
            return acceptance_result::unknown;
        }
    }

#endif