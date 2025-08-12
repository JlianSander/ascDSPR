#include "../../include/logic/ConeOfInfluence.h"

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

ConeOfInfluence::ConeOfInfluence(AF &framework) {
	Distance_to_query.resize(static_cast<uint64_t>(framework.num_args) + 1);
	//initialize distances with 0
	std::fill(Distance_to_query.begin(), Distance_to_query.end(), 0);
	Max_distance = 0;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

ArgumentDistancePair::ArgumentDistancePair(uint32_t _argument, ConeOfInfluence &coi) {
	Argument = _argument;
	Distance_to_query = coi.Distance_to_query[_argument];
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool ArgumentDistancePair::compare_by_distance(ArgumentDistancePair &firstElem, ArgumentDistancePair &secondElem) {
	return firstElem.Distance_to_query >= secondElem.Distance_to_query;
}