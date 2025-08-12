#ifndef MEMORY_WATCHDOG_H
#define MEMORY_WATCHDOG_H

#include <stdlib.h>
#include <sys/resource.h>

/// <summary>
/// This method returns the currently used total memory of the program itself.
/// </summary>
/// <returns>Memory usage in kB</returns>
long get_mem_usage();

/// <summary>
/// This method returns the number of voluntarily context switches that occured during the runtime.
/// </summary>
/// <returns>Number of voluntarily context switches on the CPU's</returns>
long get_ctxt_switches_volun();

/// <summary>
/// This method returns the number of involuntary context switches that occured during the runtime.
/// </summary>
/// <returns>Number of involuntary context switches on the CPU's</returns>
long get_ctxt_switches_involun();

#endif