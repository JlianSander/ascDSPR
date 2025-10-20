
#include "../../include/logic/AlgorithmicShortcut_4.h"

acceptance_result AlgorithmicShortcut_4::try_solve(AF &framework, uint32_t query_argument)
{
    bool is_contained, is_attacked;
    Solver_GR::calculate_grounded_extension(framework, query_argument, is_contained, is_attacked, true, true);
    if(is_attacked)
    {
        return acceptance_result::rejected;
    } else {
        return acceptance_result::unknown;
    }
}
