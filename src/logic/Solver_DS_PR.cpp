#include "../../include/logic/Solver_DS_PR.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static acceptance_result apply_shortcuts(AF &framework, uint32_t query_argument)
{
	if (framework.self_attack[query_argument])
	{
		return acceptance_result::rejected;
	}

	if (framework.attackers[query_argument].empty())
	{
		return acceptance_result::accepted;
	}

	ArrayBitSet initial_actives = framework.create_active_arguments();
	bool is_contained_in_GR, is_attack_by_GR;
	Solver_GR::calculate_grounded_extension(framework, query_argument, is_contained_in_GR, is_attack_by_GR, true, true);
	if(is_contained_in_GR) return acceptance_result::accepted;
	if(is_attack_by_GR) return acceptance_result::rejected;
	return acceptance_result::unknown;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool Solver_DS_PR::solve(AF &framework, uint32_t query_argument)
{
	// initialize variables
	switch (apply_shortcuts(framework, query_argument)) {
		case accepted:
			return true;

		case rejected:
			return false;

		default:
			return false;
	}
}