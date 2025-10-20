
    #include "../../include/logic/AlgorithmicShortcut_10.h"

    acceptance_result AlgorithmicShortcut_10::try_solve(AF &framework, uint32_t query_argument)
    {
        // initialize SATSolver
        SatSolver *solver = NULL;
        solver = new SatSolver();
        // add encoding for nonempty complete labeling to the SATSolver
        Encoding::add_clauses_nonempty_complete(*solver, framework);

        // check if there is at least one nonempty complete labeling
        bool exists_complete_labeling = (*solver).solve();
        if (!exists_complete_labeling)
        {
            return acceptance_result::unknown;
        }

        // create new solver, since kissat allows no incremental clause adding
        solver = new SatSolver();
        // add encoding for nonempty complete labeling to the SATSolver
        Encoding::add_clauses_nonempty_complete(*solver, framework);
        create_clauses_self_defense(framework, *solver);

        // ask SAT solver if a nonempty complete labeling lab exists, so that lab(q) = NOT IN
        (*solver).add_clause_short(Encoding::get_literal_accepted(query_argument, false), 0);
        bool exists_complete_labeling_not_in = (*solver).solve();

        if (exists_complete_labeling_not_in) {
            return acceptance_result::unknown;
        } else {
            return acceptance_result::accepted;
        }
    }

    //===========================================================================================================================================================
    //===========================================================================================================================================================

    void AlgorithmicShortcut_10::create_clauses_self_defense(AF &framework, SatSolver &solver)
    {
        vector<uint32_t> set_self_defending_arguments = get_set_self_defending_arguments(framework);

        for(uint32_t i = 0; i < set_self_defending_arguments.size(); i++)
        {
            uint32_t argument = set_self_defending_arguments[i];
            solver.add_clause_short(Encoding::get_literal_accepted(argument, true), Encoding::get_literal_rejected(framework, argument, true));
        }
    }

    //===========================================================================================================================================================
    //===========================================================================================================================================================

    vector<uint32_t> AlgorithmicShortcut_10::get_set_self_defending_arguments(AF &framework)
    {
        vector<uint32_t> set_self_defending_arguments;
        for (uint32_t i = 0; i < framework.num_args; i++)
        {
            uint32_t argument = i + 1;

            //ensure that self-attacking arguments cannot be self-defending arguments
            if(framework.self_attack[argument])
            {
                continue;
            }

            vector<uint32_t> attackers = framework.attackers[argument];
            bool is_self_defending = true;
            for (uint32_t j = 0; j < framework.attackers[argument].size(); j++)
            {
                uint32_t attacker = attackers[j];
                if (!framework.exists_attack(argument, attacker))
                {
                    is_self_defending = false;
                    break;
                }
            }

            if (is_self_defending)
            {
                set_self_defending_arguments.push_back(argument);
            }
        }

        return set_self_defending_arguments;
    }

