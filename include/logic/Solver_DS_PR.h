#ifndef SOLVER_DS_PR_H
#define SOLVER_DS_PR_H

#include <iostream>
#include <cstdint>
#include <string_view>
#include <functional>
#include <vector>
#include <queue>

extern "C" {
	#include "../util/MemoryWatchDog.h"
}

#include "AF.h"
#include "Decoding.h"
#include "Encoding.h"
#include "Enums.h"
#include "Solver_GR.h"
#include "Reduct.h"
#include "SatSolver.h"

#include "../util/Printer.h"
#include "../util/ToolsList.h"

using namespace std;

/// <summary>
/// This class is responsible for deciding about the sceptical acceptance of an query-argument
/// using the preferred semantics.
/// </summary>
class Solver_DS_PR {
public:

	/// <summary>
	/// Checks if a specified argument is sceptically accepted using the preferred semantics.
	/// </summary>
	/// <param name="framework">The abstract argumentation framework, specifying the underlying attack relations between the arguments.</param>
	/// <param name="query_argument">The argument, which could be accepted or not.</param>
	/// <returns>TRUE iff the argument is sceptically accepted. FALSE otherwise.</returns>
	static bool solve(AF &framework, uint32_t query_argument);
};

#endif