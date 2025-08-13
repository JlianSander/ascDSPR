#include "../../include/logic/Solver_GR.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

list<uint32_t> Solver_GR::calculate_grounded_extension(AF &framework, uint32_t query, bool &is_contained, bool &is_attacked, bool stop_if_contained, bool stop_if_attacked)
{
	list<uint32_t> grounded_extension;
	is_contained = false;
	is_attacked = false;
	// fill list with unattacked arguments
	list<uint32_t> ls_unattacked_unprocessed;
	vector<uint32_t> num_attacker;
	num_attacker.resize(framework.num_args + 1);
	//iterate through active arguments
	for (std::vector<unsigned int>::size_type i = 1; i < framework.num_args; i++) {
		uint32_t argument = i;
		//check if argument is unattacked
		if (framework.attackers[argument].empty()) {
			// add unattacked argument to list and to output grounded extension
			ls_unattacked_unprocessed.push_back(argument);
			grounded_extension.push_back(argument);
		}
		// set number of attacker for current argument
		num_attacker[argument] = framework.attackers[argument].size();
	}

	// init variable of current reduct
	ArrayBitSet  reduct = framework.create_active_arguments();
	//process list of unattacked arguments
	for (list<uint32_t>::iterator mIter = ls_unattacked_unprocessed.begin(); mIter != ls_unattacked_unprocessed.end(); ++mIter) {
		const auto &ua = *mIter;
		//check if query is part of grounded extension, if query == 0 then there is no query argument to check for
		if (query != 0 && ua == query) {
			is_contained = true;

			if (stop_if_contained) {
				return grounded_extension;
			}
		}

		//iterate through victims of the unattacked argument
		for (std::vector<unsigned int>::size_type i = 0; i < framework.victims[ua].size(); i++) {
			uint32_t vua = framework.victims[ua][i];
			//only account victims that are still active
			if (!reduct._bitset[vua]) {
				continue;
			}
			//check if query gets attacked by argument of grounded extension, if query == 0 then there is no query argument to check for
			if (query != 0 && vua == query) {
				is_attacked = true;

				if (stop_if_attacked) {
					return grounded_extension;
				}
			}

			//iterate through victims of the victims of unattacked argument
			for (std::vector<unsigned int>::size_type j = 0; j < framework.victims[vua].size(); j++) {
				uint32_t vvua = framework.victims[vua][j];
				//only account victims of victims that are still active
				if (!reduct._bitset[vvua]) {
					continue;
				}

				//update number of attackers
				num_attacker[vvua]--;

				//check if victim of victim is unattacked
				if (num_attacker[vvua] == 0) {
					ls_unattacked_unprocessed.push_back(vvua);
					grounded_extension.push_back(vvua);
				}
			}
		}

		//reduce active argument by unattacked argument + update current reduct
		reduct = Reduct::get_reduct(reduct, framework, ua);
	}

	return grounded_extension;
}

