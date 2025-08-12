#include "../../include/logic/Solver_SE_ST.h"
/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static bool start_checking(AF &framework, ArrayBitSet &active_args, list<uint32_t> &out_certificate_extension)
{
	// initialize SATSolver
	SatSolver *solver = NULL;
	solver = new SatSolver();
	// add encoding for nonempty stable sets
	Encoding::add_clauses_nonempty_stable_set(*solver, framework, active_args);
	// compute a solution with the SATSolver
	bool has_solution = (*solver).solve();
	// update the certificate if a solution was found
	if (has_solution) {
		tools::Tools_Solver::UpdateCertificate(solver, active_args, out_certificate_extension);
	}

	delete solver;
	return has_solution;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool Solver_SE_ST::solve(AF &framework, list<uint32_t> &out_certificate_extension)
{
	ArrayBitSet active_args = framework.create_active_arguments();
	ArrayBitSet reduct_after_grounded = ArrayBitSet();
	Solver_GR::reduce_by_grounded(framework, active_args, 0, true, true, reduct_after_grounded, out_certificate_extension);

	//check if grounded extension is stable
	if (reduct_after_grounded._array.size() == 0) {
		//reduct is empty, therefore grounded extension is only stable extension
		return true;
	}

	return start_checking(framework, reduct_after_grounded, out_certificate_extension);
}