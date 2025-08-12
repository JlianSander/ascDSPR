#include "../../include/util/ToolsList.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

std::list<uint32_t> tools::Tools_List::extend_list(std::list<uint32_t> &listA, std::list<uint32_t> &listB)
{
	std::list<uint32_t> tmpCopy_1, tmpCopy_2;
	std::copy(listA.begin(), listA.end(), std::back_inserter(tmpCopy_1));
	std::copy(listB.begin(), listB.end(), std::back_inserter(tmpCopy_2));
	tmpCopy_1.merge(tmpCopy_2);
	return tmpCopy_1;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void tools::Tools_List::copy_in_list(std::list<uint32_t> &list_dest, std::vector<uint32_t> vector_source) {
	std::list<uint32_t>::iterator it = list_dest.begin();
	list_dest.insert(it, vector_source.begin(), vector_source.end());
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/
bool tools::Tools_List::contains(std::list<uint32_t> list_input, uint32_t query) {
	// iterate through elements of the list
	for (std::list<uint32_t>::iterator mIter = list_input.begin(); mIter != list_input.end(); ++mIter) {
		if (*mIter == query) {
			return true;
		}
	}

	return false;
}