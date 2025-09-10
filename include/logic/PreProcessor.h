#ifndef PREPROC_H
#define PREPROC_H

#include <iostream>
#include <cstdint>
#include <list>
#include <unordered_map>

#include "AF.h"
#include "Reduct.h"

#include "../util/ArrayBitSet.h"

extern "C" {
#include "../util/MemoryWatchDog.h"
}

/// <summary>
/// This class is responsible for preparing data, before the data is used in the actual process of solving the problem.
/// The preprocessor checks if the problem can simplified by replacing or removing parts of the argumentation framework.
/// </summary>
class PreProcessor {
public:

	/// <summary>
	/// Calculates the cone of influence of a specified argumentation framework, starting with a specified argument of that framework.
	/// </summary>
	/// <param name="framework">The abstract argumentation framework, in which the cone if situated</param>
	/// <param name="query">The starting argument of the cone of influence</param>
	/// <param name="">[Output parameter] Maps the arguments of the new framework to the arguments of the old framework. </param>
	/// <returns>A reduct of the framework, containing only those argument, which are relevant for the specified query argument.</returns>
	static AF calculate_cone_influence(AF &framework, uint32_t query, std::unordered_map<uint32_t, uint32_t> &args_new_to_old);
};
#endif
