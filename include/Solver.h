/* #ifndef SOLVER_H
#define SOLVER_H

#include <vector>
#include <unordered_map>
#include <string>
#include <cstdint>

#include "Main.h"
#include "../include/util/ToolsList.h"

class Solver {
public:
	Solver();
	void set_query(uint32_t arg);
	void set_semantics(semantics sem);
	void add_argument(uint32_t arg);
	void add_attack(uint32_t attacker, uint32_t victim);
	void delete_argument(uint32_t arg);
	void delete_attack(uint32_t attacker, uint32_t victim);
	int32_t solve(bool credulous_mode);

private:
	AF _framework;
	uint32_t _query_argument;
	semantics _semantics;

	std::vector<uint32_t> _int_to_arg;
	std::unordered_map<uint32_t, uint32_t> _arg_to_int;
	bool _is_initialized;
};

extern "C" {

#include "ipafair.h"

	static Solver * import(void *s) { return (Solver *)s; }
	const char *ipafair_signature() { return "ICCMA'25"; }
	void *ipafair_init() { return new Solver(); }
	void ipafair_release(void *s) { delete import(s); }
	void ipafair_set_semantics(void *s, semantics sem) { import(s)->set_semantics(sem); }
	void ipafair_add_argument(void *s, int32_t a) { import(s)->add_argument(a); }
	void ipafair_add_attack(void *s, int32_t a, int32_t b) { import(s)->add_attack(a, b); }
	void ipafair_del_argument(void *s, int32_t a) { import(s)->delete_argument(a); }
	void ipafair_del_attack(void *s, int32_t a, int32_t b) { import(s)->delete_attack(a, b); }
	void ipafair_assume(void *s, int32_t a) { import(s)->set_query(a); }
	int32_t ipafair_solve_cred(void *s) { return import(s)->solve(true); }
	int32_t ipafair_solve_skept(void *s) { return import(s)->solve(false); }
	int32_t ipafair_val(void *s, int32_t a) { cout << "Not Supported."; return -1; }
};


#endif
 */