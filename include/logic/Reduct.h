#ifndef REDUCT_H
#define REDUCT_H

#include <vector>
#include <unordered_set>
#include <cstdint>
#include <iterator>
#include <list>

#include "AF.h"

#include "../util/ArrayBitSet.h"

using namespace std;

/// <summary>
/// This class is responsible for reducing a state of an abstract argumentation framework by a set of arguments.
/// </summary>
class Reduct {

public:
	/// <summary>
	/// Reduces the state of the specified framework by the specified argument. Which means setting the argument and all its victims to "not active".
	/// The state of the framework is defined by the specified set of active arguments.
	/// </summary>
	/// <param name="activeArguments">Set of arguments, which are active in the current transition state of the framework.</param>
	/// <param name="framework">The framework to reduce.</param>
	/// <param name="argument">The argument, by which the framework will be reduced.</param>
	/// <returns>Set of active arguments in the new transition state after the reduction.</returns>
	static ArrayBitSet get_reduct(ArrayBitSet &activeArguments, AF &framework, uint32_t argument);

	/// <summary>
	/// Reduces the state of the specified framework by the specified set of arguments. Which means setting the argument of the set and all their victims to "not active".
	/// The state of the framework is defined by the specified set of active arguments.
	/// </summary>
	/// <param name="activeArguments">Set of arguments, which are active in the current transition state of the framework.</param>
	/// <param name="framework">The framework to reduce.</param>
	/// <param name="set_arguments">The set of argument, by which the framework will be reduced.</param>
	/// <returns>Set of active arguments in the new transition state after the reduction.</returns>
	static ArrayBitSet get_reduct_set(ArrayBitSet &activeArguments, AF &framework, list<uint32_t> &set_arguments);
};

#endif
