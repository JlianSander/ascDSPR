#include "../../include/logic/ToolsSolver.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void tools::Tools_Solver::UpdateCertificate(SatSolver *solver, ArrayBitSet &active_args, std::__cxx11::list<uint32_t> &out_certificate_extension)
{
	list<uint32_t> calculated_extension = Decoding::get_set_from_solver(*solver, active_args);
	Tools_Solver::UpdateCertificate(out_certificate_extension, calculated_extension);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void tools::Tools_Solver::UpdateCertificate(std::__cxx11::list<uint32_t> &out_certificate_extension, std::__cxx11::list<uint32_t> &set_to_extend_with)
{
	list<uint32_t> new_certificate = tools::Tools_List::extend_list(out_certificate_extension, set_to_extend_with);
	out_certificate_extension = new_certificate;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool tools::Tools_Solver::check_existance_stable_extension(AF &framework, ArrayBitSet &active_args, list<uint32_t> &out_certificate_extension) {
	// initialize the SATSolver
	SatSolver *solver = NULL;
	solver = new SatSolver();
	// add encoding for nonempty stable sets
	Encoding::add_clauses_nonempty_stable_set(*solver, framework, active_args);
	// compute a solution
	bool has_solution = (*solver).solve();
	// update certificate if solution was found
	if (has_solution) {
		Tools_Solver::UpdateCertificate(solver, active_args, out_certificate_extension);
	}

	delete solver;
	return has_solution;
}