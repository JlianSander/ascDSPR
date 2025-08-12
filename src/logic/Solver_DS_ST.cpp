#include "../../include/logic/Solver_DS_ST.h"
/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

/// <summary>
///  This method is used to check the skeptical acceptance after the framework has been preprocessed
/// </summary>
static bool check_for_stable_extension_without_query(uint32_t query_argument, AF &framework, ArrayBitSet &active_args, list<uint32_t> &out_certificate_extension)
{
	// initialise the SATSolver
	SatSolver *solver = NULL;
	solver = new SatSolver();
	// add an encoding for nonempty stable sets
	Encoding::add_clauses_nonempty_stable_set(*solver, framework, active_args);
	// compute a solution with the SATSolver
	bool has_solution_without_query = (*solver).solve(Encoding::get_literal_accepted(query_argument, false),
		Encoding::get_literal_rejected(framework, query_argument, true));
	// update the certificate iff a solution was found
	if (has_solution_without_query) {
		tools::Tools_Solver::UpdateCertificate(solver, active_args, out_certificate_extension);
	}
	//only two cases remain: 1. no stable solution is computable; 2. all stable solutions contain the query; both cases lead to scetical acceptance
		
	delete solver;
	return has_solution_without_query;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static acceptance_result apply_shortcuts(AF &framework, uint32_t query_argument, ArrayBitSet &out_reduct, std::__cxx11::list<uint32_t> &out_grounded_extension)
{
	if (framework.attackers[query_argument].empty())
	{
		return acceptance_result::accepted;
	}

	ArrayBitSet active_args = framework.create_active_arguments();
	return Solver_GR::reduce_by_grounded(framework, active_args, query_argument, true, false, out_reduct, out_grounded_extension);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool Solver_DS_ST::solve(uint32_t query_argument, AF &framework, list<uint32_t> &out_certificate_extension)
{
	ArrayBitSet reduct_after_grounded = ArrayBitSet();
	switch (apply_shortcuts(framework, query_argument, reduct_after_grounded, out_certificate_extension)) {
	case accepted:
		return true;

	case rejected:
		if (reduct_after_grounded._array.size() == 0) {
			//calculated grounded extension is the stable extension
			return false;
		}

		return !check_for_stable_extension_without_query(query_argument, framework, reduct_after_grounded, out_certificate_extension);

	default:
		

		return !check_for_stable_extension_without_query(query_argument, framework, reduct_after_grounded, out_certificate_extension);
	}
}