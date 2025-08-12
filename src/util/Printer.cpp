#include "../../include/util/Printer.h"

using namespace std;

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Printer::print_list(list<uint32_t> &listToPrint) {

	if (listToPrint.empty()) {
		return;
	}

	// iterate through list and print elements
	cout << *listToPrint.begin();
	for (list<uint32_t>::iterator mIter = std::next(listToPrint.begin()); mIter != listToPrint.end(); ++mIter) {
		cout << " " << *mIter;
	}
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Printer::print_set(unordered_set<uint32_t> &setToPrint) {

	if (setToPrint.empty()) {
		return;
	}

	bool isFirst = true;

	// iterate through buckets
	for (size_t bno = 0; bno < setToPrint.bucket_count(); ++bno) {
		// iterate through content of a bucket
		for (auto bit = setToPrint.begin(bno), end = setToPrint.end(bno); bit != end; ++bit) {
			
			if (isFirst) {
				isFirst = false;
				cout << *bit;
			}
			else {
				cout << " " << *bit;
			}
			
		}
	}
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Printer::print_vector(vector<uint32_t> &vector) {
	if (vector.empty()) {
		return;
	}

	cout << vector[0];
	// iterate through content of vector
	for (std::vector<unsigned int>::size_type i = 1; i < vector.size(); i++) {
		cout << " " << vector[i];
	}
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Printer::print_vector(vector<int64_t> &vector) {
	if (vector.empty()) {
		return;
	}

	cout << vector[0];
	// iterate through content of vector
	for (std::vector<unsigned int>::size_type i = 1; i < vector.size(); i++) {
		cout << " " << vector[i];
	}
}