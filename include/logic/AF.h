#ifndef AF_H
#define AF_H

#include <vector>
#include <unordered_set>
#include <cstdint>
#include <iostream>	
#include <omp.h>

#include "../util/ArrayBitSet.h"

template <class T>
inline void hash_combine(std::size_t &seed, const T &v)
{
	std::hash<T> hasher;
	seed ^= hasher(v) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}

namespace std
{
	template<typename S, typename T> struct hash<pair<S, T>>
	{
		inline size_t operator()(const pair<S, T> &v) const
		{
			size_t seed = 0;
			::hash_combine(seed, v.first);
			::hash_combine(seed, v.second);
			return seed;
		}
	};
}

/// <summary>
/// This class is responsible for representing the data of an abstract argumentation framework.
/// </summary>
class AF {

public:

    /// <summary>
    /// Number of arguments in the abstract argumentation framework.
    /// </summary>
    uint32_t num_args;
    /// <summary>
    /// Lists for each argument a list of the arguments, attacking it.
    /// </summary>
    std::vector<vector<uint32_t>> attackers;
	/// <summary>
	/// Lists for each argument a list of the arguments, which are attacked by it.
	/// </summary>
	std::vector<vector<uint32_t>> victims;
	/// <summary>
	/// Booleans indicating if an argument attacks itself.
	/// </summary>
	std::vector<uint8_t> self_attack;
    /// <summary>
    /// Set in which the buckets contain pairs of arguments, indicating that the first argument is attacking the second.
    /// </summary>
    std::unordered_set<std::pair<uint32_t, uint32_t>> attacks;

    /// <summary>
    /// Adds an attack to the instance.
    /// </summary>
    /// <param name="attacker">The argument which is attacking the other.</param>
    /// <param name="victim">The argument which is been attacked by the other.</param>
    /// <returns>TRUE iff the attack was successfully added.</returns>
    bool add_attack(uint32_t attacker, uint32_t victim);
	/// <summary>
	/// Checks if a specified argument gets attacked by any member of the specified set of arguments.
	/// </summary>
	/// <param name="argument">An argument of the framework.</param>
	/// <param name="set_arguments">Set of arguments of the framework.</param>
	/// <param name="framework">The abstract argumentation framework, specifying the underlying attack relations between the arguments.</param>
	/// <returns>TRUE iff any member of the set attacks the specified argument. FALSE otherwise.</returns>
	bool check_attack(std::uint32_t argument, std::list<std::uint32_t> &set_arguments, AF &framework);
	/// <summary>
	/// This method deletes the data structure of the instance.
	/// </summary>
	void clear();
	/// <summary>
	/// This method creates an ArrayBitSet containing all arguments of this framework.
	/// </summary>
	/// <returns>An ArrayBitSet of all arguments in this framework.</returns>
	ArrayBitSet create_active_arguments();
	/// <summary>
	/// Deletes an attack of the instance.
	/// </summary>
	/// <param name="attacker">The argument which is attacking the other.</param>
	/// <param name="victim">The argument which is been attacked by the other.</param>
	/// <returns>TRUE iff the attack was successfully deleted.</returns>
	bool delete_attack(uint32_t attacker, uint32_t victim);
    /// <summary>
    /// This method checks if there's an attack from the first to the second specified 
	/// argument.
    /// </summary>
    /// <param name="attacker">The argument which is attacking the other.</param>
    /// <param name="victim">The argument which is been attacked by the other.</param>
    /// <returns>TRUE iff there is an attack.</returns>
    bool exists_attack(uint32_t attacker, uint32_t victim) const;
    /// <summary>
    /// This method signals the instance, that it has all necessary information to finish
	/// the initialization process.
    /// </summary>
    void finish_initilization();
	/// <summary>
	/// This method starts the initialization process on this instance.
	/// </summary>
	/// <param name="number_args">The number of arguments in the framework to initialize.</param>
	void initialize(uint32_t number_args);
};

#endif