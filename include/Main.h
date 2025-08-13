#ifndef MAIN_H
#define MAIN_H

#include <cstdio>
#include <iostream>
#include <stdio.h>
#include <stdint.h>
#include <getopt.h>

extern "C" {
	#include "../include/util/MemoryWatchDog.h"
}

#include "../include/logic/AF.h"
#include "../include/logic/Parser_iccma.h"
#include "../include/logic/Solver_DS_PR.h"

#include "../include/logic/Enums.h"

#if defined(ASC_1)
	#include "AlgorithmicShortcut_1.h"
	typedef AlgorithmicShortcut_1 ALGO_SHORT_T;
#elif defined(ASC_2)
	#include "AlgorithmicShortcut_2.h"
	typedef AlgorithmicShortcut_2 ALGO_SHORT_T;
#else
	//#error "No SAT Solver defined"
#endif

/// <summary>
/// Name of the program
/// </summary>
constexpr auto PROGRAM_NAME = "ascDSPR";
constexpr auto VERSIONNUMBER = "0.1";

/// <summary>
/// Flags used for internal processing.
/// </summary>
static int version_flag = 0;
static int usage_flag = 0;
static int formats_flag = 0;
static int problems_flag = 0;

/// <summary>
/// Different options that can be added to a execution call of this application.
/// </summary>
const struct option longopts[] =
{
	{"help", no_argument, &usage_flag, 1},
	{"version", no_argument, &version_flag, 1},
	{"formats", no_argument, &formats_flag, 1},
	{"problems", no_argument, &problems_flag, 1},
	{"p", required_argument, 0, 'p'},
	{"f", required_argument, 0, 'f'},
	{"fo", required_argument, 0, 'o'},
	{"a", required_argument, 0, 'a'},
	{0, 0, 0, 0}
};

/// <summary>
/// This method is used to start the program.
/// </summary>
/// <param name="argc">Number of arguments with which the program got started.</param>
/// <param name="argv">Array of strings, containing the different starting arguments of this progam.</param>
/// <returns>0 iff the program exited without error. 1 otherwise.</returns>
int main(int argc, char **argv);

#endif