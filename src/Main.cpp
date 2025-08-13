#include "../include/Main.h"

using namespace std;

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void static print_usage()
{
	cout << "Usage: " << PROGRAM_NAME << " -p <task> -f <file> -fo <format> [-a <query>]\n\n";
	cout << "  <task>      computational problem; for a list of available problems use option --problems\n";
	cout << "  <file>      input argumentation framework\n";
	cout << "  <format>    file format for input AF; for a list of available formats use option --formats\n";
	cout << "  <query>     query argument\n";
	cout << "Options:\n";
	cout << "  --help      Displays this help message.\n";
	cout << "  --version   Prints version and author information.\n";
	cout << "  --formats   Prints available file formats.\n";
	cout << "  --problems  Prints available computational tasks.\n";
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void static print_version()
{
	cout << PROGRAM_NAME << " (version "<< VERSIONNUMBER <<")\n"
		<< "Lars Bengel, University of Hagen <lars.bengel@fernuni-hagen.de>\n" 
		<< "Julian Sander, University of Hagen <julian.sander@fernuni-hagen.de>\n"
		<< "Matthias Thimm, University of Hagen <matthias.thimm@fernuni-hagen.de>\n";
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void static print_formats()
{
	cout << "[i23,tgf]\n";
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void static print_problems()
{
	cout << "[DS-PR]" << endl;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

int static execute(int argc, char **argv)
{
	// read command arguments
	if (argc == 1) {
		print_version();
		return 0;
	}

	int option_index = 0;
	int opt = 0;
	string problem, file, fileformat, query;

	while ((opt = getopt_long_only(argc, argv, "", longopts, &option_index)) != -1) {
		switch (opt) {
		case 0:
			break;
		case 'p':
			problem = optarg;
			break;
		case 'f':
			file = optarg;
			break;
		case 'o':
			fileformat = optarg;
			break;
		case 'a':
			query = optarg;
			break;
		default:
			return 1;
		}
	}

	if (version_flag) {
		print_version();
		return 0;
	}

	if (usage_flag) {
		print_usage();
		return 0;
	}

	if (formats_flag) {
		print_formats();
		return 0;
	}

	if (problems_flag) {
		print_problems();
		return 0;
	}

	if (problem.empty()) {
		cerr << argv[0] << ": Problem must be specified via -p flag\n";
		return 1;
	}

	if (file.empty()) {
		cerr << argv[0] << ": Input file must be specified via -f flag\n";
		return 1;
	}

	if (fileformat.empty()) {
		fileformat = file.substr(file.find_last_of(".") + 1, file.length() - file.find_last_of(".") - 1);
	}

	// parse the framework
	AF framework;
	uint32_t query_argument = 0;
	switch (Enums::string_to_format(fileformat)) {
		case I23:
			query_argument = ParserICCMA::parse_af_i23(framework, query, file);
			break;
		case TGF:
			query_argument = ParserICCMA::parse_af_tgf(framework, query, file);
			break;
		default:
			cerr << argv[0] << ": Unsupported file format\n";
			return 1;
	}

	// parse the problem and semantics
	string task = problem.substr(0, problem.find("-"));
	problem.erase(0, problem.find("-") + 1);
	string sem = problem.substr(0, problem.find("-"));
		
	// process the problem
	if(Enums::string_to_task(task) != DS)
	{
		cerr << argv[0] << ": Unsupported problem\n";
		return 1;
	}

	if(Enums::string_to_sem(sem) != preferred)
	{
		cerr << argv[0] << ": Unsupported semantics\n";
		return 1;
	}

	if (query_argument == 0) {
		cerr << argv[0] << ": Query argument must be specified via -a flag and greater than 0\n";
		return 1;
	}

	ALGO_SHORT_T shortcut;
	acceptance_result result = shortcut.try_solve(framework, query_argument);
	// print result
	if(result == acceptance_result::accepted || result == acceptance_result::rejected)
	cout << (result == acceptance_result::accepted ? "YES" : "NO") << endl;

	return 0;
}

int main(int argc, char **argv)
{
	execute(argc, argv);
}