#ifndef DECODINGS_SATSOLVER_H
#define DECODINGS_SATSOLVER_H

#include <cstdint>
#include <list>
#include <unordered_set>

#include "Encoding.h"
#include "SatSolver.h"
#include "Encoding.h"

using namespace std;

/// <summary>
/// This class is responsible to decode a SATProblem, returning a structure of arguments.
/// </summary>
class Decoding {
public:

	/// <summary>
	/// Translates the solution of a specified SatSolver to a set of argument, in the context of a specified set of active arguments.
	/// </summary>
	/// <param name="solver">The SatSolver, which solution is to be translated.</param>
	/// <param name="framework">The framework of the problem.</param>
	/// <returns>Set of arguments, which solves the problem of the specified SatSolver.</returns>
	static list<uint32_t> get_set_from_solver(SatSolver &solver, AF &framework);
};
#endif