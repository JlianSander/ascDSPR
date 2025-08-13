#ifdef ASC_2
    #include "../../include/logic/AlgorithmicShortcut_2.h"

    acceptance_result AlgorithmicShortcut_2::try_solve(AF &framework, uint32_t query_argument)
    {
        if(framework.attackers[query_argument].size() == 0)
        {
            return acceptance_result::accepted;
        } else {
            return acceptance_result::unknown;
        }
    }
#endif