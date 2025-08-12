#ifndef SOLVER_SE_PR_H
#define SOLVER_SE_PR_H

#include <iostream>
#include <cstdint>
#include <vector>
#include "omp.h"

#include "AF.h"
#include "Decoding.h"
#include "Encoding.h"
#include "Enums.h"
#include "Solver_GR.h"
#include "Reduct.h"
#include "SatSolver.h"
#include "ToolsSolver.h"

#include "../util/Printer.h"
#include "../util/ToolsList.h"

using namespace std;

/// <summary>
/// This class is responsible for calculating an extension using the preferred semantics.
/// </summary>
class Solver_SE_PR {
public:

	/// <summary>
	/// Checks if an extension can be calculated using the preferred semantics.
	/// </summary>
	/// <param name="framework">The abstract argumentation framework, specifying the underlying attack relations between the arguments.</param>
	/// <param name="out_certificate_extension"> The calculated preferred extension.</param>
	/// <returns>TRUE iff an extension was found. FALSE otherwise.</returns>
	static bool solve(AF &framework, list<uint32_t> &out_certificate_extension);

	/// <summary>
	/// Checks if an extension can be calculated in the specified reduct of the framework using the preferred semantics.
	/// </summary>
	/// <param name="framework">The abstract argumentation framework, specifying the underlying attack relations between the arguments.</param>
	/// <param name="reduct">The set of active arguments, used to describe the state of the specified argumentation framework.</param>
	/// <param name="out_certificate_extension"> The calculated preferred extension.</param>
	/// <returns>TRUE iff an extension was found. FALSE otherwise.</returns>
	static bool solve(AF &framework, ArrayBitSet &reduct, list<uint32_t> &out_certificate_extension);
};

#endif