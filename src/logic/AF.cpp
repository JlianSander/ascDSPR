#include "../../include/logic/AF.h"
using namespace std;

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool AF::add_attack(uint32_t attacker, uint32_t victim)
{
	//check that input is valid
	if (attacker == 0 || victim == 0) return false;
	
	//check if attack is already contained
	if (attacks.count(make_pair(attacker, victim))) {
		return false;
	}
	attacks.insert(make_pair(attacker, victim));
	return true;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void AF::clear() {
	attacks.clear();
	attackers.clear();
	victims.clear();
	self_attack.clear();
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

ArrayBitSet AF::create_active_arguments() {
	vector<uint32_t> active_args_vector;
	vector<uint8_t> active_args_bitset(num_args + 1, 1);
	active_args_bitset[0] = false;

	//iterate through the arguments to append them to the vector
	for (std::vector<unsigned int>::size_type i = 0; i < num_args; i++) {
		active_args_vector.push_back(i + 1);
	}

	return ArrayBitSet(active_args_vector, active_args_bitset);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool AF::delete_attack(uint32_t attacker, uint32_t victim) {
	//check that input is valid
	if (attacker == 0 || victim == 0) return false;

	return attacks.erase(make_pair(attacker, victim)) == 1;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool AF::exists_attack(uint32_t attacker, uint32_t victim) const {
	return attacks.count(make_pair(attacker, victim));
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool AF::exists_attack(std::uint32_t argument, std::list<std::uint32_t> &set_arguments) const {
	//iterate through arguments of the set
	for (list<uint32_t>::iterator mIter = set_arguments.begin(); mIter != set_arguments.end(); ++mIter) {
		//check if query argument is victim of the set
		if (exists_attack(*mIter, argument)) {
			return true;
		}
	}

	return false;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void AF::initialize(uint32_t number_args) {
	num_args = number_args;
	attackers.resize(static_cast<uint64_t>(num_args) + 1);
	victims.resize(static_cast<uint64_t>(num_args) + 1);
	self_attack.resize(static_cast<uint64_t>(num_args) + 1);
	std::fill(self_attack.begin(), self_attack.end(), 0);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void AF::finish_initilization()
{
	attackers.clear();
	victims.clear();
	std::fill(self_attack.begin(), self_attack.end(), 0);

	for (const pair<uint32_t, uint32_t> &attack : attacks) {
		int32_t source = attack.first;
		int32_t target = attack.second;
		attackers[target].push_back(source);
		victims[source].push_back(target);

		if (source == target)
			self_attack[source] = true;
	}
}