#include "../../include/logic/Parser_iccma.h"

using namespace std;

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

uint32_t ParserICCMA::parse_af_i23(AF &framework, string query, string file)
{
	ifstream input;
	input.open(file);

	if (!input.good()) {
		cerr << "Cannot open input file\n";
		exit(1);
	}

	// parse first line
	string line;
	int32_t n_args = 0;
	getline(input, line);
	std::istringstream iss(line);
	if (line[0] == 'p') {
		string p, af;
		iss >> p >> af >> n_args;
	}
	else {
		cerr << "File does not comply to ICCMA'23 format\n";
		exit(1);
	}

	// parse rest of lines
	framework.initialize(n_args);
	while (!input.eof()) {
		getline(input, line);
		if (line.length() == 0 || line[0] == '#') continue;
		std::istringstream iss(line);
		uint32_t attacker, victim;
		iss >> attacker >> victim;
		framework.add_attack(attacker, victim);
	}

	input.close();
	framework.finish_initilization();

	if (!query.empty()) {
		return std::stoi(query);
	}
	else {
		return 0;
	}
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

uint32_t ParserICCMA::parse_af_tgf(AF &framework, string query, string file) {
	ifstream input;
	input.open(file);

	if (!input.good()) {
		cerr << "Cannot open input file\n";
		exit(1);
	}

	// parse first part about arguments
	string line, arg;
	uint32_t n_args = 0;
	unordered_map<string, uint32_t> arg_str_to_int;
	while (!input.eof()) {
		getline(input, line);
		std::istringstream iss(line);
		iss >> arg;
		if (arg == "#") break;
		arg_str_to_int[arg] = ++n_args;
	}

	// parse second part about attacks
	framework.initialize(n_args);
	string attacker, victim;
	while (!input.eof()) {
		getline(input, line);
		if (line.empty()) break;
		std::istringstream iss(line);
		iss >> attacker >> victim;
		framework.add_attack(arg_str_to_int[attacker], arg_str_to_int[victim]);
	}

	input.close();
	framework.finish_initilization();

	if (!query.empty()) {
		return  arg_str_to_int[query];
	}
	else {
		return 0;
	}
}