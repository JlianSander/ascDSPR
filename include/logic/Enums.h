#ifndef ENUMS_H
#define ENUMS_H

#include "../ipafair.h"

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdexcept>

#include <iostream>

/// <summary>
/// Abbreviations of the different types of tasks, which the solver can solve
/// </summary>
enum task { DC, DS, SE, UNKNOWN_TASK };

/// <summary>
/// Return values of the preprocessor, indicating if the preprocessor solved the problem, and if so to what conclusion
/// </summary>
enum acceptance_result { accepted, rejected, unknown };

/// <summary>
/// Abbreviations of the different file formats, that the solver can handle
/// </summary>
enum format {I23, TGF, UNKNOWN_FORMAT};

using namespace std;

/// <summary>
/// This class is responsible for converting to and from Enum-Data-Types.
/// </summary>
class Enums {
public:

	/// <summary>
	/// This method converts the specified string into a task.
	/// </summary>
	/// <param name="task_abbreviation">String containing the abbreviation of the task as used in the enum.</param>
	/// <returns>Task corresponding to the specified string.</returns>
	static task string_to_task(string task_abbreviation);

	/// <summary>
	/// This method converts the specified string into a semantics.
	/// </summary>
	/// <param name="semantics_abbreviation">String containing the abbreviation of the semantics as used in the enum.</param>
	/// <returns>Semantics corresponding to the specified string.</returns>
	static semantics string_to_sem(string semantics_abbreviation);

	/// <summary>
	/// This method converts the specified string into a file format.
	/// </summary>
	/// <param name="format_abbreviation">String containing the abbreviation of the file format as used in the enum.</param>
	/// <returns>File format corresponding to the specified string.</returns>
	static format string_to_format(string format_abbreviation);
};

#endif