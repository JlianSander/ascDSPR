#include "../../include/logic/Decoding.h"

using namespace std;
using std::vector;

list<uint32_t> Decoding::get_set_from_solver(SatSolver &solver, AF &framework)
{
	list<uint32_t> output;

	//iterate through active arguments to check if argument is set in model
	for (std::vector<unsigned int>::size_type i = 1; i < framework.num_args; i++) {
		uint32_t argument = i;
		if (solver.check_var_model(Encoding::get_literal_accepted(argument, true)))
		{
			output.push_back(argument);
		}
	}

	return output;
}