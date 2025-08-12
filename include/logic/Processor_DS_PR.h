#ifndef PROC_DS_PR_H
#define PROC_DS_PR_H

#include <cstdint>
#include <list>
#include "omp.h"

#include "Encoding.h"
#include "Decoding.h"
#include "SatSolver.h"

#include "../util/ArrayBitSet.h"
#include "../util/ToolsList.h"

using namespace std;

/// <summary>
/// This class is responsible for processing solving steps for the DS-PR problem.
/// </summary>
class Proc_DS_PR {

public:
	/// <summary>
	/// This method calculates a nonemtpy set which attacks the specified query argument, if such a set can be calculated in the specified reduct, using the specified solver.
	/// </summary>
	/// <param name="query_argument">The query argument of the DS-PR problem</param>
	/// <param name="framework">The abstract argumentation framework of the problem.</param>
	/// <param name="active_args">The arguments that are active in the current state of the framework.</param>
	/// <param name="out_is_rejected">[Output-Parameter] Flag used to signal that the argument is rejected.</param>
	/// <param name="out_is_query_attacked">[Output-Parameter] Flag used to signal if the calculated set of arguments attacks the query argument.</param>
	/// <param name="out_is_complete_pr">[Output-Parameter] Flag used to signal if the calculated set of arguments is a complete preferred extension.</param>
	/// <param name="solver">The solver used to calculate sets for this state of the framework.</param>
	/// <param name="out_has_solution_without_query">[Output-Parameter] Flag used to signal if the solver could calculate a solution.</param>
	/// <param name="is_first_iteration">Flag indicating if this iteration to calculate a set is the first in the specified state of the framework.</param>
	/// <returns>An non emtpy set, if such a set can be computed. Empty list otherwise.</returns>
	static list<uint32_t> calculate_rejecting_set(uint32_t query_argument, AF &framework, ArrayBitSet &active_args, bool &out_is_rejected, bool &out_is_query_attacked, bool &out_is_complete_pr,
		SatSolver &solver, bool &out_has_solution_without_query, bool is_first_iteration);
};
#endif