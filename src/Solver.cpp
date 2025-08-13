#include "../include/Solver.h"

Solver::Solver(){
	_framework = AF();
	_query_argument = 0;
	_semantics = admissible;
	_int_to_arg = std::vector<uint32_t>();
	_arg_to_int = std::unordered_map<uint32_t, uint32_t>();
	_is_initialized = false;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Solver::add_argument(uint32_t arg)
{
	_int_to_arg.push_back(arg);
	_arg_to_int.insert(make_pair(_int_to_arg.size() - 1, arg));
	_framework.initialize(_int_to_arg.size());
	_is_initialized = false;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Solver::add_attack(uint32_t arg_attacker, uint32_t arg_victim) {
	uint32_t attacker = _arg_to_int[arg_attacker];
	uint32_t victim = _arg_to_int[arg_victim];

	//check if attack is already contained
	if (_framework.exists_attack(attacker, victim)) return;

	_framework.add_attack(attacker, victim);
	_is_initialized = false;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Solver::delete_argument(uint32_t arg) {
	uint32_t argument_delete = _arg_to_int[arg];
	_arg_to_int.erase(arg);
	for (uint32_t i = argument_delete; i < _int_to_arg.size() - 1; i++) {
		uint32_t _next_arg = _int_to_arg[i + 1];
		_int_to_arg[i] = _next_arg;
		_arg_to_int[_next_arg] = i;
	}
	_int_to_arg.erase(_int_to_arg.end());

	_framework.initialize(_int_to_arg.size());
	_is_initialized = false;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Solver::delete_attack(uint32_t arg_attacker, uint32_t arg_victim) {
	uint32_t attacker = _arg_to_int[arg_attacker];
	uint32_t victim = _arg_to_int[arg_victim];
	
	_framework.delete_attack(attacker, victim);
	_is_initialized = false;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Solver::set_query(uint32_t arg) {
	_query_argument = _arg_to_int[arg];
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Solver::set_semantics(semantics sem) {
	_semantics = sem;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

int32_t Solver::solve(bool credulous_mode) {
	if (_query_argument == 0) {
		return -1;
	}

	if (!_is_initialized) {
		_framework.finish_initilization();
	}

	acceptance_result result = acceptance_result::unknown;
	if(credulous_mode) {
		cerr << _semantics << ": Unsupported problem\n";
		return -1;
	}
	else {
		switch (_semantics) {
		case preferred:
			ALGO_SHORT_T shortcut;
			result = shortcut.try_solve(_framework, _query_argument);
			break;
		default:
			cerr << _semantics << ": Unsupported semantics\n";
			return -1;
		}
	}

	switch (result) {
	case acceptance_result::accepted:
		return 10;
	case acceptance_result::rejected:
		return 20;
	default:
		return -1;
	}
}