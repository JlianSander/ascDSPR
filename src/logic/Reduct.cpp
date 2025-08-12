#include "../../include/logic/Reduct.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

ArrayBitSet Reduct::get_reduct(ArrayBitSet &activeArguments, AF &framework, uint32_t argument)
{
	// initialize variables
	vector<uint32_t> reduct_vector;
	vector<uint8_t> reduct_bitset;
	reduct_bitset.resize(static_cast<uint64_t>(framework.num_args) + 1);
	// iterate through all active arguments
	for (std::vector<unsigned int>::size_type i = 0; i < activeArguments._array.size(); i++) {
		// ignore the argument and the victims of the argument
		if (activeArguments._array[i] == argument || framework.exists_attack(argument, activeArguments._array[i])){
			continue;
		}
		// add all argument not attacked by the argument to the set of still active arguments
		reduct_vector.push_back(activeArguments._array[i]);
		reduct_bitset[activeArguments._array[i]] = true;
	}

	return ArrayBitSet(reduct_vector, reduct_bitset);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

ArrayBitSet Reduct::get_reduct_set(ArrayBitSet &activeArguments, AF &framework, list<uint32_t> &set_arguments)
{
	if (set_arguments.empty()) {
		cout << "get_reduct_set:: set of arguments is empty get_reduct_set" << endl;
		throw new exception;
	}

	// reduce the framework by the first argument of the set
	ArrayBitSet reduct = get_reduct(activeArguments, framework, *set_arguments.begin());
	if (reduct._array.empty()) {
		return reduct;
	}
	// iterate through the specified set of arguments
	for (list<uint32_t>::iterator mIter = std::next(set_arguments.begin()); mIter != set_arguments.end(); ++mIter) {
		// abort method if calculated reduct is already empty
		if (reduct._array.empty())
		{
			break;
		}

		// reduce the framework by the current argument of the set
		ArrayBitSet reduct_tmp = get_reduct(reduct, framework, *mIter);
		reduct.clear();
		reduct = reduct_tmp;
	}

	return reduct;
}