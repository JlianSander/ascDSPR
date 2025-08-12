#ifndef PARSER_ICCMA
#define PARSER_ICCMA

#include <cstdint>
#include <iostream>			
#include <fstream>			
#include <algorithm>
#include <sstream>
#include <unordered_map>

#include <omp.h>

#include "AF.h"

extern "C" {
	#include "../util/MemoryWatchDog.h"
}

using namespace std;

/// <summary>
/// This class is responsible for parsing a file into a data type representing an abstract argumentation framework.
/// </summary>
class ParserICCMA {
public:

	/// <summary>
	/// This method parses an abstract argumentation framework from a file, which complies to the ICCMA'23 format, located 
	/// at the specified path.
	/// </summary>
	/// <param name="framework"> Object of the framework to create.</param>
	/// <param name="query"> String that describes the query argument.</param>
	/// <param name="file">String that describes the location of the file to open.</param>
	/// <returns> The query argument of this task <\returns>
	static uint32_t parse_af_i23(AF &framework, string query, string file);

	/// <summary>
	/// This method parses an abstract argumentation framework from a file, which complies to the tgf format, located 
	/// at the specified path.
	/// </summary>
	/// <param name="framework"> Object of the framework to create.</param>
	/// <param name="file">String that describes the location of the file to open.</param>
	/// <returns> The query argument of this task <\returns>
	static uint32_t parse_af_tgf(AF &framework, string query, string file);
};

#endif