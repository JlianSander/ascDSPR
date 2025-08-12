#ifndef CONEOFINFLUENCE_H
#define CONEOFINFLUENCE_H


#include <vector>
#include <cstdint>
#include <list>

#include "AF.h"

using namespace std;

/// <summary>
/// This class is responsible for representing the data of a cone of influence created by an argument in a abstract argumentation framework.
/// </summary>
class ConeOfInfluence {
public:
	/// <summary>
	/// Lists the distance from each argument in the cone to the starting argument of the cone. Distance is measured by the minimal amount of moves between arguments that have to be
	/// made to reach the starting argument. The starting argument itself has a distance to itself of 0, its direct attackers have a distance of 1.
	/// </summary>
	vector<uint32_t> Distance_to_query;
	/// <summary>
	/// The maximum distance of an argument to the starting argument within the cone of influence
	/// </summary>
	uint32_t Max_distance;

	/// <summary>
	/// Instantiates a new cone of influence, based on a specified argumentation framework
	/// </summary>
	/// <param name="framework">The framework in which the cone is situated.</param>
	ConeOfInfluence(AF &framework);
};

/// <summary>
/// This class is responsible for representing the data of a pair consisting of an argument, and its distance to the starting argument of a cone of influence.
/// </summary>
class ArgumentDistancePair {
public:
	bool operator == (ArgumentDistancePair const &other)
	{
		return (other.Argument == Argument);
	};

	/// <summary>
	/// The argument, which distance to the starting argument of the cone is measured. 
	/// </summary>
	uint32_t Argument;
	/// <summary>
	/// The distance from the associated argument to the starting argument of the cone. Distance is measured by the minimal amount of moves between arguments that have to be
	/// made to reach the starting argument. The starting argument itself has a distance to itself of 0, its direct attackers have a distance of 1.
	/// </summary>
	uint32_t Distance_to_query;

	/// <summary>
	/// Instantiates a new pair based on a specified cone of influence and one argument of this cone.
	/// </summary>
	/// <param name="argument">An argument of the specified cone of influence.</param>
	/// <param name="coi">A cone of influence.</param>
	ArgumentDistancePair(uint32_t argument, ConeOfInfluence &coi);
	/// <summary>
	/// Compares if the associated argument of two pairs of the same cone of influence have the same distance to the starting argument of the cone. 
	/// </summary>
	/// <param name="firstElem"> First pair to compare.</param>
	/// <param name="secondElem"> Second pair to compare.</param>
	/// <returns>TRUE iff the two associated argument have the same distance to the starting argument of the associated cone of influence.</returns>
	static bool compare_by_distance(ArgumentDistancePair &firstElem, ArgumentDistancePair &secondElem);
};

inline bool operator == (ArgumentDistancePair const &lhs, ArgumentDistancePair const &rhs)
{
	return (lhs.Argument == rhs.Argument);
};
#endif