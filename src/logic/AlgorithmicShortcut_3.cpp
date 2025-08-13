#ifdef ASC_3
    #include "../../include/logic/AlgorithmicShortcut_3.h"

    acceptance_result AlgorithmicShortcut_3::try_solve(AF &framework, uint32_t query_argument)
    {
        bool is_contained, is_attacked;
        Solver_GR::calculate_grounded_extension(framework, query_argument, is_contained, is_attacked, true, true);
        if(is_contained)
        {
            return acceptance_result::accepted;
        } else {
            return acceptance_result::unknown;
        }
    }
#endif