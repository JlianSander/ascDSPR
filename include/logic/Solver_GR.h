#ifndef SOLVER_G_H
#define SOLVER_G_H

#include <iostream>
#include <cstdint>
#include <list>

#include "AF.h"

#include "../logic/Enums.h"
#include "Reduct.h"

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
	/// <param name="query">The query argument, whose acceptance is to be checked. In case that there is no query argument to check for set this parameter to 0.</param>
	/// <param name="is_contained"> If TRUE, then the grounded extension contains the query argument.</param>
	/// <param name="is_attacked"> If TRUE, then the grounded extension attacks the query argument.</param>
	/// <param name="stop_if_contained"> If TRUE, then the method stops when the grounded extension calculated to this point contains the query argument.</param>
	/// <param name="stop_if_attacked"> If TRUE, then the method stops when the grounded extension calculated to this point attacks the query argument.</param>
	/// <returns>The calculated grounded extension of the framework.</returns>
	static list<uint32_t> calculate_grounded_extension(AF &framework, uint32_t query, bool &is_contained, bool &is_attacked, bool stop_if_contained, bool stop_if_attacked);
};
#endif
