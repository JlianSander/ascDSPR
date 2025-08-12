#include "../../include/logic/Decoding.h"

using namespace std;
using std::vector;

list<uint32_t> Decoding::get_set_from_solver(SatSolver &solver, ArrayBitSet &activeArgs)
{
	list<uint32_t> output;

	//iterate through active arguments to check if argument is set in model
	for (std::vector<unsigned int>::size_type i = 0; i < activeArgs._array.size(); i++) {
		if (solver.check_var_model(Encoding::get_literal_accepted(activeArgs._array[i], true)))
		{
			output.push_back(activeArgs._array[i]);
		}
	}

	return output;
}