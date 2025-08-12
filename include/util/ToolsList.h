#ifndef TOOLS_LIST_H
#define TOOLS_LIST_H

#include<cstdint>
#include<list>
#include<vector>

namespace tools {

	/// <summary>
	/// This class is responsible for offering helping methods for lists.
	/// </summary>
	class Tools_List {

	public:
		/// <summary>
		/// This method copies the specified lists in a newly created third list, which starts with the elements from ListA.
		/// </summary>
		/// <param name="listA">List of elements to be in the front of the list to create.</param>
		/// <param name="ListB">List of elements to be in the back of the list to create.</param>
		/// <returns>Newly created list, that holds copies of the specified input lists.</returns>
		static std::list<uint32_t> extend_list(std::list<uint32_t> &listA, std::list<uint32_t> &listB);

		/// <summary>
		/// This method copies all elements of the specified vector in the specified list, without removing the element from the vector.
		/// </summary>
		/// <param name="list_dest">List of element, in which the elements of the vector get inserted in.</param>
		/// <param name="vector_source">Vector, which elements get copied in the list.</param>
		static void copy_in_list(std::list<uint32_t> &list_dest, std::vector<uint32_t> vector_source);

		/// <summary>
		/// Checks if a specified element is contained in the specified list.
		/// </summary>
		/// <param name="list">The list to search through.</param>
		/// <param name="query">The element, which inclusion is to be checked.</param>
		/// <returns>TRUE iff the element is contained. FALSE otherwise.</returns>
		static bool contains(std::list<uint32_t> list_input, uint32_t query);
	};
};
#endif