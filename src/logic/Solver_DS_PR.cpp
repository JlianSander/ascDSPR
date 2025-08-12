#include "../../include/logic/Solver_DS_PR.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

/// <summary>
/// This method searched for complete sets in a specified state of a framework, which attack the specified query argument
/// </summary>
static bool search_complete_sets_in_state(AF &framework, ArrayBitSet &reduct, uint32_t query_argument,	
	std::__cxx11::list<uint32_t> &out_certificate_extension, bool &is_query_attacked, bool &is_complete_pr)
{
	// initialize SATSolver
	SatSolver *solver = NULL;
	solver = new SatSolver();
	// add encoding for nonempty complete sets to the SATSolver
	Encoding::add_clauses_nonempty_complete_set(*solver, framework, reduct);
	bool continue_calculation = false;
	bool is_rejected = false;
	// calculate a set of arguments by solving the SAT problem
	list<uint32_t> calculated_set = Proc_DS_PR::calculate_rejecting_set(query_argument, framework, reduct, is_rejected, is_query_attacked, is_complete_pr,
		*solver, continue_calculation, true);
	// update the certificate if such a set was found
	if (is_rejected) {
		tools::Tools_Solver::UpdateCertificate(out_certificate_extension, calculated_set);
	}
	// iterate through all possible sets in the state
	while (continue_calculation && !is_rejected) {
		// calculate a set of arguments by solving the SAT problem
		calculated_set = Proc_DS_PR::calculate_rejecting_set(query_argument, framework, reduct, is_rejected, is_query_attacked, is_complete_pr,
			*solver, continue_calculation, false);
		// update the certificate if such a set was found
		if (is_rejected) {
			tools::Tools_Solver::UpdateCertificate(out_certificate_extension, calculated_set);
		}
	}
	delete solver;
	return !is_rejected;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

/// <summary>
/// This method completes the preferred extension used as an certificate
/// </summary>
static void complete_certificate(AF &framework, list<uint32_t> &out_certificate_extension) {
	// get the original state of the framework
	ArrayBitSet original_active_args = framework.create_active_arguments();
	// reduce the original state by the extension found so far
	ArrayBitSet reduct = out_certificate_extension.empty() ? original_active_args : Reduct::get_reduct_set(original_active_args, framework, out_certificate_extension);
	// abort if no active argument is left
	if (reduct._array.empty()) {
		return;
	}
	// use the algorithm for the SE-PR problem to compute a preferred extension in the reduct
	list<uint32_t> extension_outside_certificate;
	bool has_extension_outside_certificate = Solver_SE_PR::solve(framework, reduct, extension_outside_certificate);
	// update the certificate if such a set was found
	if (has_extension_outside_certificate) {
		tools::Tools_Solver::UpdateCertificate(out_certificate_extension, extension_outside_certificate);
	}
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static acceptance_result apply_shortcuts(AF &framework, uint32_t query_argument, ArrayBitSet &out_reduct, std::__cxx11::list<uint32_t> &out_grounded_extension)
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
	return Solver_GR::reduce_by_grounded(framework, initial_actives, query_argument, true, true, out_reduct, out_grounded_extension);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool Solver_DS_PR::solve(uint32_t query_argument, AF &framework, list<uint32_t> &out_certificate_extension)
{
	// initialize variables
	ArrayBitSet reduct_after_grounded = ArrayBitSet();
	switch (apply_shortcuts(framework, query_argument, reduct_after_grounded, out_certificate_extension)) {
		case accepted:
			return true;

		case rejected:
			// complete certificate if it does not attack the query
			if (!framework.check_attack(query_argument, out_certificate_extension, framework)) {
				complete_certificate(framework, out_certificate_extension);
			}
			return false;

		default:
			bool is_query_attacked = false;
			bool is_complete_pr = false;
			bool is_skeptically_accepted = search_complete_sets_in_state(framework, reduct_after_grounded, query_argument, out_certificate_extension, is_query_attacked, is_complete_pr);

			// if skeptical acceptance of query got rejected, but query is not attacked by certificate and the certificate is not a complete preferred set,
			// then extend certificate to get a complete preferred extension of the original framework
			if (!is_skeptically_accepted && !is_query_attacked && !is_complete_pr) {
				complete_certificate(framework, out_certificate_extension);
				return is_skeptically_accepted;
			}

			return is_skeptically_accepted;
	}
}