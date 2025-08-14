#include "../../include/logic/Encoding.h"
#include "Encoding.h"

using namespace std;
using std::vector;

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

int64_t Encoding::get_literal_accepted(uint32_t argument, bool isPositive)
{
	int64_t variable = static_cast<int64_t>(argument);
	return isPositive ? variable : -1 * variable;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

int64_t Encoding::get_literal_rejected(AF &framework, uint32_t argument, bool isPositive)
{
	int64_t variable = static_cast<int64_t>(argument) + framework.num_args;
	return isPositive ? variable : -1 * variable;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

int64_t Encoding::get_literal_aux(AF &framework, uint32_t index, bool isPositive)
{
	// use offset (2 * framework.num_args), because all arguments are decoded as [1 ... framework.num_args], hence all positive literals are decoded same as the arguments
    // while all negative literals are decoded as [(framework.num_args + 1) ... (framework.num_args + framework.num_args)]. Therefore use space above neg. literals.
	int64_t variable = static_cast<int64_t>(index) + 2 * framework.num_args + 1;
	return isPositive ? variable : -1 * variable;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static void add_clause(SatSolver &solver, std::vector<int64_t> &clause)
{
    solver.add_clause(clause);
    clause.clear();
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static void add_clause_consistence(SatSolver &solver, AF &framework, uint32_t argument)
{
	solver.add_clause_short(
		Encoding::get_literal_accepted(argument, false),
		Encoding::get_literal_rejected(framework, argument, false)
		);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static void add_clause_legal_in(SatSolver &solver, AF &framework, uint32_t argument, uint32_t attacker)
{
	solver.add_clause_short(
		Encoding::get_literal_accepted(argument, false),
		Encoding::get_literal_rejected(framework, attacker, true)
		);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static vector<int64_t> create_clause_legal_out(AF &framework, uint32_t argument)
{
	vector<int64_t> legal_out_clause;
	legal_out_clause.push_back(Encoding::get_literal_rejected(framework, argument, false));
	return legal_out_clause;
}

static void update_clause_legal_out(vector<int64_t> &clause, uint32_t attacker)
{
	clause.push_back(Encoding::get_literal_accepted(attacker, true));
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static vector<int64_t> add_clauses_nonempty_admissible_set_part_one(SatSolver &solver, AF &framework, vector<int64_t> &non_empty_clause, uint32_t argument)
{
	add_clause_consistence(solver, framework, argument);
	non_empty_clause.push_back(Encoding::get_literal_accepted(argument, true));
	return create_clause_legal_out(framework, argument);
}

static void add_clauses_nonempty_admissible_set_part_two(SatSolver &solver, AF &framework, uint32_t argument, std::vector<int64_t> &legal_out_clause, uint32_t attacker)
{
    add_clause_legal_in(solver, framework, argument, attacker);
    update_clause_legal_out(legal_out_clause, attacker);
}

void Encoding::add_clauses_nonempty_admissible(SatSolver &solver, AF &framework)
{
	vector<int64_t> non_empty_clause;

	//////////////////////////////////////// FOR ALL ARGUMENTS /////////////////////////////////////////////////////////
	for (std::vector<unsigned int>::size_type i = 1; i < framework.num_args; i++) {
		uint32_t argument = i;
		vector<int64_t> legal_out_clause = add_clauses_nonempty_admissible_set_part_one(solver, framework, non_empty_clause, argument);

		//////////////////////////////////////// FOR ALL ATTACKERS /////////////////////////////////////////////////////////
		vector<uint32_t> attackers = framework.attackers[argument];
		for (std::vector<unsigned int>::size_type i = 0; i < attackers.size(); i++)
		{
			uint32_t attacker = attackers[i];
			add_clauses_nonempty_admissible_set_part_two(solver, framework, argument, legal_out_clause, attacker);
		}

        add_clause(solver, legal_out_clause);
    }
	
	add_clause(solver, non_empty_clause);
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static vector<int64_t> create_clause_legal_undec_out(uint32_t argument)
{
	vector<int64_t> clause;
	clause.push_back(Encoding::get_literal_accepted(argument, true));
	return clause;
}

static void update_clause_legal_undec_out(AF &framework, vector<int64_t> &clause, uint32_t attacker)
{
	clause.push_back(Encoding::get_literal_rejected(framework, attacker, false));
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

static void add_clause_legal_undec_in(SatSolver &solver, AF &framework, uint32_t argument, uint32_t attacker)
{
	solver.add_clause_short(
		Encoding::get_literal_accepted(attacker, false),
		Encoding::get_literal_rejected(framework, argument, true)
	); 
}
/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void Encoding::add_clauses_nonempty_complete(SatSolver &solver, AF &framework)
{
	vector<int64_t> non_empty_clause;

	//////////////////////////////////////// FOR ALL ARGUMENTS /////////////////////////////////////////////////////////
	for (std::vector<unsigned int>::size_type i = 1; i < framework.num_args; i++) {
		uint32_t argument = i;
		vector<int64_t> legal_out_clause = add_clauses_nonempty_admissible_set_part_one(solver, framework, non_empty_clause, argument);
		vector<int64_t> legal_undec_out_clause = create_clause_legal_undec_out(argument);

		//////////////////////////////////////// FOR ALL ATTACKERS /////////////////////////////////////////////////////////
		vector<uint32_t> attackers = framework.attackers[argument];
		for (std::vector<unsigned int>::size_type i = 0; i < attackers.size(); i++)
		{
			uint32_t attacker = attackers[i];
            add_clauses_nonempty_admissible_set_part_two(solver, framework, argument, legal_out_clause, attacker);
			update_clause_legal_undec_out(framework, legal_undec_out_clause, attacker);
			add_clause_legal_undec_in(solver, framework, argument, attacker);
		}

        add_clause(solver, legal_out_clause);
		add_clause(solver, legal_undec_out_clause);
    }
	
	add_clause(solver, non_empty_clause);
}