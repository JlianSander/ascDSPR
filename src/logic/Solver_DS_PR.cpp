#include "../../include/logic/Solver_DS_PR.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static acceptance_result apply_shortcuts(AF &framework, uint32_t query_argument, ArrayBitSet &out_reduct)
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
	std::__cxx11::list<uint32_t> out_grounded_extension;
	return Solver_GR::reduce_by_grounded(framework, initial_actives, query_argument, true, true, out_reduct, out_grounded_extension);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool Solver_DS_PR::solve(AF &framework, uint32_t query_argument)
{
	// initialize variables
	ArrayBitSet reduct_after_grounded = ArrayBitSet();
	switch (apply_shortcuts(framework, query_argument, reduct_after_grounded)) {
		case accepted:
			return true;

		case rejected:
			return false;

		default:
			return false;
	}
}