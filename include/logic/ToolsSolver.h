#ifndef TOOLS_SOLVER_H
#define TOOLS_SOLVER_H

#include <iostream>
#include <cstdint>
#include <vector>
#include "omp.h"

#include "../util/ArrayBitSet.h"
#include "AF.h"
#include "Decoding.h"
#include "Encoding.h"
#include "SatSolver.h"

#include "../util/Printer.h"
#include "../util/ToolsList.h"

namespace tools {

	/// <summary>
	/// This class is responsible for auxiliary code, used in several different problems adressed by the solver.
	/// </summary>
	class Tools_Solver {
	public:

		/// <summary>
		/// Updates the certificate by extending it by the solution of a specified SatSolver.
		/// </summary>
		/// <param name="solver">The solver, which has calculated a solution.</param>
		/// <param name="active_args">The arguments that are active in the current state of the framework.</param>
		/// <param name="certificate_extension"> The extension used as certificate/proof of the result.</param>
		static void UpdateCertificate(SatSolver *solver, ArrayBitSet &active_args, std::__cxx11::list<uint32_t> &out_certificate_extension);

		/// <summary>
		/// Updates the certificate by extending it by the specified set of arguments.
		/// </summary>
		/// <param name="certificate_extension"> The extension used as certificate/proof of the result.</param>
		/// <param name="set_to_extend_with">Set of arguments, which are appended at the certificate.</param>
		static void UpdateCertificate(std::__cxx11::list<uint32_t> &certificate_extension, std::__cxx11::list<uint32_t> &set_to_extend_with);

		/// <summary>
		/// Checks if there exists a stable extension in the specified framework in the specified state.
		/// </summary>
		/// <param name="framework">The abstract argumentation framework, specifying the underlying attack relations between the arguments.</param>
		/// <param name="active_args">The arguments that are active in the current state of the framework.</param>
		/// <param name="out_certificate_extension"> Extension proving, that there is at least one stable extension.</param>
		/// <returns>TRUE iff a stable extension exists. FALSE otherwise.</returns>
		static bool check_existance_stable_extension(AF &framework, ArrayBitSet &active_args, list<uint32_t> &out_certificate_extension);
	};
};

#endif