#ifndef ALGO_SHORT_H
#define ALGO_SHORT_H

#include "AF.h"
#include "Enums.h"

class AlgorithmicShortcut {
public:
	~AlgorithmicShortcut() {}
    acceptance_result try_solve(AF &framework, uint32_t query_argument) { return acceptance_result::unknown; }
};

#endif