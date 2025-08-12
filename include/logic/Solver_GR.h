#ifndef SOLVER_G_H
#define SOLVER_G_H

#include <iostream>
#include <cstdint>
#include <list>

#include "AF.h"
#include "Reduct.h"
#include "ConeOfInfluence.h"
#include "PreProcessor.h"

#include "../util/ArrayBitSet.h"
#include "../logic/Enums.h"

extern "C" {
#include "../util/MemoryWatchDog.h"
}

/// <summary>
/// This class is responsible computing the grounded extension of an argumentation framework.
/// </summary>
class Solver_GR {
public:

	/// <summary>
	/// This method checks if a solution can be easily drawn by reducing the current state of the framework by the grounded extension.
	/// </summary>
	/// <param name="framework">The original abstract argumentation framework of the situation.</param>
	/// <param name="active_args">Current active arguments in the framework.</param>
	/// <param name="query">The query argument, whose acceptance is to be checked. In case that there is no query argument to check for set this parameter to 0.</param>
	/// <param name="break_acception"> If TRUE, the preprocessing will abort the process, in case the grounded extension contains the query argument.</param>
	/// <param name="break_rejection"> If TRUE, the preprocessing will abort the process, in case the grounded extension attacks the query argument.</param>
	/// <param name="out_reduct">[Output-Parameter]The set of active arguments, which remain of the original framework after the preprocessor is finished.</param>
	/// <param name="out_gr_extension">[Output-Parameter] The calculated grounded extension of the framework.</param>
	/// <returns>Returns an Enum indicating if the method has solved the problem, and if so to which conclusion it came.</returns>
	static acceptance_result reduce_by_grounded(AF &framework, ArrayBitSet &active_args, uint32_t query, bool break_acception, bool break_rejection,
		ArrayBitSet &out_reduct, list<uint32_t> &out_gr_extension);
};
#endif
