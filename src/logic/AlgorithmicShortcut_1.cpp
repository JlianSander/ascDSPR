
#include "../../include/logic/AlgorithmicShortcut_1.h"

acceptance_result AlgorithmicShortcut_1::try_solve(AF &framework, uint32_t query_argument)
{
    if(framework.self_attack[query_argument])
    {
        return acceptance_result::rejected;
    } else {
         return acceptance_result::unknown;
    }
}
