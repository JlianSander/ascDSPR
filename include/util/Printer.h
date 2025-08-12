#ifndef PRINTER_H
#define PRINTER_H

#include <iostream>
#include <vector>
#include <unordered_set>
#include <cstdint>
#include <list>

using namespace std;

/// <summary>
/// This class is responsible for printing data to console.
/// </summary>
class Printer {

public:
	/// <summary>
	/// Prints the specified list to console.
	/// </summary>
	/// <param name="list">The list to print.</param>
	static void print_list(list<uint32_t> &list);

	/// <summary>
	/// Prints the specified set to console.
	/// </summary>
	/// <param name="setToPrint">The set to print</param>
	static void print_set(unordered_set<uint32_t> &setToPrint);

	/// <summary>
	/// Prints the specified vector to console.
	/// </summary>
	/// <param name="vector">The vector to print.</param>
	static void print_vector(vector<uint32_t> &vector);

	/// <summary>
	/// Prints the specified vector to console.
	/// </summary>
	/// <param name="vector">The vector to print.</param>
	static void print_vector(vector<int64_t> &vector);
};
#endif