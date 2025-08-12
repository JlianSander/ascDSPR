#ifndef SOLVER_SE_ST_H
#define SOLVER_SE_ST_H

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
/// This class is responsible for calculating an extension using the stable semantics.
/// </summary>
class Solver_SE_ST {
public:

	/// <summary>
	/// Checks if an extension can be calculated using the stable semantics.
	/// </summary>
	/// <param name="framework">The abstract argumentation framework, specifying the underlying attack relations between the arguments.</param>
	/// <param name="proof_extension">The calculated stable extension.</param>
	/// <returns>TRUE iff an extension was found. FALSE otherwise.</returns>
	static bool solve(AF &framework, list<uint32_t> &out_certificate_extension);
};

#endif
