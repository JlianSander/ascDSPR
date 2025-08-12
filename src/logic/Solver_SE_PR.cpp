#include "../../include/logic/Solver_SE_PR.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool Solver_SE_PR::solve(AF &framework, ArrayBitSet &active_args, list<uint32_t> &out_certificate_extension)
{
	//calculate grounded extension to simplify the problem
	ArrayBitSet reduct_after_grounded = ArrayBitSet();
	Solver_GR::reduce_by_grounded(framework, active_args, 0, true, true, reduct_after_grounded, out_certificate_extension);

	// initialize the SATSolver
	SatSolver *solver = NULL;
	solver = new SatSolver();
	list<uint32_t> calculated_extension;
	// add an encoding for a nonempty complete set to the SATSolver
	Encoding::add_clauses_nonempty_complete_set(*solver, framework, reduct_after_grounded);
	bool has_solution = (*solver).solve();
	// extend the complete extension to get preferred extension
	// by repeating the process until no nonempty complete set can not be found anymore
	while (has_solution) {
		// get the calculated extension
		calculated_extension.clear();
		calculated_extension = Decoding::get_set_from_solver(*solver, reduct_after_grounded);

		//ensure that solver does not find same solution again
		Encoding::add_complement_clause(*solver, reduct_after_grounded);

		// reduce the current state by the calculated extension
		for (std::list<uint32_t>::iterator mIter = calculated_extension.begin(); mIter != calculated_extension.end(); ++mIter) {
			solver->add_clause_short(Encoding::get_literal_accepted(*mIter, true), 0);
			solver->add_clause_short(Encoding::get_literal_rejected(framework, *mIter, false), 0);
		}

		has_solution = (*solver).solve();
		//if has_solution == false, then no more complete set can be calculated, therefor extension found so far cannot be extended, and is therefor preferred
	}

	// get certificate
	tools::Tools_Solver::UpdateCertificate(out_certificate_extension, calculated_extension);

	delete solver;
	return true;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool Solver_SE_PR::solve(AF &framework, list<uint32_t> &out_certificate_extension)
{
	ArrayBitSet active_args = framework.create_active_arguments();
	return solve(framework, active_args, out_certificate_extension);
}