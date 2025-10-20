
    #include "../../include/logic/AlgorithmicShortcut_8.h"

    acceptance_result AlgorithmicShortcut_8::try_solve(AF &framework, uint32_t query_argument)
    {
    // check if there is at least one attacker of q
    if (framework.attackers[query_argument].size() == 0)
    {
        return acceptance_result::unknown;
    }

    // check if query_argument is attacking itself and has no other attacker
    if (check_only_self_attack(framework, query_argument))
    {
        return acceptance_result::rejected;
    }

    // check if each attacker of q has at least one defender
    if (!check_each_attacker_has_defender(framework, query_argument))
    {
        return acceptance_result::rejected;
    }

    // initialize SATSolver
    SatSolver *solver = NULL;
    solver = new SatSolver();
    // add encoding for nonempty complete labeling to the SATSolver
    Encoding::add_clauses_nonempty_complete(*solver, framework);

    // create clause specific for this shortcut
    create_clauses(framework, query_argument, *solver);

    // ask SAT solver if a nonempty complete labeling lab exists, so that lab(q) = OUT
    bool exists_complete_labeling = (*solver).solve();

    if (exists_complete_labeling)
    {
        return acceptance_result::rejected;
    }
    else
    {
        return acceptance_result::unknown;
    }
    }

    //===========================================================================================================================================================
    //===========================================================================================================================================================

    bool AlgorithmicShortcut_8::check_only_self_attack(AF &framework, uint32_t query_argument)
    {
        vector<uint32_t> attackers = framework.attackers[query_argument];

        // if unattacked then no self-attack possible
        if(attackers.size() == 0) return false;
        // if more than one attacker than at least one has to be no self-attack
        if(attackers.size() > 1) return false;
        // check if only attack is a self-attack
        return attackers[0] == query_argument;
    }
    
    //===========================================================================================================================================================
    //===========================================================================================================================================================

    bool AlgorithmicShortcut_8::check_each_attacker_has_defender(AF &framework, uint32_t query_argument)
    {
        vector<uint32_t> attackers = framework.attackers[query_argument];
        for (std::vector<unsigned int>::size_type i = 0; i < attackers.size(); i++)
        {
            uint32_t attacker = attackers[i];
            if(framework.attackers[attacker].size() == 0)
            {
                return false;
            }
        }

        return true;
    }

    //===========================================================================================================================================================
    //===========================================================================================================================================================

    void AlgorithmicShortcut_8::create_clauses(AF &framework, uint32_t query_argument, SatSolver &solver)
    {
        // disjunction of all additional z values
        vector<int64_t> clause_all_z;
        // for each attacker do
        vector<uint32_t> attackers = framework.attackers[query_argument];
        for(uint32_t i = 0; i < attackers.size(); i++)
        {
            uint32_t attacker = attackers[i];

            //one z per attacker
            clause_all_z.push_back(Encoding::get_literal_aux(framework, i, true));

            // for each defender against this attacker do
            vector<uint32_t> defenders = framework.attackers[attacker];
            for(uint32_t j = 0; j < defenders.size(); j++)
            {
                uint32_t defender = defenders[j];
                //do not process self-attacks
                if(defender == attacker)
                {
                    continue;
                }
                                
                solver.add_clause_short(Encoding::get_literal_aux(framework, i, false),Encoding::get_literal_rejected(framework, defender, true));
            }
        }

        solver.add_clause(clause_all_z);
    }

