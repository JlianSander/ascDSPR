#include "../../include/logic/Processor_DS_PR.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

list<uint32_t> Proc_DS_PR::calculate_rejecting_set(uint32_t query_argument, AF &framework, ArrayBitSet &active_args, bool &out_is_rejected, bool &out_is_query_attacked, bool &out_is_complete_pr,
	SatSolver &solver, bool &out_has_solution_without_query, bool is_first_iteration){
	// compute a solution with SATSolver
	out_has_solution_without_query = solver.solve(Encoding::get_literal_accepted(query_argument, false));
	if (!out_has_solution_without_query) {
		//there is no nonempty adm. set, which is not containing the query, there might be solutions containing the query
		if (is_first_iteration && !solver.solve(Encoding::get_literal_accepted(query_argument, true))) {
			// this is the first iteration, so there have been no solution excluded by a complement clause
			// there is no nonempty adm. set, with or without the query argument, that's why there is only the empty set as adm. set
			// which means we found a preferred extension, which is not containing the query argument, hence we found a counter evidence
			out_is_rejected = true;
			out_is_complete_pr = true;
		}
		return list<uint32_t>();
	}
	else {
		//check if calculated CO set attacks query
		list<uint32_t> calculated_set = Decoding::get_set_from_solver(solver, active_args);
		out_is_query_attacked = framework.check_attack(query_argument, calculated_set, framework);
		if (out_is_query_attacked) {
			// found counter-example
			out_is_rejected = true;
			return calculated_set;
		}

		//ensure that solver does not find same solution again
		Encoding::add_complement_clause(solver, active_args);

		//check if set is PR, by checking if reduct has CO set
		for (std::list<uint32_t>::iterator mIter = calculated_set.begin(); mIter != calculated_set.end(); ++mIter) {
			solver.add_assumption(Encoding::get_literal_accepted(*mIter, true));
			solver.add_assumption(Encoding::get_literal_rejected(framework, *mIter, false));
		}
		if (!solver.solve())
		{
			// cannot calculate CO set in reduct, hence set used for reduction has to be a PR set
			// since the PR set does not contain the query, it's a counter-example
			out_is_rejected = true;
			out_is_complete_pr = true;
		}
		else {
			//check if calculated CO extension rejects query
			list<uint32_t> calculated_set_2 = Decoding::get_set_from_solver(solver, active_args);
			out_is_query_attacked = framework.check_attack(query_argument, calculated_set_2, framework);
			if (out_is_query_attacked) {
				// found counter-example
				list<uint32_t> calculated_set_tmp = tools::Tools_List::extend_list(calculated_set, calculated_set_2);
				calculated_set = calculated_set_tmp;
				out_is_rejected = true;
			}
			else {
				//check if calculated CO extension contains query, if so then extend complement clause by the new extension
				//since it is uninteresting to visit the combined extension once again
				if (tools::Tools_List::contains(calculated_set_2, query_argument)) {
					Encoding::add_complement_clause(solver, active_args);
				}
			}
		}
		return calculated_set;
	}
}