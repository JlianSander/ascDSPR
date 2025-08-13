#ifndef ALGO_SHORT_H
#define ALGO_SHORT_H

#include "AF.h"
#include "Enums.h"

class AlgorithmicShortcut {
public:
	virtual ~AlgorithmicShortcut() {}
    virtual acceptance_result try_solve(AF &framework, uint32_t query_argument) = 0;
};

#endif