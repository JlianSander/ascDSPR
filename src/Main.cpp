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
	cout << "[DC-CO,DC-ST,DS-PR,DS-ST,SE-PR,SE-ST]" << endl;
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

void static print_proof(std::__cxx11::list<uint32_t> &proof_extension)
{
	cout << "w ";

	if (!proof_extension.empty()) {
		for (list<uint32_t>::iterator mIter = proof_extension.begin(); mIter != proof_extension.end(); ++mIter) {
			cout << *mIter << " ";
		}
		cout << endl;
	}
}

void static print_proof(std::__cxx11::list<uint32_t> &proof_extension, unordered_map<uint32_t, uint32_t> &args_new_to_old)
{
	cout << "w ";

	if (!proof_extension.empty()) {
		for (list<uint32_t>::iterator mIter = proof_extension.begin(); mIter != proof_extension.end(); ++mIter) {
			cout << args_new_to_old[*mIter] << " ";
		}
		cout << endl;
	}
}

/*===========================================================================================================================================================*/
/*===========================================================================================================================================================*/

bool static check_query(uint32_t query, char **argv)
{
	if (query == 0) {
		cerr << argv[0] << ": Query argument must be specified via -a flag\n";
		return false;
	}
	return true;
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
	bool has_preprocessed = false;
	unordered_map<uint32_t, uint32_t> args_new_to_old;

	// parse the problem and semantics
	string task = problem.substr(0, problem.find("-"));
	problem.erase(0, problem.find("-") + 1);
	string sem = problem.substr(0, problem.find("-"));

	//preprocess if compiler flag is set
#ifdef DO_PREPROC
	//calculate relevant arguments for problems DC-CO and DS-PR
	if ((Enums::string_to_task(task) == DS && Enums::string_to_sem(sem) == preferred)
		|| (Enums::string_to_task(task) == DC && Enums::string_to_sem(sem) == complete)) {
		has_preprocessed = true;
		framework = PreProcessor::calculate_cone_influence(framework, query_argument, args_new_to_old);
		query_argument = 1;
	}	
#endif
		
	// process the problem
	switch (Enums::string_to_task(task)) {
		// skeptical acceptance problem
		case DS:
		{
			if (!check_query(query_argument, argv)) {
				return 1;
			}			

			list<uint32_t> proof_extension;
			bool skept_accepted = false;

			// process the semantics
			switch (Enums::string_to_sem(sem)) {
				case preferred:
					skept_accepted = Solver_DS_PR::solve(query_argument, framework, proof_extension);
					break;
				case stable:
					skept_accepted = Solver_DS_ST::solve(query_argument, framework, proof_extension);
					break;
				default:
					cerr << argv[0] << ": Unsupported semantics\n";
					return 1;
			}

			// print result
			cout << (skept_accepted ? "YES" : "NO") << endl;
			if (!skept_accepted)
			{
				if (has_preprocessed)
				{
					print_proof(proof_extension, args_new_to_old);
				}
				else 
				{
					print_proof(proof_extension);
				}
			}

			//free allocated memory
			proof_extension.clear();			
		}
		break;

		// credulous acceptance problem
		case DC:
		{
			if (!check_query(query_argument, argv)) {
				return 1;
			}

			list<uint32_t> proof_extension;
			bool cred_accepted = false;

			// process the semantics
			switch (Enums::string_to_sem(sem)) {
			case complete:
				cred_accepted = Solver_DC_CO::solve(query_argument, framework, proof_extension);
				break;
			case stable:
				cred_accepted = Solver_DC_ST::solve(query_argument, framework, proof_extension);
				break;
			default:
				cerr << argv[0] << ": Unsupported semantics\n";
				return 1;
			}

			// print result
			cout << (cred_accepted ? "YES" : "NO") << endl;
			if (cred_accepted)
			{
				if (has_preprocessed)
				{
					print_proof(proof_extension, args_new_to_old);
				}
				else
				{
					print_proof(proof_extension);
				}
			}

			//free allocated memory
			proof_extension.clear();
		}
		break;

		// single extension problem
		case SE:
		{
			list<uint32_t> proof_extension;
			bool has_extension = false;

			// process the semantics
			switch (Enums::string_to_sem(sem)) {
			case preferred:
				has_extension = Solver_SE_PR::solve(framework, proof_extension);
				break;
			case stable:
				has_extension = Solver_SE_ST::solve(framework, proof_extension);
				break;
			default:
				cerr << argv[0] << ": Unsupported semantics\n";
				return 1;
			}

			// print result
			if (has_extension)
			{
				if (has_preprocessed)
				{
					print_proof(proof_extension, args_new_to_old);
				}
				else
				{
					print_proof(proof_extension);
				}
			}
			else {
				cout << "NO" << endl;
			}

			//free allocated memory
			proof_extension.clear();
		}
		break;
			
		default:
			cerr << argv[0] << ": Problem not supported!\n";
			return 1;
	}

	return 0;
}

int main(int argc, char **argv)
{
	execute(argc, argv);
}