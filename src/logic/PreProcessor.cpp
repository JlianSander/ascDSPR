#include "../../include/logic/PreProcessor.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void add_arg_to_cone(std::__cxx11::list<uint32_t> &ls_args_unprocessed, std::vector<uint8_t> &active_args_bitset, 
	uint32_t &out_num_args_new, std::unordered_map<uint32_t, uint32_t> &out_args_new_to_old, std::unordered_map<uint32_t, uint32_t> &out_args_old_to_new, uint32_t &argument)
{
	active_args_bitset[argument] = true;
	out_num_args_new++;
	out_args_new_to_old[out_num_args_new] = argument;
	out_args_old_to_new[argument] = out_num_args_new;
	ls_args_unprocessed.push_back(argument);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static AF create_framework(AF &framework_old, vector<uint8_t> &active_args_bitset, uint32_t num_args_new,
	std::unordered_map<uint32_t, uint32_t> &args_new_to_old, std::unordered_map<uint32_t, uint32_t> &args_old_to_new) {
	AF framework_new = AF();
	framework_new.initialize(num_args_new);
	//iterate through new framework and add all attacks of the old framework
	for (std::vector<unsigned int>::size_type i = 1; i < framework_new.num_args + 1; i++) {
		uint32_t argument_new = i;
		uint32_t argument_old = args_new_to_old[argument_new];
		// iterate through attackers of the current argument
		for (std::vector<unsigned int>::size_type j = 0; j < framework_old.attackers[argument_old].size(); j++) {
			uint32_t attacker_old = framework_old.attackers[argument_old][j];
			uint32_t attacker_new = args_old_to_new[attacker_old];
			framework_new.add_attack(attacker_new, argument_new);
		}
	}
	framework_new.finish_initilization();
	return framework_new;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

AF PreProcessor::calculate_cone_influence(AF &framework, uint32_t query, std::unordered_map<uint32_t, uint32_t> &out_args_new_to_old) {
	// initialize variables
	vector<uint8_t> active_args_bitset(framework.num_args + 1, 0);
	uint32_t num_args_new = 0;
	list<uint32_t> ls_args_unprocessed;
	std::unordered_map<uint32_t, uint32_t> args_old_to_new = std::unordered_map<uint32_t, uint32_t>();
	// start list with query
	add_arg_to_cone(ls_args_unprocessed, active_args_bitset, num_args_new, out_args_new_to_old, args_old_to_new, query);

	// iterate through list as long as it has elements
	for (list<uint32_t>::iterator mIter = ls_args_unprocessed.begin(); mIter != ls_args_unprocessed.end(); ++mIter) {
		const auto &argument = *mIter;
		// iterate through attackers of the current argument
		for (std::vector<unsigned int>::size_type i = 0; i < framework.attackers[argument].size(); i++) {
			uint32_t attacker = framework.attackers[argument][i];
			if (active_args_bitset[attacker]) {
				// attacker was already visited
				continue;
			}

			// add attacker to the cone of influence
			add_arg_to_cone(ls_args_unprocessed, active_args_bitset, num_args_new, out_args_new_to_old, args_old_to_new, attacker);
		}
	}

	return create_framework(framework, active_args_bitset, num_args_new, out_args_new_to_old, args_old_to_new);
}